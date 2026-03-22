from __future__ import annotations

import logging
from uuid import uuid4

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .errors import AppError
from .models import ApiErrorEnvelope
from .request_context import get_request_id, set_request_id

logger = logging.getLogger(__name__)


def ensure_request_id(request: Request) -> str:
    header_value = request.headers.get("x-request-id")
    request_id = header_value or f"req_{uuid4().hex[:16]}"
    request.state.request_id = request_id
    set_request_id(request_id)
    return request_id


async def app_error_handler(_: Request, error: AppError) -> JSONResponse:
    envelope = ApiErrorEnvelope(
        code=error.code,
        category=error.category,
        retryable=error.retryable,
        message=error.message,
        request_id=get_request_id(),
        details=error.details or None,
    )
    return JSONResponse(status_code=error.http_status, content=envelope.model_dump(mode="json", by_alias=True))


async def http_exception_handler(_: Request, error: HTTPException) -> JSONResponse:
    status = error.status_code
    code = {
        401: "unauthorized",
        403: "forbidden",
        404: "not_found",
        409: "conflict",
    }.get(status, "http_error")
    category = "auth" if status in (401, 403) else "domain"
    envelope = ApiErrorEnvelope(
        code=code,
        category=category,
        retryable=False,
        message=str(error.detail),
        request_id=get_request_id(),
    )
    return JSONResponse(status_code=status, content=envelope.model_dump(mode="json", by_alias=True))


async def validation_exception_handler(_: Request, error: RequestValidationError) -> JSONResponse:
    # Summarize validation errors to field-level messages without exposing schema internals
    field_errors = []
    for err in error.errors():
        loc = ".".join(str(part) for part in err.get("loc", []))
        field_errors.append({"field": loc, "message": err.get("msg", "Invalid value")})

    envelope = ApiErrorEnvelope(
        code="validation_error",
        category="validation",
        retryable=False,
        message="Requete invalide.",
        request_id=get_request_id(),
        details={"errors": field_errors},
    )
    return JSONResponse(status_code=422, content=envelope.model_dump(mode="json", by_alias=True))


async def unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception (request_id=%s)", get_request_id(), exc_info=exc)
    envelope = ApiErrorEnvelope(
        code="internal_error",
        category="internal",
        retryable=False,
        message="Erreur interne.",
        request_id=get_request_id(),
    )
    return JSONResponse(status_code=500, content=envelope.model_dump(mode="json", by_alias=True))
