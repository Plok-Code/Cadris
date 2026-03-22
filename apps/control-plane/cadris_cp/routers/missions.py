"""Missions router — CRUD, run stream, resume stream, state, validate-docs, answers, logo."""
from __future__ import annotations

import json
import logging
from uuid import uuid4

import httpx
import openai
from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..auth import AuthenticatedUser, require_user
from ..billing import check_mission_limit, increment_mission_count
from ..database import get_session
from ..dependencies import file_search_client, renderer_client, runtime_client, upload_storage
from ..errors import AppError
from ..models import (
    AnswerQuestionRequest,
    AnswerQuestionResponse,
    CreateMissionRequest,
    CreateMissionResponse,
    DossierReadModel,
    FLOW_LABELS,
    LogoGenerateRequest,
    MissionReadModel,
    MissionStateResponse,
    ProjectSummary,
    RendererRequest,
    RuntimeResumeRequest,
    RuntimeStartRequest,
    TimelineItem as TLI,
    ValidateDocsRequest,
    utc_now,
)
from ..repository import ControlPlaneRepository
from ..services.mission_service import save_sse_state, to_runtime_inputs

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/missions", tags=["missions"])


async def _close_async_iterator(stream) -> None:
    close = getattr(stream, "aclose", None)
    if close is not None:
        await close()


async def _prime_runtime_stream(stream):
    try:
        first_event = await anext(stream)
    except StopAsyncIteration as exc:
        raise AppError.integration(
            "runtime_empty_stream",
            "Le runtime n'a produit aucun evenement de demarrage.",
            http_status=502,
        ) from exc

    if first_event.get("event") == "error":
        await _close_async_iterator(stream)
        data = first_event.get("data", {})
        message = data.get("error") if isinstance(data, dict) else None
        raise AppError.integration(
            "runtime_stream_error",
            str(message or "Le runtime a echoue avant de demarrer la mission."),
            http_status=502,
        )

    return first_event


@router.get("", response_model=None)
async def list_missions(
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """List all missions for the authenticated user (most recent first)."""
    repository = ControlPlaneRepository(session)
    return repository.list_missions_for_user(user.id)


@router.delete("/{mission_id}", status_code=204)
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

    vs_id = repository.get_vector_store_id_for_mission(mission_id)
    if vs_id and file_search_client:
        file_search_client.delete_vector_store(vs_id)
    if upload_storage:
        upload_storage.delete_mission_files(mission_id)
    await runtime_client.cleanup_mission(mission_id)

    repository.delete_mission(mission_id)
    return Response(status_code=204)


@router.post("/run")
async def run_mission_stream(
    payload: CreateMissionRequest,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Launch a collaborative mission and stream SSE events to the client."""
    repository = ControlPlaneRepository(session)

    db_user = repository.get_user(user.id)
    if db_user and not check_mission_limit(db_user, session):
        raise AppError.forbidden(
            "Vous avez atteint la limite de missions pour votre plan. "
            "Passez au plan superieur pour plus de missions."
        )

    projects = repository.list_projects_for_user(user.id)
    project = projects[0] if projects else None
    project_name = project.name if project else "Mon projet"

    mission_id = f"mission_{uuid4().hex[:10]}"
    user_plan = db_user.plan if db_user else "free"
    stream = runtime_client.start_mission_stream(
        RuntimeStartRequest(
            mission_id=mission_id,
            project_name=project_name,
            intake_text=payload.intake_text.strip(),
            flow_code=payload.flow_code,
            plan=user_plan,
            template_id=payload.template_id,
            supporting_inputs=[],
        )
    )
    first_event = await _prime_runtime_stream(stream)

    if project is None:
        project = repository.create_project(
            user_id=user.id,
            project_id=f"project_{uuid4().hex[:10]}",
            name=project_name,
        )

    flow_label = FLOW_LABELS.get(payload.flow_code, payload.flow_code)
    mission_title = f"{flow_label} - {project_name}"

    repository.upsert_mission(MissionReadModel(
        id=mission_id,
        project_id=project.id,
        flow_code=payload.flow_code,
        flow_label=flow_label,
        title=mission_title,
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

    repository.update_project_after_mission(
        project_id=project.id,
        active_mission_id=mission_id,
        active_mission_status="in_progress",
        mission_delta=1,
    )

    if db_user:
        increment_mission_count(db_user, session)

    async def event_generator():
        yield f"event: mission_created\ndata: {json.dumps({'mission_id': mission_id, 'project_id': project.id})}\n\n"

        collected_docs: dict[str, dict] = {}
        try:
            save_sse_state(session, mission_id, first_event, collected_docs, repository)
            yield f"event: {first_event['event']}\ndata: {json.dumps(first_event['data'], ensure_ascii=False)}\n\n"
            async for event in stream:
                save_sse_state(session, mission_id, event, collected_docs, repository)
                yield f"event: {event['event']}\ndata: {json.dumps(event['data'], ensure_ascii=False)}\n\n"
        except Exception as exc:  # noqa: BLE001 — SSE must never drop silently
            logger.error("SSE stream error: %s", exc, exc_info=True)
            yield f"event: error\ndata: {json.dumps({'error': 'Une erreur interne est survenue.'})}\n\n"
        finally:
            await _close_async_iterator(stream)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/{mission_id}/resume")
async def resume_mission_stream(
    mission_id: str,
    payload: AnswerQuestionRequest,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Resume a wave-based mission with user answer/validation and stream SSE events."""
    repository = ControlPlaneRepository(session)
    mission = repository.get_mission_for_user(user.id, mission_id)
    if not mission:
        raise AppError.not_found("mission_not_found", "Mission not found.")

    mission_state = repository.get_mission_state(user.id, mission_id)
    project = repository.get_project_for_user(user.id, mission.project_id)
    if not project:
        raise AppError.not_found("project_not_found", "Project not found.")

    db_user = repository.get_user(user.id)
    user_plan = db_user.plan if db_user else "free"
    runtime_action = payload.action
    if (
        runtime_action == "next_wave"
        and mission_state
        and mission_state.get("phase") == "wave_running"
        and int(mission_state.get("currentWave", 0) or 0) > 0
    ):
        runtime_action = "refine_wave"

    if payload.action == "answer_qualification" and payload.answer_text:
        try:
            answers = json.loads(payload.answer_text) if payload.answer_text.startswith("{") else {}
        except (json.JSONDecodeError, TypeError):
            answers = {}
        if answers:
            repository.save_qualification_answers(mission_id, answers)
        repository.update_mission_phase(mission_id, "wave_running")

    async def event_generator():
        collected_docs: dict[str, dict] = {}
        try:
            async for event in runtime_client.resume_mission_stream(
                RuntimeResumeRequest(
                    mission_id=mission_id,
                    project_name=project.name,
                    intake_text=mission.intake_text,
                    answer_text=payload.answer_text.strip() if payload.answer_text else "",
                    flow_code=mission.flow_code,
                    plan=user_plan,
                    action=runtime_action,
                )
            ):
                save_sse_state(session, mission_id, event, collected_docs, repository)
                yield f"event: {event['event']}\ndata: {json.dumps(event['data'], ensure_ascii=False)}\n\n"
        except Exception as exc:  # noqa: BLE001 — SSE must never drop silently
            logger.error("SSE resume stream error: %s", exc, exc_info=True)
            yield f"event: error\ndata: {json.dumps({'error': 'Une erreur interne est survenue.'})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/{mission_id}", response_model=MissionReadModel)
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


@router.get("/{mission_id}/state", response_model=MissionStateResponse)
async def get_mission_state(
    mission_id: str,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Return full resumable state for a mission."""
    repository = ControlPlaneRepository(session)
    state = repository.get_mission_state(user.id, mission_id)
    if not state:
        raise AppError.not_found("mission_not_found", "Mission not found.")
    return state


@router.post("/{mission_id}/validate-docs")
async def validate_docs(
    mission_id: str,
    payload: ValidateDocsRequest,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Persist doc validation/correction status during doc_review phase."""
    repository = ControlPlaneRepository(session)
    mission = repository.get_mission_for_user(user.id, mission_id)
    if not mission:
        raise AppError.not_found("mission_not_found", "Mission not found.")
    repository.update_dossier_doc_status(
        mission_id,
        validated_ids=payload.validated_doc_ids,
        corrections=payload.corrections,
    )
    repository.update_mission_phase(mission_id, "doc_review")
    return {"ok": True}


@router.post("/{mission_id}/answers", response_model=AnswerQuestionResponse)
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
    except Exception:  # noqa: BLE001 — mark agent run failed then re-raise
        repository.update_agent_run(run_id=run_id, status="failed")
        raise

    is_final = runtime_response.status == "completed"

    # ── Render dossier BEFORE marking mission as completed ──
    # This ensures we never have status=completed + dossier_ready=true
    # without an actual dossier in the DB (atomic invariant).
    dossier = None
    if is_final and runtime_response.dossier_title and runtime_response.dossier_summary:
        try:
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
        except Exception:  # noqa: BLE001 — renderer failure must not mark mission complete
            logger.error("Renderer failed for mission %s, marking as failed", mission.id, exc_info=True)
            is_final = False
            runtime_response.status = "failed"
            runtime_response.next_step = "Le rendu du dossier a echoue. Relancez la mission."

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
        dossier_ready=is_final and dossier is not None,
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

    # Persist dossier ONLY after mission is persisted with matching state
    if dossier is not None:
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


@router.post("/{mission_id}/logo")
async def generate_mission_logo(
    mission_id: str,
    body: LogoGenerateRequest,
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    """Generate logo variants for a mission (Expert plan only)."""
    from ..config import settings

    repository = ControlPlaneRepository(session)

    mission = repository.get_mission_for_user(user.id, mission_id)
    if not mission:
        raise AppError.not_found("mission_not_found", "Mission non trouvee.")

    db_user = repository.get_user(user.id)
    if not db_user or db_user.plan not in ("expert",):
        raise AppError.forbidden(
            "La generation de logo necessite le plan Expert.",
            code="plan_required",
        )

    from openai import AsyncOpenAI

    openai_key = settings.openai_api_key if hasattr(settings, "openai_api_key") else None
    if not openai_key:
        openai_key = __import__("os").environ.get("OPENAI_API_KEY")
    if not openai_key:
        raise AppError.internal("openai_not_configured", "OpenAI n'est pas configure.")

    client = AsyncOpenAI(api_key=openai_key)
    brief = body.project_brief[:200]
    num = min(max(body.num_variants, 1), 4)

    styles = [
        ("modern_minimalist", "Clean, modern, minimalist logo"),
        ("geometric_abstract", "Abstract geometric shapes, bold colors"),
        ("professional_corporate", "Professional, corporate, trustworthy"),
        ("playful_startup", "Playful, vibrant, startup-friendly"),
    ][:num]

    logos = []
    for style_key, style_desc in styles:
        prompt = (
            f"Create a professional logo for '{body.project_name}'. "
            f"Project: {brief}. Style: {style_desc}. "
            "The logo should work on white and dark backgrounds. "
            "Square format, centered."
        )
        try:
            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image = response.data[0]
            logos.append({
                "url": image.url,
                "revised_prompt": image.revised_prompt or prompt,
                "style": style_key,
            })
        except (openai.OpenAIError, httpx.HTTPError) as exc:
            logger.warning("Logo generation failed for style '%s': %s", style_key, exc)

    return {"logos": logos, "count": len(logos)}
