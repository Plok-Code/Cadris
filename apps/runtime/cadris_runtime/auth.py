"""Service-to-service authentication for the runtime.

The control-plane calls the runtime over an internal network.
This module provides a FastAPI ``Depends()`` guard that checks the
``X-Cadris-Internal-Secret`` header against a shared secret.

Fail-closed: if no secret is configured **and**
``CADRIS_ALLOW_UNSIGNED_REQUESTS`` is not ``true``, all requests
are rejected (except /health).
"""
from __future__ import annotations

import hmac
import logging

from fastapi import Depends, Request
from starlette.responses import JSONResponse

from .config import settings

logger = logging.getLogger(__name__)

_HEADER_NAME = "x-cadris-internal-secret"


async def verify_internal_request(request: Request) -> None:
    """FastAPI dependency that validates the internal shared secret.

    Usage::

        @router.post("/endpoint")
        async def my_endpoint(
            ...,
            _auth: None = Depends(verify_internal_request),
        ):
    """
    secret = settings.internal_secret

    # Dev mode — explicitly opted-in via env var
    if not secret and settings.allow_unsigned_requests:
        return

    # Fail-closed: no secret configured and not in dev mode
    if not secret:
        logger.error(
            "CADRIS_INTERNAL_SECRET not configured and "
            "CADRIS_ALLOW_UNSIGNED_REQUESTS is not true — rejecting request"
        )
        raise _unauthorized("Server misconfigured — auth secret missing")

    # Check header
    header_value = request.headers.get(_HEADER_NAME, "")
    if not header_value:
        raise _unauthorized("Missing authentication header")

    # Constant-time comparison to prevent timing attacks
    if not hmac.compare_digest(header_value, secret):
        logger.warning(
            "runtime auth: invalid secret for %s %s",
            request.method,
            request.url.path,
        )
        raise _unauthorized("Invalid credentials")


def _unauthorized(detail: str) -> Exception:
    """Return an HTTPException-like response for 401.

    We raise a raw exception that FastAPI catches, avoiding
    import of HTTPException to keep this module minimal.
    """
    from fastapi import HTTPException

    return HTTPException(status_code=401, detail=detail)
