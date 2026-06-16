"""Shared dossier & export management router."""
from __future__ import annotations

import hashlib
import json
import logging
import secrets
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session

from ..auth import AuthenticatedUser, require_user
from ..config import settings
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

logger = logging.getLogger(__name__)

router = APIRouter(tags=["shared"])

# Share links expire after 30 days by default.
_SHARE_LINK_TTL_DAYS = 30


def _hash_token(token: str) -> str:
    """SHA-256 hash of a share token — only the hash is persisted."""
    return hashlib.sha256(token.encode()).hexdigest()


def _public_base_url(request: Request) -> str:
    origin = (request.headers.get("origin") or "").rstrip("/")
    if origin and origin in settings.allowed_origins:
        return origin
    return settings.frontend_url.rstrip("/")


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

    # 32 bytes (256 bits) of CSPRNG entropy — collisions are practically
    # impossible; only the hash is stored, and a UNIQUE index on token_hash
    # (migration 015) turns any hypothetical collision into a hard failure.
    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)
    expires_at = (datetime.now(UTC) + timedelta(days=_SHARE_LINK_TTL_DAYS)).isoformat()

    export = repository.create_export(
        export_id=str(uuid4()),
        mission_id=mission_id,
        format="ShareLink",
        token_hash=token_hash,
        expires_at=expires_at,
    )

    share_url = f"{_public_base_url(request)}/api/shared/{token}"

    return CreateShareLinkResponse(export=export, share_url=share_url)


@router.get("/api/shared/{token}")
async def get_shared_dossier(
    token: str,
    request: Request,
    session: Session = Depends(get_session),
):
    # Rate limit by IP to prevent brute-force of share tokens
    from ..rate_limit import check_rate_limit
    client_ip = request.client.host if request.client else "unknown"
    if not check_rate_limit(f"shared:{client_ip}", max_requests=10, window_seconds=60):
        raise AppError.validation("rate_limited", "Trop de tentatives. Reessayez dans une minute.")
    repository = ControlPlaneRepository(session)
    token_hash = _hash_token(token)
    export_record = repository.get_export_by_token_hash(token_hash)
    if export_record is None:
        raise AppError.not_found("share_link_not_found", "Ce lien de partage est invalide ou a ete revoque.")

    # Check expiration — fail closed on a malformed timestamp (treat as
    # expired) rather than serving a link forever; log so the bad row can
    # be migrated.
    if export_record.expires_at:
        try:
            is_expired = datetime.fromisoformat(export_record.expires_at) < datetime.now(UTC)
        except ValueError:
            logger.warning(
                "malformed expires_at for export %s: %r",
                export_record.id,
                export_record.expires_at,
            )
            is_expired = True
        if is_expired:
            raise AppError.not_found("share_link_expired", "Ce lien de partage a expire.")

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
