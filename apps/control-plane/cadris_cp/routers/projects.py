"""Projects router."""
from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..auth import AuthenticatedUser, require_user
from ..billing import check_and_increment_mission
from ..database import get_session
from ..dependencies import runtime_client
from ..errors import AppError
from ..models import (
    CreateMissionRequest,
    CreateMissionResponse,
    CreateProjectRequest,
    FLOW_LABELS,
    MissionReadModel,
    ProjectSummary,
    RuntimeStartRequest,
    utc_now,
)
from ..repository import ControlPlaneRepository

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=list[ProjectSummary])
async def list_projects(
    user: AuthenticatedUser = Depends(require_user),
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    return repository.list_projects_for_user(user.id)


@router.post("", response_model=ProjectSummary, status_code=status.HTTP_201_CREATED)
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


@router.post(
    "/{project_id}/missions",
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

    flow_code = payload.flow_code
    flow_label = FLOW_LABELS.get(flow_code, flow_code)

    db_user = repository.get_user(user.id)
    user_plan = db_user.plan if db_user else "free"

    if db_user and not check_and_increment_mission(db_user, session):
        raise AppError.forbidden(
            "Vous avez atteint la limite de missions pour votre plan. "
            "Passez au plan superieur pour plus de missions."
        )

    mission_id = f"mission_{uuid4().hex[:10]}"

    # Wrap runtime call + DB writes in try/except to rollback quota on failure.
    # Without this, a network error or DB failure after billing would cause
    # the user to permanently lose a mission credit for nothing.
    try:
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
            user_id=user.id,
            project_id=project.id,
            active_mission_id=mission.id,
            active_mission_status=mission.status,
            mission_delta=1,
        )
    except Exception:
        # Quota rollback — user must not lose a credit for a backend failure
        if db_user:
            db_user.missions_this_month = max(0, db_user.missions_this_month - 1)
            try:
                session.commit()
            except Exception:  # noqa: BLE001 — best-effort rollback
                session.rollback()
        raise

    persisted_mission = repository.get_mission_for_user(user.id, mission.id)
    if persisted_mission is None:
        raise AppError.internal(message="Mission creee mais non relisible.")

    return CreateMissionResponse(project=updated_project, mission=persisted_mission)
