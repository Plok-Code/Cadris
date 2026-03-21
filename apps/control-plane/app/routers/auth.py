"""Authentication router — register, login, forgot/reset password."""
from __future__ import annotations

import hashlib
import logging
import re
import secrets
import time
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from html import escape
from uuid import uuid4

import bcrypt
import httpx
from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_session
from ..errors import AppError
from ..models import (
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    ResetPasswordRequest,
)
from ..repository import ControlPlaneRepository

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Rate limiter (in-memory, auth-specific)
_rate_limits: dict[str, list[float]] = defaultdict(list)
_RATE_WINDOW = 60  # seconds
_RATE_MAX = 5


def _check_rate_limit(key: str) -> bool:
    now = time.time()
    bucket = _rate_limits[key]
    _rate_limits[key] = [t for t in bucket if now - t < _RATE_WINDOW]
    if len(_rate_limits[key]) >= _RATE_MAX:
        return False
    _rate_limits[key].append(now)
    return True


_EMAIL_RE = re.compile(r"^[^@\s]{1,128}@[^@\s]{1,128}\.[^@\s]{1,64}$")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def auth_register(
    payload: RegisterRequest,
    session: Session = Depends(get_session),
):
    email = payload.email.strip().lower()
    if not _EMAIL_RE.match(email):
        raise AppError.validation("invalid_email", "Adresse email invalide.")
    if len(payload.password) < 8:
        raise AppError.validation("weak_password", "Le mot de passe doit contenir au moins 8 caracteres.")

    repo = ControlPlaneRepository(session)
    if repo.get_user_by_email(email):
        raise AppError.conflict("email_taken", "Un compte existe deja avec cet email.")

    user_id = re.sub(r"[^a-zA-Z0-9]", "-", email)[:64]
    password_hash = bcrypt.hashpw(payload.password.encode(), bcrypt.gensalt()).decode()
    user = repo.register_user(
        user_id=user_id, email=email, name=payload.name.strip(), password_hash=password_hash
    )
    return {"id": user.id, "email": user.email, "name": user.name}


@router.post("/login")
async def auth_login(
    payload: LoginRequest,
    request: Request,
    session: Session = Depends(get_session),
):
    client_ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(f"login:{client_ip}"):
        raise AppError.validation("rate_limited", "Trop de tentatives. Reessayez dans une minute.")

    repo = ControlPlaneRepository(session)
    user = repo.get_user_by_email(payload.email.strip().lower())
    if not user or not user.password_hash:
        raise AppError.unauthorized("Email ou mot de passe incorrect.")
    if not bcrypt.checkpw(payload.password.encode(), user.password_hash.encode()):
        raise AppError.unauthorized("Email ou mot de passe incorrect.")

    return {"id": user.id, "email": user.email, "name": user.name}


@router.post("/forgot-password")
async def auth_forgot_password(
    payload: ForgotPasswordRequest,
    session: Session = Depends(get_session),
):
    email = payload.email.strip().lower()
    if not _check_rate_limit(f"forgot:{email}"):
        raise AppError.validation("rate_limited", "Trop de tentatives. Reessayez dans une minute.")

    repo = ControlPlaneRepository(session)
    user = repo.get_user_by_email(email)

    msg = "Si un compte existe avec cet email, un lien de reinitialisation a ete envoye."

    if user and user.password_hash and settings.resend_api_key:
        token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(token.encode()).hexdigest()
        expires_at = (datetime.now(UTC) + timedelta(hours=1)).isoformat()
        repo.create_password_reset_token(
            token_id=str(uuid4()), user_id=user.id,
            token_hash=token_hash, expires_at=expires_at,
        )
        reset_url = f"{settings.frontend_url}/reset-password?token={token}"
        try:
            async with httpx.AsyncClient() as client:
                await client.post(
                    "https://api.resend.com/emails",
                    headers={"Authorization": f"Bearer {settings.resend_api_key}"},
                    json={
                        "from": "Cadris <onboarding@resend.dev>",
                        "to": [email],
                        "subject": "Reinitialisation de votre mot de passe Cadris",
                        "html": (
                            f"<p>Bonjour,</p>"
                            f"<p>Cliquez sur le lien ci-dessous pour reinitialiser votre mot de passe :</p>"
                            f'<p><a href="{escape(reset_url)}">Reinitialiser mon mot de passe</a></p>'
                            f"<p>Ce lien expire dans 1 heure.</p>"
                            f"<p>Si vous n'avez pas demande cette reinitialisation, ignorez cet email.</p>"
                        ),
                    },
                )
        except Exception:
            logger.exception("Failed to send password reset email")

    return {"message": msg}


@router.post("/reset-password")
async def auth_reset_password(
    payload: ResetPasswordRequest,
    request: Request,
    session: Session = Depends(get_session),
):
    client_ip = request.client.host if request.client else "unknown"
    if not _check_rate_limit(f"reset:{client_ip}"):
        raise AppError.validation("rate_limited", "Trop de tentatives. Reessayez dans une minute.")

    if len(payload.password) < 8:
        raise AppError.validation("weak_password", "Le mot de passe doit contenir au moins 8 caracteres.")

    token_hash = hashlib.sha256(payload.token.encode()).hexdigest()
    repo = ControlPlaneRepository(session)
    record = repo.get_valid_reset_token(token_hash)

    if not record:
        raise AppError.validation("invalid_token", "Lien invalide ou expire.")

    if datetime.fromisoformat(record.expires_at) < datetime.now(UTC):
        raise AppError.validation("expired_token", "Ce lien a expire. Demandez un nouveau lien.")

    password_hash = bcrypt.hashpw(payload.password.encode(), bcrypt.gensalt()).decode()
    repo.update_password_hash(user_id=record.user_id, password_hash=password_hash)
    repo.mark_reset_token_used(record.id)

    return {"message": "Mot de passe reinitialise avec succes."}
