from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Category = Literal["validation", "domain", "auth", "integration", "internal"]


@dataclass(slots=True)
class AppError(Exception):
    code: str
    category: Category
    message: str
    http_status: int
    retryable: bool = False
    details: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def validation(cls, code: str, message: str, *, details: dict[str, Any] | None = None) -> "AppError":
        return cls(code=code, category="validation", message=message, http_status=422, details=details or {})

    @classmethod
    def unauthorized(cls, message: str = "Authentification requise.") -> "AppError":
        return cls(code="unauthorized", category="auth", message=message, http_status=401)

    @classmethod
    def forbidden(cls, message: str = "Action interdite.") -> "AppError":
        return cls(code="forbidden", category="auth", message=message, http_status=403)

    @classmethod
    def not_found(cls, code: str, message: str) -> "AppError":
        return cls(code=code, category="domain", message=message, http_status=404)

    @classmethod
    def conflict(cls, code: str, message: str) -> "AppError":
        return cls(code=code, category="domain", message=message, http_status=409)

    @classmethod
    def integration(
        cls,
        code: str,
        message: str,
        *,
        retryable: bool = True,
        http_status: int = 503,
        details: dict[str, Any] | None = None,
    ) -> "AppError":
        return cls(
            code=code,
            category="integration",
            message=message,
            http_status=http_status,
            retryable=retryable,
            details=details or {},
        )

    @classmethod
    def internal(cls, code: str = "internal_error", message: str = "Erreur interne.") -> "AppError":
        return cls(code=code, category="internal", message=message, http_status=500)
