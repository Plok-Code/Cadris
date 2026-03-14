from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4
from fastapi import Depends, FastAPI, File, Request, Response, UploadFile, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.orm import Session
from .auth import AuthenticatedUser, require_user
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
    CreateMissionRequest,
    CreateMissionResponse,
    CreateProjectRequest,
    DossierReadModel,
    MissionReadModel,
    ProjectSummary,
    RendererRequest,
    RuntimeInputItem,
    RuntimeResumeRequest,
    RuntimeStartRequest,
    UploadMissionInputResponse,
    utc_now,
)
from .migrations import run_sql_migrations
from .renderer_client import RendererClient
from .repository import ControlPlaneRepository
from .runtime_client import RuntimeClient
from .uploads import LocalUploadStorage, S3UploadStorage

runtime_client = RuntimeClient()
renderer_client = RendererClient()

if settings.s3_bucket:
    upload_storage = S3UploadStorage(settings.s3_bucket, settings.s3_endpoint)
else:
    upload_storage = LocalUploadStorage(settings.uploads_dir)


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
    response: Response = await call_next(request)
    response.headers["x-request-id"] = request_id
    return response


app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


@app.get("/health")
async def healthcheck():
    return {"ok": True, "databaseUrl": settings.database_url}


@app.get("/api/projects", response_model=list[ProjectSummary])
async def list_projects(
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    return repository.list_projects_for_user(user.id)


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

    mission_id = f"mission_{uuid4().hex[:10]}"
    runtime_response = await runtime_client.start_mission(
        RuntimeStartRequest(
            mission_id=mission_id,
            project_name=project.name,
            intake_text=payload.intake_text.strip(),
            supporting_inputs=[],
        )
    )

    mission = MissionReadModel(
        id=mission_id,
        project_id=project.id,
        flow_code="demarrage",
        flow_label="Nouveau projet",
        title=f"Demarrage - {project.name}",
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
                supporting_inputs=to_runtime_inputs(mission.inputs),
            )
        )
    except Exception:
        repository.update_agent_run(run_id=run_id, status="failed")
        raise

    question = mission.active_question
    if question:
        question.status = "answered"
        question.answer_text = payload.answer_text.strip()

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
        active_question=None,
        active_agents=runtime_response.active_agents,
        recent_messages=runtime_response.recent_messages,
        timeline=runtime_response.timeline,
        dossier_ready=True,
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
    repository.replace_mission_agents(mission_id=mission.id, agents=updated_mission.active_agents)
    repository.replace_messages(mission_id=mission.id, messages=updated_mission.recent_messages)
    repository.update_agent_run(run_id=run_id, status=updated_mission.status)

    rendered = await renderer_client.render_markdown(
        RendererRequest(
            title=runtime_response.dossier_title,
            summary=runtime_response.dossier_summary,
            sections=runtime_response.dossier_sections,
        )
    )

    dossier = DossierReadModel(
        mission_id=mission.id,
        title=runtime_response.dossier_title,
        quality_label=runtime_response.quality_label,
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

    path = Path(record.storage_path)
    if not path.exists():
        raise AppError.not_found("input_file_missing", "Input file not found.")

    return FileResponse(path, media_type=record.mime_type or "application/octet-stream", filename=record.display_name)


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


@app.get("/api/missions/{mission_id}/dossier/pdf")
async def get_dossier_pdf(
    mission_id: str,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    dossier = repository.get_dossier_for_user(user.id, mission_id)
    if not dossier:
        raise AppError.not_found("dossier_not_found", "Dossier not found.")

    from .models import DossierSection as DossierSectionModel

    pdf_bytes = await renderer_client.render_pdf(
        RendererRequest(
            title=dossier.title,
            summary=dossier.summary,
            sections=[
                DossierSectionModel(
                    id=s.id, title=s.title, content=s.content, certainty=s.certainty
                )
                for s in dossier.sections
            ],
        )
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="dossier-{mission_id}.pdf"'},
    )

