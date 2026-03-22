from __future__ import annotations

import logging

from sqlalchemy import select

from .base import utc_now
from ..errors import AppError
from ..records import PasswordResetTokenRecord, UserRecord

logger = logging.getLogger(__name__)


class UserRepoMixin:
    """User-related repository methods."""

    def get_user(self, user_id: str) -> UserRecord | None:
        return self.session.get(UserRecord, user_id)

    def ensure_user(self, user_id: str, email: str) -> UserRecord:
        # 1. Lookup by primary key — fast path
        user = self.session.get(UserRecord, user_id)
        if user is not None:
            return user

        # 2. Check if email is already taken by a DIFFERENT user_id.
        #    This prevents identity spoofing: an attacker sending a
        #    forged user_id with a victim's email must NOT get the
        #    victim's UserRecord back.
        existing = self.session.execute(
            select(UserRecord).where(UserRecord.email == email)
        ).scalar_one_or_none()
        if existing is not None:
            logger.warning(
                "ensure_user: user_id=%s tried to claim email=%s "
                "which belongs to user_id=%s — rejecting",
                user_id, email, existing.id,
            )
            raise AppError.unauthorized("Identity mismatch.")

        # 3. Brand new user — create
        user = UserRecord(id=user_id, email=email)
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_email(self, email: str) -> UserRecord | None:
        statement = select(UserRecord).where(UserRecord.email == email)
        return self.session.scalar(statement)

    def register_user(
        self, *, user_id: str, email: str, name: str, password_hash: str
    ) -> UserRecord:
        user = UserRecord(
            id=user_id,
            email=email,
            name=name or None,
            password_hash=password_hash,
            plan="free",
            created_at=utc_now(),
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_password_hash(self, *, user_id: str, password_hash: str) -> None:
        user = self.session.get(UserRecord, user_id)
        if user:
            user.password_hash = password_hash
            self.session.commit()

    def create_password_reset_token(
        self, *, token_id: str, user_id: str, token_hash: str, expires_at: str
    ) -> None:
        record = PasswordResetTokenRecord(
            id=token_id,
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            created_at=utc_now(),
        )
        self.session.add(record)
        self.session.commit()

    def get_valid_reset_token(self, token_hash: str) -> PasswordResetTokenRecord | None:
        statement = select(PasswordResetTokenRecord).where(
            PasswordResetTokenRecord.token_hash == token_hash,
            PasswordResetTokenRecord.used == 0,
        )
        return self.session.scalar(statement)

    def mark_reset_token_used(self, token_id: str) -> None:
        record = self.session.get(PasswordResetTokenRecord, token_id)
        if record:
            record.used = 1
            self.session.commit()
