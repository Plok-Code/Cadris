from __future__ import annotations

import logging
import time

from fastapi import FastAPI, Request, Response
from .engine import create_runtime_engine
from .models import (
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
)

logger = logging.getLogger(__name__)

runtime_engine = create_runtime_engine()

app = FastAPI(title="Cadris Runtime", version="0.1.0")


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    start = time.perf_counter()
    response: Response = await call_next(request)
    duration_ms = round((time.perf_counter() - start) * 1000, 1)
    logger.info(
        "request completed",
        extra={
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        },
    )
    return response


@app.get("/health")
async def healthcheck():
    return {"ok": True, **runtime_engine.health_payload()}


@app.post("/internal/runtime/start", response_model=RuntimeStartResponse)
async def start_runtime(payload: RuntimeStartRequest):
    return await runtime_engine.start_mission(payload)


@app.post("/internal/runtime/resume", response_model=RuntimeResumeResponse)
async def resume_runtime(payload: RuntimeResumeRequest):
    return await runtime_engine.resume_mission(payload)
