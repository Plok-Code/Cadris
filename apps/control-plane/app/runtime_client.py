from __future__ import annotations

import httpx
from .errors import AppError
from .config import settings
from .models import (
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
)
from .request_context import get_request_id


class RuntimeClient:
    async def start_mission(self, payload: RuntimeStartRequest) -> RuntimeStartResponse:
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{settings.runtime_url}/internal/runtime/start",
                    json=payload.model_dump(),
                    headers={"x-request-id": get_request_id()},
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
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{settings.runtime_url}/internal/runtime/resume",
                    json=payload.model_dump(),
                    headers={"x-request-id": get_request_id()},
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
