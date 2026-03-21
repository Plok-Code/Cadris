from __future__ import annotations

import httpx
from .cloud_auth import auth_headers, get_id_token
from .errors import AppError
from .config import settings
from .models import RendererRequest, RendererResponse
from .request_context import get_request_id


class RendererClient:
    async def _headers(self) -> dict[str, str]:
        token = await get_id_token(settings.renderer_url)
        return {"x-request-id": get_request_id(), **auth_headers(token)}

    async def render_markdown(self, payload: RendererRequest) -> RendererResponse:
        headers = await self._headers()
        async with httpx.AsyncClient(timeout=10.0) as client:
            try:
                response = await client.post(
                    f"{settings.renderer_url}/internal/renderer/markdown",
                    json=payload.model_dump(),
                    headers=headers,
                )
                response.raise_for_status()
            except httpx.TimeoutException as exc:
                raise AppError.integration("renderer_timeout", "Le renderer ne repond pas a temps.") from exc
            except httpx.HTTPStatusError as exc:
                raise AppError.integration(
                    "renderer_unavailable",
                    "Le renderer a renvoye une erreur.",
                    http_status=502,
                    details={"status_code": exc.response.status_code},
                ) from exc
            except httpx.RequestError as exc:
                raise AppError.integration("renderer_unreachable", "Le renderer est indisponible.") from exc
        return RendererResponse.model_validate(response.json())

    async def render_pdf(self, payload: RendererRequest) -> bytes:
        headers = await self._headers()
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{settings.renderer_url}/internal/renderer/pdf",
                    json=payload.model_dump(),
                    headers=headers,
                )
                response.raise_for_status()
            except httpx.TimeoutException as exc:
                raise AppError.integration("renderer_timeout", "Le renderer ne repond pas a temps pour le PDF.") from exc
            except httpx.HTTPStatusError as exc:
                raise AppError.integration(
                    "renderer_unavailable",
                    "Le renderer a renvoye une erreur lors de la generation PDF.",
                    http_status=502,
                    details={"status_code": exc.response.status_code},
                ) from exc
            except httpx.RequestError as exc:
                raise AppError.integration("renderer_unreachable", "Le renderer est indisponible.") from exc
        return response.content
