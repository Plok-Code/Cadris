from __future__ import annotations

import json
import logging
from typing import AsyncIterator

import httpx
from .cloud_auth import auth_headers, get_id_token
from .errors import AppError
from .config import settings
from .models import (
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
)
from .request_context import get_request_id

logger = logging.getLogger(__name__)


class RuntimeClient:
    async def _headers(self) -> dict[str, str]:
        token = await get_id_token(settings.runtime_url)
        return {"x-request-id": get_request_id(), **auth_headers(token)}

    async def start_mission(self, payload: RuntimeStartRequest) -> RuntimeStartResponse:
        headers = await self._headers()
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{settings.runtime_url}/internal/runtime/start",
                    json=payload.model_dump(),
                    headers=headers,
                )
                response.raise_for_status()
            except httpx.TimeoutException as exc:
                raise AppError.integration("runtime_timeout", "Le runtime ne repond pas a temps.") from exc
            except httpx.HTTPStatusError as exc:
                raise AppError.integration(
                    "runtime_unavailable",
                    "Le runtime a renvoye une erreur.",
                    http_status=502,
                    details={"status_code": exc.response.status_code},
                ) from exc
            except httpx.RequestError as exc:
                raise AppError.integration("runtime_unreachable", "Le runtime est indisponible.") from exc
        return RuntimeStartResponse.model_validate(response.json())

    async def resume_mission(self, payload: RuntimeResumeRequest) -> RuntimeResumeResponse:
        headers = await self._headers()
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{settings.runtime_url}/internal/runtime/resume",
                    json=payload.model_dump(),
                    headers=headers,
                )
                response.raise_for_status()
            except httpx.TimeoutException as exc:
                raise AppError.integration("runtime_timeout", "Le runtime ne repond pas a temps.") from exc
            except httpx.HTTPStatusError as exc:
                raise AppError.integration(
                    "runtime_unavailable",
                    "Le runtime a renvoye une erreur.",
                    http_status=502,
                    details={"status_code": exc.response.status_code},
                ) from exc
            except httpx.RequestError as exc:
                raise AppError.integration("runtime_unreachable", "Le runtime est indisponible.") from exc
        return RuntimeResumeResponse.model_validate(response.json())

    async def start_mission_stream(self, payload: RuntimeStartRequest) -> AsyncIterator[dict]:
        """Call runtime's streaming endpoint and yield parsed SSE events."""
        headers = await self._headers()
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{settings.runtime_url}/internal/runtime/start-stream",
                    json=payload.model_dump(),
                    headers=headers,
                ) as response:
                    response.raise_for_status()
                    event_type = None
                    async for line in response.aiter_lines():
                        line = line.strip()
                        if not line:
                            continue
                        if line.startswith("event: "):
                            event_type = line[7:]
                        elif line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                yield {"event": event_type or "message", "data": data}
                            except json.JSONDecodeError:
                                logger.warning("invalid JSON in SSE data: %s", line[6:])
                            event_type = None
            except httpx.TimeoutException as exc:
                raise AppError.integration("runtime_timeout", "Le runtime ne repond pas a temps.") from exc
            except httpx.HTTPStatusError as exc:
                raise AppError.integration(
                    "runtime_unavailable",
                    "Le runtime a renvoye une erreur.",
                    http_status=502,
                    details={"status_code": exc.response.status_code},
                ) from exc
            except httpx.RequestError as exc:
                raise AppError.integration("runtime_unreachable", "Le runtime est indisponible.") from exc

    async def resume_mission_stream(self, payload: RuntimeResumeRequest) -> AsyncIterator[dict]:
        """Call runtime's streaming resume endpoint and yield parsed SSE events."""
        headers = await self._headers()
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                async with client.stream(
                    "POST",
                    f"{settings.runtime_url}/internal/runtime/resume-stream",
                    json=payload.model_dump(),
                    headers=headers,
                ) as response:
                    response.raise_for_status()
                    event_type = None
                    async for line in response.aiter_lines():
                        line = line.strip()
                        if not line:
                            continue
                        if line.startswith("event: "):
                            event_type = line[7:]
                        elif line.startswith("data: "):
                            try:
                                data = json.loads(line[6:])
                                yield {"event": event_type or "message", "data": data}
                            except json.JSONDecodeError:
                                logger.warning("invalid JSON in SSE data: %s", line[6:])
                            event_type = None
            except httpx.TimeoutException as exc:
                raise AppError.integration("runtime_timeout", "Le runtime ne repond pas a temps.") from exc
            except httpx.HTTPStatusError as exc:
                raise AppError.integration(
                    "runtime_unavailable",
                    "Le runtime a renvoye une erreur.",
                    http_status=502,
                    details={"status_code": exc.response.status_code},
                ) from exc
            except httpx.RequestError as exc:
                raise AppError.integration("runtime_unreachable", "Le runtime est indisponible.") from exc

    async def cleanup_mission(self, mission_id: str) -> None:
        """Ask runtime to remove mission memory and snapshots."""
        headers = await self._headers()
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.delete(
                    f"{settings.runtime_url}/internal/runtime/missions/{mission_id}",
                    headers=headers,
                )
        except Exception:
            logger.warning("Failed to cleanup runtime mission %s", mission_id, exc_info=True)
