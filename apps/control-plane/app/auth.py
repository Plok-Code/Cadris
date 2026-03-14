from __future__ import annotations

from dataclasses import dataclass
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from .database import get_session
from .errors import AppError
from .repository import ControlPlaneRepository


@dataclass(slots=True)
class AuthenticatedUser:
    id: str
    email: str


def require_user(
    x_cadris_user_id: str | None = Header(default=None),
    x_cadris_user_email: str | None = Header(default=None),
    session: Session = Depends(get_session),
) -> AuthenticatedUser:
    if not x_cadris_user_id:
        raise AppError.unauthorized("Missing x-cadris-user-id header.")

    email = x_cadris_user_email or f"{x_cadris_user_id}@dev.local"
    repository = ControlPlaneRepository(session)
    repository.ensure_user(user_id=x_cadris_user_id, email=email)
    return AuthenticatedUser(id=x_cadris_user_id, email=email)
