from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4
from fastapi import Depends, FastAPI, File, Request, Response, UploadFile, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session
from .auth import AuthenticatedUser, require_user
from .billing import (
    PLANS,
    check_mission_limit,
    create_checkout_session,
    create_portal_session,
    handle_webhook,
    increment_mission_count,
)
from .config import settings
from .database import engine, get_session
from .errors import AppError
from .exception_handlers import (
    app_error_handler,
    ensure_request_id,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from .models import (
    AnswerQuestionRequest,
    AnswerQuestionResponse,
    CitationItem,
    CreateMissionRequest,
    CreateMissionResponse,
    CreateProjectRequest,
    CreateShareLinkResponse,
    DossierReadModel,
    ExportReadModel,
    MissionReadModel,
    ProjectSummary,
    RendererRequest,
    RuntimeInputItem,
    RuntimeResumeRequest,
    RuntimeStartRequest,
    SearchMissionInputsRequest,
    SearchMissionInputsResponse,
    UploadMissionInputResponse,
    utc_now,
)
from .migrations import run_sql_migrations
from .renderer_client import RendererClient
from .repository import ControlPlaneRepository
from .runtime_client import RuntimeClient
from .file_search import FileSearchClient
from .uploads import LocalUploadStorage, S3UploadStorage

import logging
import time

logger = logging.getLogger(__name__)

runtime_client = RuntimeClient()
renderer_client = RendererClient()

if settings.s3_bucket:
    upload_storage = S3UploadStorage(settings.s3_bucket, settings.s3_endpoint)
else:
    upload_storage = LocalUploadStorage(settings.uploads_dir)

file_search_client: FileSearchClient | None = None
if settings.openai_api_key:
    file_search_client = FileSearchClient(settings.openai_api_key)


def to_runtime_inputs(items):
    return [
        RuntimeInputItem(
            id=item.id,
            kind=item.kind,
            source=item.source,
            content=item.content,
            display_name=item.display_name,
            mime_type=item.mime_type,
            byte_size=item.byte_size,
            preview_text=item.preview_text,
        )
        for item in items
        if item.kind == "uploaded_file"
    ]


@asynccontextmanager
async def lifespan(_: FastAPI):
    run_sql_migrations(engine, Path(__file__).resolve().parent.parent / "sql")
    # Recover runs that were in-flight when the server last stopped
    from sqlalchemy.orm import Session as _Session
    with _Session(engine) as startup_session:
        repo = ControlPlaneRepository(startup_session)
        recovered = repo.recover_stale_runs()
        if recovered:
            logger.info("recovered %d stale agent run(s) at startup", recovered)
    yield


app = FastAPI(title="Cadris Control Plane", version="0.1.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def request_id_middleware(request: Request, call_next):
    request_id = ensure_request_id(request)
    start = time.perf_counter()
    response: Response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 1)
    response.headers["x-request-id"] = request_id
    logger.info(
        "request completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
            "request_id": request_id,
        },
    )
    return response


app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


@app.get("/health")
async def healthcheck():
    return {"ok": True}


@app.get("/api/projects", response_model=list[ProjectSummary])
async def list_projects(
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    return repository.list_projects_for_user(user.id)


@app.get("/api/missions")
async def list_missions(
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """List all missions for the authenticated user (most recent first)."""
    repository = ControlPlaneRepository(session)
    return repository.list_missions_for_user(user.id)


@app.delete("/api/missions/{mission_id}", status_code=204)
async def delete_mission(
    mission_id: str,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Delete a mission and its dossier (user must own it)."""
    repository = ControlPlaneRepository(session)
    mission = repository.get_mission_for_user(user.id, mission_id)
    if not mission:
        raise AppError.not_found("mission_not_found", "Mission not found.")
    repository.delete_mission(mission_id)
    return Response(status_code=204)


@app.post("/api/projects", response_model=ProjectSummary, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: CreateProjectRequest,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    return repository.create_project(
        user_id=user.id,
        project_id=f"project_{uuid4().hex[:10]}",
        name=payload.name.strip(),
    )


@app.post(
    "/api/projects/{project_id}/missions",
    response_model=CreateMissionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_mission(
    project_id: str,
    payload: CreateMissionRequest,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    project = repository.get_project_for_user(user.id, project_id)
    if not project:
        raise AppError.not_found("project_not_found", "Project not found.")

    from .models import FLOW_LABELS

    flow_code = payload.flow_code
    flow_label = FLOW_LABELS.get(flow_code, flow_code)

    db_user = repository.get_user(user.id)
    user_plan = db_user.plan if db_user else "free"

    mission_id = f"mission_{uuid4().hex[:10]}"
    runtime_response = await runtime_client.start_mission(
        RuntimeStartRequest(
            mission_id=mission_id,
            project_name=project.name,
            intake_text=payload.intake_text.strip(),
            flow_code=flow_code,
            plan=user_plan,
            supporting_inputs=[],
        )
    )

    mission = MissionReadModel(
        id=mission_id,
        project_id=project.id,
        flow_code=flow_code,
        flow_label=flow_label,
        title=f"{flow_label} - {project.name}",
        status=runtime_response.status,
        summary=runtime_response.summary,
        next_step=runtime_response.next_step,
        intake_text=payload.intake_text.strip(),
        artifact_blocks=runtime_response.artifact_blocks,
        active_question=runtime_response.active_question,
        active_agents=runtime_response.active_agents,
        recent_messages=runtime_response.recent_messages,
        timeline=runtime_response.timeline,
        dossier_ready=False,
        updated_at=utc_now(),
    )
    repository.upsert_mission(mission)
    repository.append_mission_input(
        mission_id=mission.id,
        kind="intake_text",
        source="user",
        content=payload.intake_text.strip(),
    )
    repository.upsert_question(mission_id=mission.id, question=mission.active_question)
    repository.replace_mission_agents(mission_id=mission.id, agents=mission.active_agents)
    repository.replace_messages(mission_id=mission.id, messages=mission.recent_messages)
    run_id = repository.create_agent_run(
        mission_id=mission.id,
        run_id=f"run_{uuid4().hex[:10]}",
        kind="start",
        idempotency_key=f"{mission.id}:start",
    )
    repository.update_agent_run(run_id=run_id, status=mission.status)

    updated_project = repository.update_project_after_mission(
        project_id=project.id,
        active_mission_id=mission.id,
        active_mission_status=mission.status,
        mission_delta=1,
    )

    persisted_mission = repository.get_mission_for_user(user.id, mission.id)
    if persisted_mission is None:
        raise AppError.internal(message="Mission creee mais non relisible.")

    return CreateMissionResponse(project=updated_project, mission=persisted_mission)


# ── SSE streaming helpers ──────────────────────────────────


def _persist_dossier_from_docs(
    db_session: Session,
    mission_id: str,
    collected_docs: dict[str, dict],
    *,
    is_final: bool = False,
) -> None:
    """Build and persist a DossierReadModel from streamed document_updated events.

    Merges new docs with any existing dossier sections from previous waves,
    so the final dossier contains ALL documents across all waves.
    """
    from .models import DossierSection as DossierSectionModel

    if not collected_docs:
        return
    try:
        repo = ControlPlaneRepository(db_session)

        # Load existing sections from previous waves (if any)
        existing_dossier = repo.get_dossier(mission_id)
        existing_map: dict[str, DossierSectionModel] = {}
        if existing_dossier:
            for s in existing_dossier.sections:
                existing_map[s.id] = s

        # Merge: new docs override existing ones with same id
        for doc_id, doc in collected_docs.items():
            existing_map[doc_id] = DossierSectionModel(
                id=doc_id,
                title=doc.get("title", doc_id),
                content=doc.get("content", ""),
                certainty=doc.get("certainty", "unknown"),
            )

        sections = list(existing_map.values())

        # Build combined markdown
        md_parts = ["# Dossier de cadrage\n"]
        for s in sections:
            md_parts.append(f"## {s.title}\n\n{s.content}\n")
        markdown = "\n".join(md_parts)

        dossier = DossierReadModel(
            mission_id=mission_id,
            title="Dossier de cadrage",
            quality_label="",
            summary="Dossier genere par les agents Cadris.",
            markdown=markdown,
            sections=sections,
            updated_at=utc_now(),
        )
        repo.upsert_dossier(dossier)

        if is_final:
            # Mark mission as completed with dossier_ready
            from .records import MissionRecord
            record = db_session.get(MissionRecord, mission_id)
            if record:
                record.status = "completed"
                record.dossier_ready = True
                db_session.commit()

        logger.info("persisted dossier for mission %s (%d sections, final=%s)", mission_id, len(sections), is_final)
    except Exception:
        logger.error("failed to persist dossier for mission %s", mission_id, exc_info=True)


# ── SSE streaming endpoint ─────────────────────────────────


@app.post("/api/missions/run")
async def run_mission_stream(
    payload: CreateMissionRequest,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Launch a collaborative mission and stream SSE events to the client.

    This creates the project + mission inline, then streams real-time
    events from the runtime's collaborative engine (wave 1 only).
    """
    import json
    from .models import TimelineItem as TLI

    repository = ControlPlaneRepository(session)

    # ── Plan enforcement: check mission limit ──
    db_user = repository.get_user(user.id)
    if db_user and not check_mission_limit(db_user):
        raise AppError.forbidden(
            "Vous avez atteint la limite de missions pour votre plan. "
            "Passez au plan Pro pour des missions illimitees."
        )

    # Auto-create a project for now (simplified flow)
    projects = repository.list_projects_for_user(user.id)
    if projects:
        project = projects[0]
    else:
        project = repository.create_project(
            user_id=user.id,
            project_id=f"project_{uuid4().hex[:10]}",
            name="Mon projet",
        )

    mission_id = f"mission_{uuid4().hex[:10]}"

    # Persist a minimal mission record so the resume endpoint can load it
    repository.upsert_mission(MissionReadModel(
        id=mission_id,
        project_id=project.id,
        flow_code=payload.flow_code,
        flow_label="Nouveau projet",
        title="Mission de cadrage",
        status="in_progress",
        summary="Mission en cours de cadrage.",
        next_step="Les agents travaillent...",
        intake_text=payload.intake_text.strip(),
        artifact_blocks=[],
        active_question=None,
        timeline=[
            TLI(id="wave1", label="Strategie", status="in_progress"),
            TLI(id="wave2", label="Business & Produit", status="not_started"),
            TLI(id="wave3", label="Tech & Design", status="not_started"),
            TLI(id="wave4", label="Consolidation", status="not_started"),
        ],
        dossier_ready=False,
    ))

    # Update project with active mission
    repository.update_project_after_mission(
        project_id=project.id,
        active_mission_id=mission_id,
        active_mission_status="in_progress",
        mission_delta=1,
    )

    # Increment mission counter for plan enforcement
    if db_user:
        increment_mission_count(db_user, session)

    async def event_generator():
        # Emit initial event with mission ID
        yield f"event: mission_created\ndata: {json.dumps({'mission_id': mission_id, 'project_id': project.id})}\n\n"

        collected_docs: dict[str, dict] = {}
        try:
            user_plan = db_user.plan if db_user else "free"
            async for event in runtime_client.start_mission_stream(
                RuntimeStartRequest(
                    mission_id=mission_id,
                    project_name=project.name,
                    intake_text=payload.intake_text.strip(),
                    flow_code=payload.flow_code,
                    plan=user_plan,
                    supporting_inputs=[],
                )
            ):
                if event["event"] == "document_updated":
                    d = event["data"]
                    collected_docs[d.get("doc_id", "")] = d
                elif event["event"] == "wave_completed":
                    # Persist docs after each wave so we accumulate across waves
                    _persist_dossier_from_docs(session, mission_id, collected_docs)
                elif event["event"] == "mission_completed":
                    _persist_dossier_from_docs(session, mission_id, collected_docs, is_final=True)
                yield f"event: {event['event']}\ndata: {json.dumps(event['data'], ensure_ascii=False)}\n\n"
        except Exception as exc:
            logger.error("SSE stream error: %s", exc, exc_info=True)
            yield f"event: error\ndata: {json.dumps({'error': str(exc)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/api/missions/{mission_id}/resume")
async def resume_mission_stream(
    mission_id: str,
    payload: AnswerQuestionRequest,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Resume a wave-based mission with user answer/validation and stream SSE events.

    Actions:
    - action="refine_wave": re-run current wave with user's additional context
    - action="next_wave": validate current wave and advance to next
    """
    import json

    repository = ControlPlaneRepository(session)
    mission = repository.get_mission_for_user(user.id, mission_id)
    if not mission:
        raise AppError.not_found("mission_not_found", "Mission not found.")

    project_id = mission.project_id

    db_user = repository.get_user(user.id)
    user_plan = db_user.plan if db_user else "free"

    async def event_generator():
        collected_docs: dict[str, dict] = {}
        try:
            async for event in runtime_client.resume_mission_stream(
                RuntimeResumeRequest(
                    mission_id=mission_id,
                    project_name="Mon projet",
                    intake_text=mission.intake_text,
                    answer_text=payload.answer_text.strip() if payload.answer_text else "",
                    flow_code=mission.flow_code,
                    plan=user_plan,
                    action=payload.action,
                )
            ):
                if event["event"] == "document_updated":
                    d = event["data"]
                    collected_docs[d.get("doc_id", "")] = d
                elif event["event"] == "wave_completed":
                    _persist_dossier_from_docs(session, mission_id, collected_docs)
                elif event["event"] == "mission_completed":
                    _persist_dossier_from_docs(session, mission_id, collected_docs, is_final=True)
                yield f"event: {event['event']}\ndata: {json.dumps(event['data'], ensure_ascii=False)}\n\n"
        except Exception as exc:
            logger.error("SSE resume stream error: %s", exc, exc_info=True)
            yield f"event: error\ndata: {json.dumps({'error': str(exc)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.get("/api/missions/{mission_id}", response_model=MissionReadModel)
async def get_mission(
    mission_id: str,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    mission = repository.get_mission_for_user(user.id, mission_id)
    if not mission:
        raise AppError.not_found("mission_not_found", "Mission not found.")
    return mission


@app.post("/api/missions/{mission_id}/answers", response_model=AnswerQuestionResponse)
async def answer_question(
    mission_id: str,
    payload: AnswerQuestionRequest,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    mission = repository.get_mission_for_user(user.id, mission_id)
    if not mission:
        raise AppError.not_found("mission_not_found", "Mission not found.")
    if mission.status != "waiting_user" or mission.active_question is None:
        raise AppError.conflict("mission_not_waiting_user", "La mission n'attend pas de reponse utilisateur.")

    project = repository.get_project_for_user(user.id, mission.project_id)
    if not project:
        raise AppError.not_found("project_not_found", "Project not found.")

    db_user = repository.get_user(user.id)
    user_plan = db_user.plan if db_user else "free"

    answered_questions = [q for q in mission.question_history if q.status == "answered"]
    cycle_number = len(answered_questions) + 1
    previous_answers = [q.answer_text for q in answered_questions if q.answer_text]

    run_id = repository.create_agent_run(
        mission_id=mission.id,
        run_id=f"run_{uuid4().hex[:10]}",
        kind="resume",
        idempotency_key=f"{mission.id}:resume:{uuid4().hex[:8]}",
    )
    try:
        runtime_response = await runtime_client.resume_mission(
            RuntimeResumeRequest(
                mission_id=mission.id,
                project_name=project.name,
                intake_text=mission.intake_text,
                answer_text=payload.answer_text.strip(),
                flow_code=mission.flow_code,
                plan=user_plan,
                cycle_number=cycle_number,
                previous_answers=previous_answers,
                supporting_inputs=to_runtime_inputs(mission.inputs),
            )
        )
    except Exception:
        repository.update_agent_run(run_id=run_id, status="failed")
        raise

    is_final = runtime_response.status == "completed"

    updated_mission = MissionReadModel(
        id=mission.id,
        project_id=mission.project_id,
        flow_code=mission.flow_code,
        flow_label=mission.flow_label,
        title=mission.title,
        status=runtime_response.status,
        summary=runtime_response.summary,
        next_step=runtime_response.next_step,
        intake_text=mission.intake_text,
        artifact_blocks=runtime_response.artifact_blocks,
        active_question=runtime_response.active_question,
        active_agents=runtime_response.active_agents,
        recent_messages=runtime_response.recent_messages,
        timeline=runtime_response.timeline,
        dossier_ready=is_final,
        updated_at=utc_now(),
    )
    repository.upsert_mission(updated_mission)
    repository.append_mission_input(
        mission_id=mission.id,
        kind="user_answer",
        source="user",
        content=payload.answer_text.strip(),
    )
    repository.answer_latest_question(mission_id=mission.id, answer_text=payload.answer_text.strip())
    if runtime_response.active_question:
        repository.upsert_question(mission_id=mission.id, question=runtime_response.active_question)
    repository.replace_mission_agents(mission_id=mission.id, agents=updated_mission.active_agents)
    repository.replace_messages(mission_id=mission.id, messages=updated_mission.recent_messages)
    repository.update_agent_run(run_id=run_id, status=updated_mission.status)

    dossier = None
    if is_final and runtime_response.dossier_title and runtime_response.dossier_summary:
        rendered = await renderer_client.render_markdown(
            RendererRequest(
                title=runtime_response.dossier_title,
                summary=runtime_response.dossier_summary,
                quality_label=runtime_response.quality_label,
                sections=runtime_response.dossier_sections,
            )
        )

        dossier = DossierReadModel(
            mission_id=mission.id,
            title=runtime_response.dossier_title,
            quality_label=runtime_response.quality_label or "",
            summary=runtime_response.dossier_summary,
            markdown=rendered.markdown,
            sections=runtime_response.dossier_sections,
            updated_at=utc_now(),
        )
        repository.upsert_dossier(dossier)

    repository.update_project_after_mission(
        project_id=project.id,
        active_mission_id=updated_mission.id,
        active_mission_status=updated_mission.status,
    )

    persisted_mission = repository.get_mission_for_user(user.id, updated_mission.id)
    if persisted_mission is None:
        raise AppError.internal(message="Mission mise a jour mais non relisible.")

    return AnswerQuestionResponse(mission=persisted_mission, dossier=dossier)


@app.post(
    "/api/missions/{mission_id}/inputs/upload",
    response_model=UploadMissionInputResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_mission_input(
    mission_id: str,
    file: UploadFile = File(...),
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    mission = repository.get_mission_for_user(user.id, mission_id)
    if not mission:
        raise AppError.not_found("mission_not_found", "Mission not found.")
    if not file.filename:
        raise AppError.validation("upload_filename_required", "Le nom du fichier est requis.")

    payload = await file.read()
    if not payload:
        raise AppError.validation("upload_empty", "Le fichier est vide.")
    if len(payload) > settings.max_upload_bytes:
        raise AppError.validation(
            "upload_too_large",
            "Le fichier depasse la taille maximale autorisee.",
            details={"max_bytes": settings.max_upload_bytes},
        )

    stored = upload_storage.store(
        mission_id=mission.id,
        filename=file.filename,
        media_type=file.content_type,
        data=payload,
    )

    openai_file_id: str | None = None
    vector_store_id: str | None = None
    if file_search_client is not None:
        try:
            indexed = file_search_client.index_file(
                mission_id=mission.id,
                file_data=payload,
                filename=file.filename,
            )
            openai_file_id = indexed.openai_file_id
            vector_store_id = indexed.vector_store_id
        except Exception:
            logger.warning(
                "File Search indexation failed for %s, upload proceeds without indexation",
                stored.input_id,
                exc_info=True,
            )

    input_item = repository.create_mission_input(
        mission_id=mission.id,
        kind="uploaded_file",
        source="user_upload",
        content=f"Fichier attache : {stored.display_name}",
        input_id=stored.input_id,
        display_name=stored.display_name,
        mime_type=stored.mime_type,
        byte_size=stored.byte_size,
        storage_path=stored.storage_path,
        preview_text=stored.preview_text,
        openai_file_id=openai_file_id,
        vector_store_id=vector_store_id,
    )

    persisted_mission = repository.get_mission_for_user(user.id, mission.id)
    if persisted_mission is None:
        raise AppError.internal(message="Mission mise a jour mais non relisible.")

    return UploadMissionInputResponse(mission=persisted_mission, input=input_item)


@app.get("/api/missions/{mission_id}/inputs/{input_id}/download")
async def download_mission_input(
    mission_id: str,
    input_id: str,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    record = repository.get_mission_input_for_user(user.id, mission_id, input_id)
    if record is None or not record.storage_path:
        raise AppError.not_found("input_not_found", "Input not found.")

    storage_path = record.storage_path

    if storage_path.startswith("s3://"):
        if isinstance(upload_storage, S3UploadStorage):
            presigned_url = upload_storage.generate_presigned_download_url(storage_path)
            if presigned_url is None:
                raise AppError.not_found("input_file_missing", "Input file not found on S3.")
            return JSONResponse(
                content={"download_url": presigned_url},
                headers={"Cache-Control": "no-store"},
            )
        raise AppError.internal(message="S3 storage not configured but file stored on S3.")

    path = Path(storage_path)
    if not path.exists():
        raise AppError.not_found("input_file_missing", "Input file not found.")

    return FileResponse(path, media_type=record.mime_type or "application/octet-stream", filename=record.display_name)


@app.post(
    "/api/missions/{mission_id}/inputs/search",
    response_model=SearchMissionInputsResponse,
)
async def search_mission_inputs(
    mission_id: str,
    payload: SearchMissionInputsRequest,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    mission = repository.get_mission_for_user(user.id, mission_id)
    if not mission:
        raise AppError.not_found("mission_not_found", "Mission not found.")

    if file_search_client is None:
        return SearchMissionInputsResponse(results=[])

    vector_store_id = repository.get_vector_store_id_for_mission(mission_id)
    if not vector_store_id:
        return SearchMissionInputsResponse(results=[])

    search_results = file_search_client.search(
        vector_store_id=vector_store_id,
        query=payload.query,
        max_results=payload.max_results,
    )

    citations: list[CitationItem] = []
    for result in search_results:
        citation = repository.create_citation(
            citation_id=f"cite_{uuid4().hex[:10]}",
            mission_id=mission_id,
            input_id=result.input_id,
            agent_code="search",
            excerpt=result.excerpt,
            locator=result.locator,
            score=result.score,
        )
        citation.display_name = result.filename
        citations.append(citation)

    return SearchMissionInputsResponse(results=citations)


@app.get("/api/missions/{mission_id}/citations", response_model=list[CitationItem])
async def list_mission_citations(
    mission_id: str,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    mission = repository.get_mission_for_user(user.id, mission_id)
    if not mission:
        raise AppError.not_found("mission_not_found", "Mission not found.")
    return repository.list_citations_for_mission(mission_id)


@app.get("/api/missions/{mission_id}/dossier", response_model=DossierReadModel)
async def get_dossier(
    mission_id: str,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    dossier = repository.get_dossier_for_user(user.id, mission_id)
    if not dossier:
        raise AppError.not_found("dossier_not_found", "Dossier not found.")
    return dossier


_PDF_CSS = """
@page { size: A4; margin: 2cm; }
body {
    font-family: Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #1a1a2e;
}
h1 { font-size: 18pt; color: #16213e; border-bottom: 2px solid #0f3460; padding-bottom: 6pt; margin-bottom: 12pt; }
h2 { font-size: 13pt; color: #0f3460; margin-top: 16pt; margin-bottom: 6pt; }
h3 { font-size: 11pt; color: #16213e; margin-top: 12pt; margin-bottom: 4pt; }
p { margin-bottom: 8pt; }
ul, ol { margin-bottom: 8pt; padding-left: 20pt; }
li { margin-bottom: 3pt; }
table { width: 100%; border-collapse: collapse; margin-bottom: 10pt; font-size: 9pt; }
th, td { border: 1px solid #ccc; padding: 4pt 6pt; text-align: left; vertical-align: top; }
th { background: #f0f4f8; font-weight: bold; color: #0f3460; }
code { font-family: Courier; font-size: 8pt; background: #f0f4f8; padding: 1pt 3pt; }
pre { background: #f0f4f8; padding: 6pt 10pt; font-size: 8pt; margin-bottom: 8pt; }
pre code { background: none; padding: 0; }
blockquote { border-left: 3pt solid #0f3460; margin: 8pt 0; padding: 4pt 10pt; color: #555; background: #f8f9fa; }
.footer { margin-top: 20pt; padding-top: 6pt; border-top: 1px solid #ddd; font-size: 7pt; color: #999; }
"""


def _md_to_pdf_bytes(title: str, content: str) -> bytes:
    """Convert a markdown document to PDF via HTML (supports tables, accents, formatting)."""
    import markdown as md_lib
    from xhtml2pdf import pisa

    # Convert markdown to HTML with GFM extensions
    html_body = md_lib.markdown(
        content,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
    )

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><style>{_PDF_CSS}</style></head>
<body>
<h1>{title}</h1>
{html_body}
<div class="footer">Genere par Cadris</div>
</body>
</html>"""

    buffer = io.BytesIO()
    pisa.CreatePDF(html, dest=buffer)
    buffer.seek(0)
    return buffer.getvalue()


@app.get("/api/missions/{mission_id}/dossier/pdf")
async def get_dossier_pdf(
    mission_id: str,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Download all docs as a ZIP of individual PDF files."""
    repository = ControlPlaneRepository(session)
    dossier = repository.get_dossier_for_user(user.id, mission_id)
    if not dossier:
        raise AppError.not_found("dossier_not_found", "Dossier not found.")

    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for section in dossier.sections:
            zip_path = DOC_ID_TO_ZIP_PATH.get(section.id)
            if zip_path:
                pdf_path = zip_path.replace(".md", ".pdf")
            else:
                pdf_path = f"{section.id}.pdf"
            try:
                pdf_bytes = _md_to_pdf_bytes(section.title, section.content)
                zf.writestr(pdf_path, pdf_bytes)
            except Exception as exc:
                logger.warning("PDF generation failed for %s: %s", section.id, exc)
                # Fallback: include as .md
                zf.writestr(pdf_path.replace(".pdf", ".md"), f"# {section.title}\n\n{section.content}")
    buffer.seek(0)

    repository.create_export(
        export_id=str(uuid4()),
        mission_id=mission_id,
        format="PDF",
    )

    return Response(
        content=buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="cadris-{mission_id}-pdf.zip"'},
    )


# ---------------------------------------------------------------------------
# Markdown export
# ---------------------------------------------------------------------------


@app.get("/api/missions/{mission_id}/dossier/markdown")
async def get_dossier_markdown(
    mission_id: str,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Download all docs as a ZIP of .md files, organized by folder."""
    repository = ControlPlaneRepository(session)
    dossier = repository.get_dossier_for_user(user.id, mission_id)
    if not dossier:
        raise AppError.not_found("dossier_not_found", "Dossier not found.")

    # Build zip of .md files — files at root, no wrapper folder
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for section in dossier.sections:
            zip_path = DOC_ID_TO_ZIP_PATH.get(section.id)
            # Only prepend title if content doesn't already start with a heading
            raw = section.content.strip()
            if raw.startswith("#"):
                content = raw
            else:
                content = f"# {section.title}\n\n{raw}"
            if zip_path:
                zf.writestr(zip_path, content)
            else:
                zf.writestr(f"{section.id}.md", content)
    buffer.seek(0)

    repository.create_export(
        export_id=str(uuid4()),
        mission_id=mission_id,
        format="Markdown",
    )

    return Response(
        content=buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="cadris-{mission_id}-md.zip"'},
    )


# ---------------------------------------------------------------------------
# Zip export (Claude Code ready)
# ---------------------------------------------------------------------------

import zipfile
import io

DOC_ID_TO_ZIP_PATH = {
    "implementation_plan": "CLAUDE.md",
    "user_guide": "user_guide.md",
    "executive_summary": "executive_summary.md",
    "vision_produit": "01-strategy/vision_produit.md",
    "problem_statement": "01-strategy/problem_statement.md",
    "icp_personas": "01-strategy/icp_personas.md",
    "value_proposition": "01-strategy/value_proposition.md",
    "business_model": "02-business/business_model.md",
    "pricing_strategy": "02-business/pricing_strategy.md",
    "market_analysis": "02-business/market_analysis.md",
    "scope_document": "03-product/scope_document.md",
    "mvp_definition": "03-product/mvp_definition.md",
    "prd": "03-product/prd.md",
    "user_stories": "03-product/user_stories.md",
    "feature_specs": "03-product/feature_specs.md",
    "architecture": "04-technical/architecture.md",
    "tech_stack": "04-technical/tech_stack.md",
    "data_model": "04-technical/data_model.md",
    "api_spec": "04-technical/api_spec.md",
    "nfr_security": "04-technical/nfr_security.md",
    "ux_principles": "05-design/ux_principles.md",
    "information_architecture": "05-design/information_architecture.md",
    "design_system": "05-design/design_system.md",
    "dossier_consolide": "06-synthesis/dossier_consolide.md",
}


@app.get("/api/missions/{mission_id}/dossier/zip")
async def get_dossier_zip(
    mission_id: str,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    dossier = repository.get_dossier_for_user(user.id, mission_id)
    if not dossier:
        raise AppError.not_found("dossier_not_found", "Dossier not found.")

    # Build zip in memory — files at root, no wrapper folder
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for section in dossier.sections:
            zip_path = DOC_ID_TO_ZIP_PATH.get(section.id)
            if zip_path:
                raw = section.content.strip()
                content = raw if raw.startswith("#") else f"# {section.title}\n\n{raw}"
                zf.writestr(zip_path, content)

    buffer.seek(0)

    repository.create_export(
        export_id=str(uuid4()),
        mission_id=mission_id,
        format="Zip",
    )

    return Response(
        content=buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="cadris-{mission_id}.zip"'},
    )


# ---------------------------------------------------------------------------
# Share links
# ---------------------------------------------------------------------------

import secrets


@app.post("/api/missions/{mission_id}/dossier/share", response_model=CreateShareLinkResponse)
async def create_share_link(
    mission_id: str,
    request: Request,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    dossier = repository.get_dossier_for_user(user.id, mission_id)
    if not dossier:
        raise AppError.not_found("dossier_not_found", "Dossier not found.")

    token = secrets.token_urlsafe(32)
    export = repository.create_export(
        export_id=str(uuid4()),
        mission_id=mission_id,
        format="ShareLink",
        token=token,
    )

    base_url = str(request.base_url).rstrip("/")
    share_url = f"{base_url}/api/shared/{token}"

    return CreateShareLinkResponse(export=export, share_url=share_url)


@app.get("/api/shared/{token}")
async def get_shared_dossier(
    token: str,
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    export_record = repository.get_export_by_token(token)
    if export_record is None:
        raise AppError.not_found("share_link_not_found", "Ce lien de partage est invalide ou a ete revoque.")

    from .records import DossierRecord
    from .models import DossierSection as DossierSectionModel
    import json

    dossier_record = session.get(DossierRecord, export_record.mission_id)
    if dossier_record is None:
        raise AppError.not_found("dossier_not_found", "Dossier not found.")

    sections = json.loads(dossier_record.sections_json)
    renderer_payload = RendererRequest(
        title=dossier_record.title,
        summary=dossier_record.summary,
        quality_label=dossier_record.quality_label,
        sections=[
            DossierSectionModel(**s) for s in sections
        ],
    )
    # Token lookup is via DB (get_export_by_token) — timing-safe against enumeration
    # because the DB query dominates response time regardless of token validity.
    html = build_shared_html(renderer_payload)
    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store"},
    )


@app.delete("/api/exports/{export_id}", response_model=ExportReadModel)
async def revoke_share_link(
    export_id: str,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    result = repository.revoke_export(export_id, user.id)
    if result is None:
        raise AppError.not_found("export_not_found", "Export not found.")
    return result


@app.get("/api/missions/{mission_id}/exports", response_model=list[ExportReadModel])
async def list_exports(
    mission_id: str,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    mission = repository.get_mission_for_user(user.id, mission_id)
    if not mission:
        raise AppError.not_found("mission_not_found", "Mission not found.")
    return repository.list_exports_for_mission(mission_id)


def build_shared_html(payload: RendererRequest) -> str:
    """Build a self-contained HTML page for shared dossier viewing."""
    import markdown as md_lib

    css = """
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; color: #1a1a2e; line-height: 1.6; }
    h1 { font-size: 1.5rem; color: #16213e; border-bottom: 2px solid #0f3460; padding-bottom: 0.5rem; }
    h2 { font-size: 1.1rem; color: #0f3460; margin-top: 1.5rem; }
    .quality-label { font-size: 0.9rem; color: #0f3460; padding: 0.25rem 0.5rem; background: #f0f4f8; border-left: 3px solid #0f3460; margin-bottom: 1rem; }
    .certainty-tag { display: inline-block; font-size: 0.7rem; padding: 0.1rem 0.4rem; border-radius: 3px; color: #fff; margin-left: 0.5rem; vertical-align: middle; }
    .certainty-solid { background: #2ecc71; }
    .certainty-to_confirm { background: #f39c12; }
    .certainty-unknown { background: #95a5a6; }
    .certainty-blocking { background: #e74c3c; }
    .footer { margin-top: 2rem; padding-top: 0.5rem; border-top: 1px solid #ddd; font-size: 0.75rem; color: #999; }
    """

    cert_labels = {"solid": "Solide", "to_confirm": "A confirmer", "unknown": "Inconnu", "blocking": "Bloquant"}

    parts = [f"<h1>{payload.title}</h1>"]
    if payload.quality_label:
        parts.append(f'<p class="quality-label"><strong>Statut qualite</strong> : {payload.quality_label}</p>')
    parts.append(f"<p>{payload.summary}</p>")
    for section in payload.sections:
        certainty_class = f"certainty-{section.certainty}"
        cert_label = cert_labels.get(section.certainty, section.certainty)
        tag = f'<span class="certainty-tag {certainty_class}">{cert_label}</span>'
        parts.append(f"<h2>{section.title} {tag}</h2>")
        parts.append(md_lib.markdown(section.content))
    parts.append('<div class="footer">Partage via Cadris — lien revocable par le proprietaire</div>')

    body = "\n".join(parts)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><title>{payload.title} — Cadris</title><style>{css}</style></head>
<body>{body}</body>
</html>"""


# ── Billing endpoints ──────────────────────────────────────────


@app.get("/api/billing/plans")
async def get_billing_plans(
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Return available plans with the user's current plan."""
    from .repository import ControlPlaneRepository
    repo = ControlPlaneRepository(session)
    db_user = repo.get_user(user.id)

    plans_out = []
    for plan_name, plan_info in PLANS.items():
        plans_out.append({
            "name": plan_name,
            "label": plan_info["label"],
            "missions_per_month": plan_info["missions_per_month"],
            "has_price": plan_info["price_id"] is not None,
        })

    return {
        "current_plan": db_user.plan if db_user else "free",
        "missions_this_month": db_user.missions_this_month if db_user else 0,
        "plans": plans_out,
    }


class CheckoutRequest(BaseModel):
    plan: str


@app.post("/api/billing/checkout")
async def billing_checkout(
    payload: CheckoutRequest,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Create a Stripe Checkout session for a plan upgrade."""
    from .repository import ControlPlaneRepository
    repo = ControlPlaneRepository(session)

    if not settings.stripe_secret_key:
        raise AppError.internal("stripe_not_configured", "Stripe n'est pas configure.")

    plan_info = PLANS.get(payload.plan)
    if not plan_info or not plan_info["price_id"]:
        raise AppError.validation("invalid_plan", f"Plan '{payload.plan}' invalide ou gratuit.")

    db_user = repo.get_user(user.id)
    if not db_user:
        raise AppError.not_found("user_not_found", "Utilisateur non trouve.")

    url = create_checkout_session(db_user, plan_info["price_id"], session)
    return {"url": url}


@app.post("/api/billing/portal")
async def billing_portal(
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Create a Stripe Customer Portal session."""
    from .repository import ControlPlaneRepository
    repo = ControlPlaneRepository(session)

    if not settings.stripe_secret_key:
        raise AppError.internal("stripe_not_configured", "Stripe n'est pas configure.")

    db_user = repo.get_user(user.id)
    if not db_user:
        raise AppError.not_found("user_not_found", "Utilisateur non trouve.")

    if not db_user.stripe_customer_id:
        raise AppError.validation("no_subscription", "Aucun abonnement actif.")

    url = create_portal_session(db_user, session)
    return {"url": url}


@app.post("/api/billing/webhook")
async def billing_webhook(request: Request, session: Session = Depends(get_session)):
    """Handle Stripe webhook events. No auth required (verified by signature)."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    try:
        result = handle_webhook(payload, sig_header, session)
        return result
    except ValueError as e:
        raise AppError.validation("webhook_error", str(e))
    except Exception as e:
        logger.error("webhook processing error: %s", e, exc_info=True)
        raise AppError.internal("webhook_error", "Webhook processing failed.")

