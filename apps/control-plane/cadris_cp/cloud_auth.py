"""Cloud Run service-to-service authentication.

When deployed on Cloud Run, internal services (runtime, renderer) require
an Authorization header with a Google-signed ID token. This module provides
a helper that fetches the token from the metadata server when running on GCP,
and returns None otherwise (local dev).
"""
from __future__ import annotations

import logging
import os

logger = logging.getLogger(__name__)

# The K_SERVICE env var is set automatically by Cloud Run
_ON_CLOUD_RUN = bool(os.getenv("K_SERVICE"))


async def get_id_token(audience: str) -> str | None:
    """Return a Google ID token for the given audience, or None if not on GCP."""
    if not _ON_CLOUD_RUN:
        return None

    try:
        import google.auth.transport.requests  # type: ignore[import-untyped]
        import google.oauth2.id_token  # type: ignore[import-untyped]

        request = google.auth.transport.requests.Request()
        token = google.oauth2.id_token.fetch_id_token(request, audience)
        return token
    except Exception:  # noqa: BLE001 — GCP auth may fail for many reasons outside our control
        logger.warning("Failed to fetch ID token for %s", audience, exc_info=True)
        return None


def auth_headers(token: str | None) -> dict[str, str]:
    """Build authorization headers if a token is available."""
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}
