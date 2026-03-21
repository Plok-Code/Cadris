"""Uploads router — file upload and download for mission inputs."""
from __future__ import annotations

import logging
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session

from ..auth import AuthenticatedUser, require_user
from ..config import settings
from ..database import get_session
from ..dependencies import file_search_client, upload_storage
from ..errors import AppError
from ..models import UploadMissionInputResponse
from ..repository import ControlPlaneRepository
from ..uploads import S3UploadStorage

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/missions", tags=["uploads"])


@router.post(
    "/{mission_id}/inputs/upload",
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


@router.get("/{mission_id}/inputs/{input_id}/download")
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
