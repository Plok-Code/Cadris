from __future__ import annotations

import asyncio
import json
import logging
import time

from fastapi import FastAPI, Request, Response
from fastapi.responses import StreamingResponse

from pydantic import BaseModel, Field

from .collaborative_engine import CollaborativeEngine
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
from . import training_logger

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


# ── SSE streaming endpoints ───────────────────────────────


@app.get("/internal/runtime/mission/{mission_id}/documents")
async def get_mission_documents(mission_id: str):
    """Return full document contents for a mission (used by benchmark scoring)."""
    memory = mission_store.get(mission_id)
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
async def cleanup_mission(mission_id: str):
    """Remove mission memory and snapshots from runtime."""
    from . import mission_store
    mission_store.remove(mission_id)
    return {"ok": True}


# ── Training data collection ─────────────────────────────


class FeedbackRequest(BaseModel):
    mission_id: str
    doc_id: str | None = None
    rating: int = Field(ge=1, le=5, description="1=bad, 5=excellent")
    correction: str = ""
    notes: str = ""


@app.post("/internal/runtime/feedback")
async def submit_feedback(payload: FeedbackRequest):
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
async def start_mission_stream(payload: RuntimeStartRequest):
    """Launch a collaborative mission and stream SSE events in real-time."""
    if not isinstance(runtime_engine, CollaborativeEngine):
        # Fallback: convert Pydantic result into proper SSE events
        result = await runtime_engine.start_mission(payload)
        d = result.model_dump() if hasattr(result, "model_dump") else (result if isinstance(result, dict) else {"ok": True})

        async def fallback_sse():
            for block in d.get("artifact_blocks", []):
                yield f"event: document_updated\ndata: {json.dumps(block, ensure_ascii=False)}\n\n"
            questions = d.get("questions", [])
            if questions:
                yield f"event: qualification_questions\ndata: {json.dumps({'questions': questions}, ensure_ascii=False)}\n\n"
            yield f"event: mission_completed\ndata: {json.dumps(d, ensure_ascii=False)}\n\n"

        return StreamingResponse(
            fallback_sse(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
        )

    async def event_generator():
        emitter = EventEmitter()

        async def _run():
            try:
                await runtime_engine.start_mission_stream(payload, emitter)
            except Exception as exc:
                logger.error("mission stream error: %s", exc, exc_info=True)
                await emitter.emit(EventType.ERROR, {"error": str(exc)})
            finally:
                await emitter.close()

        task = asyncio.create_task(_run())

        async for event in emitter:
            yield f"event: {event.type.value}\ndata: {json.dumps(event.data, ensure_ascii=False)}\n\n"

        await task

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@app.post("/internal/runtime/resume-stream")
async def resume_mission_stream(payload: RuntimeResumeRequest):
    """Resume a collaborative mission with user answer and stream SSE events."""
    if not isinstance(runtime_engine, CollaborativeEngine):
        result = await runtime_engine.resume_mission(payload)
        d = result.model_dump() if hasattr(result, "model_dump") else (result if isinstance(result, dict) else {"ok": True})

        async def fallback_sse():
            for block in d.get("artifact_blocks", []):
                yield f"event: document_updated\ndata: {json.dumps(block, ensure_ascii=False)}\n\n"
            questions = d.get("questions", [])
            if questions:
                yield f"event: qualification_questions\ndata: {json.dumps({'questions': questions}, ensure_ascii=False)}\n\n"
            yield f"event: mission_completed\ndata: {json.dumps(d, ensure_ascii=False)}\n\n"

        return StreamingResponse(
            fallback_sse(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
        )

    async def event_generator():
        emitter = EventEmitter()

        async def _run():
            try:
                await runtime_engine.resume_mission_stream(payload, emitter)
            except Exception as exc:
                logger.error("mission resume stream error: %s", exc, exc_info=True)
                await emitter.emit(EventType.ERROR, {"error": str(exc)})
            finally:
                await emitter.close()

        task = asyncio.create_task(_run())

        async for event in emitter:
            yield f"event: {event.type.value}\ndata: {json.dumps(event.data, ensure_ascii=False)}\n\n"

        await task

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
