from __future__ import annotations

from fastapi import FastAPI
from .engine import create_runtime_engine
from .models import (
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
)

runtime_engine = create_runtime_engine()

app = FastAPI(title="Cadris Runtime", version="0.1.0")


@app.get("/health")
async def healthcheck():
    return {"ok": True, **runtime_engine.health_payload()}


@app.post("/internal/runtime/start", response_model=RuntimeStartResponse)
async def start_runtime(payload: RuntimeStartRequest):
    return await runtime_engine.start_mission(payload)


@app.post("/internal/runtime/resume", response_model=RuntimeResumeResponse)
async def resume_runtime(payload: RuntimeResumeRequest):
    return await runtime_engine.resume_mission(payload)
