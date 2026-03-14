from __future__ import annotations

from typing import Protocol

from .config import settings
from .local_engine import LocalRuntimeEngine
from .models import (
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
)
from .openai_engine import OpenAIRuntimeEngine


class RuntimeEngine(Protocol):
    provider: str

    async def start_mission(self, payload: RuntimeStartRequest) -> RuntimeStartResponse: ...

    async def resume_mission(self, payload: RuntimeResumeRequest) -> RuntimeResumeResponse: ...

    def health_payload(self) -> dict[str, object]: ...


def create_runtime_engine() -> RuntimeEngine:
    if settings.provider == "openai":
        return OpenAIRuntimeEngine(model=settings.openai_model, api_key=settings.openai_api_key)
    return LocalRuntimeEngine()
