from __future__ import annotations

from .models import (
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
)
from .orchestrator import build_resume_response, build_start_response


class LocalRuntimeEngine:
    provider = "local"

    async def start_mission(self, payload: RuntimeStartRequest) -> RuntimeStartResponse:
        return build_start_response(payload)

    async def resume_mission(self, payload: RuntimeResumeRequest) -> RuntimeResumeResponse:
        return build_resume_response(payload)

    def health_payload(self) -> dict[str, object]:
        return {"provider": self.provider, "ready": True}
