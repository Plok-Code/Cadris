from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse

from pydantic import BaseModel, Field


# ── Structured JSON logging for production ────────────────────
class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info and record.exc_info[0]:
            payload["exc"] = self.formatException(record.exc_info)
        for key in ("method", "path", "status_code", "duration_ms"):
            val = getattr(record, key, None)
            if val is not None:
                payload[key] = val
        return json.dumps(payload, ensure_ascii=False, default=str)


def _setup_logging() -> None:
    level = logging.INFO
    if os.getenv("K_SERVICE"):
        handler = logging.StreamHandler()
        handler.setFormatter(_JsonFormatter())
        logging.root.handlers = [handler]
        logging.root.setLevel(level)
    else:
        logging.basicConfig(level=level, format="%(asctime)s %(levelname)-8s %(name)s — %(message)s")


_setup_logging()

from .auth import verify_internal_request
from .collaborative_engine import CollaborativeEngine
from .config import settings
from .engine import create_runtime_engine
from .event_emitter import EventEmitter
from .event_types import EventType
from . import mission_store
from .models import (
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
)
from .rate_limit import check_rate_limit
from . import training_logger

logger = logging.getLogger(__name__)

runtime_engine = create_runtime_engine()

_eviction_task: asyncio.Task | None = None


async def _periodic_eviction() -> None:
    """Background task: evict stale missions from memory every 5 minutes."""
    while True:
        await asyncio.sleep(300)
        try:
            mission_store.evict_stale()
        except Exception:  # noqa: BLE001 — background task must not crash
            logger.exception("periodic eviction failed")


@asynccontextmanager
async def lifespan(_: FastAPI):
    global _eviction_task

    # ── Startup checks ──
    if settings.model_profile != "dev":
        if not settings.openai_api_key and not settings.together_api_key:
            logger.warning(
                "Neither OPENAI_API_KEY nor TOGETHER_API_KEY is set — "
                "agent execution will fail until at least one is configured"
            )

    _eviction_task = asyncio.create_task(_periodic_eviction())
    logger.info("runtime started (profile=%s)", settings.model_profile)

    yield

    # ── Graceful shutdown ──
    if _eviction_task:
        _eviction_task.cancel()
        try:
            await _eviction_task
        except asyncio.CancelledError:
            pass
    logger.info("runtime shutdown complete")


app = FastAPI(title="Cadris Runtime", version="0.1.0", lifespan=lifespan)


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
async def start_runtime(payload: RuntimeStartRequest, _auth: None = Depends(verify_internal_request)):
    return await runtime_engine.start_mission(payload)


@app.post("/internal/runtime/resume", response_model=RuntimeResumeResponse)
async def resume_runtime(payload: RuntimeResumeRequest, _auth: None = Depends(verify_internal_request)):
    return await runtime_engine.resume_mission(payload)


# ── SSE helpers ───────────────────────────────────────────

_SSE_HEADERS = {
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "X-Accel-Buffering": "no",
}

MISSION_TIMEOUT = settings.mission_timeout


def _build_fallback_sse(d: dict):
    """Build a fallback SSE generator from a non-streaming engine result."""
    async def _gen():
        for block in d.get("artifact_blocks", []):
            yield f"event: document_updated\ndata: {json.dumps(block, ensure_ascii=False)}\n\n"
        questions = d.get("questions", [])
        if questions:
            yield f"event: qualification_questions\ndata: {json.dumps({'questions': questions}, ensure_ascii=False)}\n\n"
        yield f"event: mission_completed\ndata: {json.dumps(d, ensure_ascii=False)}\n\n"
    return StreamingResponse(_gen(), media_type="text/event-stream", headers=_SSE_HEADERS)


def _build_streaming_sse(coro_factory):
    """Build a streaming SSE response with timeout and error handling.

    coro_factory: async callable(emitter) that runs the engine method.
    """
    async def event_generator():
        emitter = EventEmitter()
        agent_task: asyncio.Task | None = None

        async def _run():
            try:
                async with asyncio.timeout(MISSION_TIMEOUT):
                    await coro_factory(emitter)
            except TimeoutError:
                logger.error("mission stream timed out after %ds", MISSION_TIMEOUT)
                await emitter.emit(EventType.ERROR, {"error": "La mission a depasse le temps limite."})
            except asyncio.CancelledError:
                logger.info("mission stream cancelled (client disconnect)")
                raise
            except Exception as exc:  # noqa: BLE001 — SSE must report errors, never drop
                logger.error("mission stream error: %s", exc, exc_info=True)
                await emitter.emit(EventType.ERROR, {"error": "Une erreur interne est survenue. Veuillez reessayer."})
            finally:
                await emitter.close()

        agent_task = asyncio.create_task(_run())

        try:
            # Use wait_for with a heartbeat interval so idle periods
            # (e.g. agent cooldowns) don't cause proxy/LB timeouts.
            HEARTBEAT_INTERVAL = settings.heartbeat_interval
            while True:
                try:
                    event = await asyncio.wait_for(
                        emitter.__anext__(), timeout=HEARTBEAT_INTERVAL
                    )
                    yield f"event: {event.type.value}\ndata: {json.dumps(event.data, ensure_ascii=False)}\n\n"
                except StopAsyncIteration:
                    break
                except TimeoutError:
                    # No event for HEARTBEAT_INTERVAL — send SSE comment as keepalive
                    yield ": heartbeat\n\n"
        except asyncio.CancelledError:
            # Client disconnected — cancel the background agent task
            if agent_task and not agent_task.done():
                agent_task.cancel()
            raise

        await agent_task

    return StreamingResponse(event_generator(), media_type="text/event-stream", headers=_SSE_HEADERS)


# ── SSE streaming endpoints ───────────────────────────────


@app.get("/internal/runtime/mission/{mission_id}/documents")
async def get_mission_documents(mission_id: str, _auth: None = Depends(verify_internal_request)):
    """Return full document contents for a mission (used by benchmark scoring)."""
    memory = await mission_store.aget(mission_id)
    if memory is None:
        return {"error": "mission not found", "documents": {}}
    docs = {}
    for doc_id, doc in memory.documents.items():
        docs[doc_id] = {
            "doc_id": doc.doc_id,
            "title": doc.title,
            "agent": doc.agent_code,
            "certainty": doc.certainty,
            "content": doc.content,
            "version": doc.version,
        }
    return {"mission_id": mission_id, "total_documents": len(docs), "documents": docs}


# ── Mission cleanup ──────────────────────────────────────


@app.delete("/internal/runtime/missions/{mission_id}")
async def cleanup_mission(mission_id: str, _auth: None = Depends(verify_internal_request)):
    """Remove mission memory and snapshots from runtime."""
    from . import mission_store
    await mission_store.aremove(mission_id)
    return {"ok": True}


# ── Training data collection ─────────────────────────────


class FeedbackRequest(BaseModel):
    mission_id: str = Field(max_length=128, pattern=r"^[a-zA-Z0-9_-]+$")
    doc_id: str | None = Field(default=None, max_length=200)
    rating: int = Field(ge=1, le=5, description="1=bad, 5=excellent")
    correction: str = Field(default="", max_length=10_000)
    notes: str = Field(default="", max_length=5_000)


@app.post("/internal/runtime/feedback")
async def submit_feedback(payload: FeedbackRequest, _auth: None = Depends(verify_internal_request)):
    """Collect user feedback on a document or overall mission. Stored for training."""
    training_logger.log_feedback(
        mission_id=payload.mission_id,
        doc_id=payload.doc_id,
        rating=payload.rating,
        correction=payload.correction,
        notes=payload.notes,
    )
    return {"ok": True}


@app.post("/internal/runtime/start-stream")
async def start_mission_stream(payload: RuntimeStartRequest, _auth: None = Depends(verify_internal_request)):
    """Launch a collaborative mission and stream SSE events in real-time."""
    # Rate limit: 5 mission starts per minute per mission_id
    if not check_rate_limit(f"start:{payload.mission_id}", max_requests=5, window_seconds=60):
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded. Please wait before starting a new mission."})

    if not isinstance(runtime_engine, CollaborativeEngine):
        result = await runtime_engine.start_mission(payload)
        d = result.model_dump() if hasattr(result, "model_dump") else (result if isinstance(result, dict) else {"ok": True})
        return _build_fallback_sse(d)

    return _build_streaming_sse(lambda emitter: runtime_engine.start_mission_stream(payload, emitter))


@app.post("/internal/runtime/resume-stream")
async def resume_mission_stream(payload: RuntimeResumeRequest, _auth: None = Depends(verify_internal_request)):
    """Resume a collaborative mission with user answer and stream SSE events."""
    # Rate limit: 5 resumes per minute per mission_id
    if not check_rate_limit(f"resume:{payload.mission_id}", max_requests=5, window_seconds=60):
        return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded. Please wait before resuming."})

    if not isinstance(runtime_engine, CollaborativeEngine):
        result = await runtime_engine.resume_mission(payload)
        d = result.model_dump() if hasattr(result, "model_dump") else (result if isinstance(result, dict) else {"ok": True})
        return _build_fallback_sse(d)

    return _build_streaming_sse(lambda emitter: runtime_engine.resume_mission_stream(payload, emitter))
