from __future__ import annotations

import hashlib
import hmac
import re
import time
from dataclasses import dataclass
from fastapi import Depends, Header, Request
from sqlalchemy.orm import Session
from .config import settings
from .database import get_session
from .errors import AppError
from .repository import ControlPlaneRepository

_VALID_USER_ID = re.compile(r"^[a-zA-Z0-9\-]{1,64}$")
_BASIC_EMAIL = re.compile(r"^[^@\s]{1,128}@[^@\s]{1,128}$")


@dataclass(slots=True)
class AuthenticatedUser:
    id: str
    email: str


def build_trusted_proxy_signature(
    *,
    secret: str,
    timestamp: str,
    method: str,
    path: str,
    user_id: str,
    user_email: str,
) -> str:
    payload = "\n".join(
        [timestamp, method.upper(), path, user_id, user_email]
    ).encode("utf-8")
    return hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()


def _verify_trusted_proxy_headers(
    *,
    request: Request,
    user_id: str,
    user_email: str,
    timestamp: str | None,
    signature: str | None,
) -> None:
    secret = settings.trusted_proxy_secret
    if not secret:
        if settings.allow_unsigned_requests:
            return  # Dev-only: explicit opt-in to skip signature verification
        raise AppError.unauthorized(
            "Proxy signature not configured. "
            "Set CONTROL_PLANE_TRUSTED_PROXY_SECRET or "
            "CADRIS_ALLOW_UNSIGNED_REQUESTS=true for dev."
        )

    if not timestamp or not signature:
        raise AppError.unauthorized("Missing trusted proxy signature.")

    try:
        issued_at = int(timestamp)
    except ValueError as exc:
        raise AppError.unauthorized("Invalid trusted proxy timestamp.") from exc

    now = int(time.time())
    if abs(now - issued_at) > settings.trusted_proxy_max_skew_seconds:
        raise AppError.unauthorized("Expired trusted proxy signature.")

    expected = build_trusted_proxy_signature(
        secret=secret,
        timestamp=timestamp,
        method=request.method,
        path=request.url.path,
        user_id=user_id,
        user_email=user_email,
    )
    if not hmac.compare_digest(expected, signature):
        raise AppError.unauthorized("Invalid trusted proxy signature.")


def require_user(
    request: Request,
    x_cadris_user_id: str | None = Header(default=None),
    x_cadris_user_email: str | None = Header(default=None),
    x_cadris_auth_timestamp: str | None = Header(default=None),
    x_cadris_auth_signature: str | None = Header(default=None),
    session: Session = Depends(get_session),
) -> AuthenticatedUser:
    if not x_cadris_user_id:
        raise AppError.unauthorized("Missing x-cadris-user-id header.")

    if not _VALID_USER_ID.match(x_cadris_user_id):
        raise AppError.unauthorized("Invalid x-cadris-user-id header.")

    signed_email = x_cadris_user_email or ""
    if x_cadris_user_email and not _BASIC_EMAIL.match(x_cadris_user_email):
        raise AppError.unauthorized("Invalid x-cadris-user-email header.")

    _verify_trusted_proxy_headers(
        request=request,
        user_id=x_cadris_user_id,
        user_email=signed_email,
        timestamp=x_cadris_auth_timestamp,
        signature=x_cadris_auth_signature,
    )

    email = x_cadris_user_email or f"{x_cadris_user_id}@dev.local"

    repository = ControlPlaneRepository(session)
    user = repository.ensure_user(user_id=x_cadris_user_id, email=email)
    return AuthenticatedUser(id=user.id, email=user.email)
