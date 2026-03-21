"""Shared dossier & export management router."""
from __future__ import annotations

import json
import secrets
from uuid import uuid4

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from ..auth import AuthenticatedUser, require_user
from ..database import get_session
from ..errors import AppError
from ..models import (
    CreateShareLinkResponse,
    DossierSection as DossierSectionModel,
    ExportReadModel,
    RendererRequest,
)
from ..repository import ControlPlaneRepository
from ..services.share_service import build_shared_html

router = APIRouter(tags=["shared"])


@router.post("/api/missions/{mission_id}/dossier/share", response_model=CreateShareLinkResponse)
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


@router.get("/api/shared/{token}")
async def get_shared_dossier(
    token: str,
    session: Session = Depends(get_session),
):
    repository = ControlPlaneRepository(session)
    export_record = repository.get_export_by_token(token)
    if export_record is None:
        raise AppError.not_found("share_link_not_found", "Ce lien de partage est invalide ou a ete revoque.")

    from ..records import DossierRecord

    dossier_record = session.get(DossierRecord, export_record.mission_id)
    if dossier_record is None:
        raise AppError.not_found("dossier_not_found", "Dossier not found.")

    sections = json.loads(dossier_record.sections_json)
    renderer_payload = RendererRequest(
        title=dossier_record.title,
        summary=dossier_record.summary,
        quality_label=dossier_record.quality_label,
        sections=[DossierSectionModel(**s) for s in sections],
    )
    html = build_shared_html(renderer_payload)
    return Response(
        content=html,
        media_type="text/html; charset=utf-8",
        headers={"Cache-Control": "no-store"},
    )


@router.delete("/api/exports/{export_id}", response_model=ExportReadModel)
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


@router.get("/api/missions/{mission_id}/exports", response_model=list[ExportReadModel])
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
