from __future__ import annotations

import re
from dataclasses import dataclass
from fastapi import Depends, Header
from sqlalchemy.orm import Session
from .database import get_session
from .errors import AppError
from .repository import ControlPlaneRepository

_VALID_USER_ID = re.compile(r"^[a-zA-Z0-9\-]{1,64}$")
_BASIC_EMAIL = re.compile(r"^[^@\s]{1,128}@[^@\s]{1,128}$")


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

    if not _VALID_USER_ID.match(x_cadris_user_id):
        raise AppError.unauthorized("Invalid x-cadris-user-id header.")

    email = x_cadris_user_email or f"{x_cadris_user_id}@dev.local"
    if x_cadris_user_email and not _BASIC_EMAIL.match(x_cadris_user_email):
        raise AppError.unauthorized("Invalid x-cadris-user-email header.")

    repository = ControlPlaneRepository(session)
    user = repository.ensure_user(user_id=x_cadris_user_id, email=email)
    return AuthenticatedUser(id=user.id, email=user.email)
