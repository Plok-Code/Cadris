"""Mission state persistence for collaborative SSE sessions.

Default behavior:
- If `CADRIS_RUNTIME_STATE_DB_URL` is configured, snapshots are stored in a
  shared SQL database and survive process restarts / multi-instance resumes.
- Otherwise, snapshots are written to local JSON files so local development
  still survives a runtime restart.

An in-memory cache is kept for hot access, but it is no longer the only source
of truth.
"""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import UTC, datetime, timedelta
from pathlib import Path

from sqlalchemy import Column, DateTime, MetaData, String, Table, Text, create_engine, delete, select

from .config import settings
from .memory import AgentQuestion, DocumentDraft, MissionMemory

logger = logging.getLogger(__name__)

TTL_SECONDS = 3600  # evict after 1 hour of inactivity
_store: dict[str, tuple[MissionMemory, datetime]] = {}
_snapshot_dir = settings.state_store_dir
_snapshot_dir.mkdir(parents=True, exist_ok=True)

_metadata = MetaData()
_state_table = Table(
    "runtime_mission_state",
    _metadata,
    Column("mission_id", String(128), primary_key=True),
    Column("payload_json", Text, nullable=False),
    Column("touched_at", DateTime(timezone=True), nullable=False),
)
_engine = None

if settings.state_store_url:
    try:
        _engine = create_engine(settings.state_store_url, future=True)
        _metadata.create_all(_engine)
        logger.info("mission_store: using database backend for snapshots")
    except Exception:  # noqa: BLE001 — DB init may fail; file snapshots are the fallback
        logger.exception("mission_store: failed to initialize database backend, falling back to file snapshots")
        _engine = None


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _snapshot_path(mission_id: str) -> Path:
    return _snapshot_dir / f"{mission_id}.json"


def _serialize_memory(memory: MissionMemory) -> dict[str, object]:
    return {
        "mission_id": memory.mission_id,
        "intake_text": memory.intake_text,
        "plan": memory.plan,
        "documents": [
            {
                "doc_id": doc.doc_id,
                "title": doc.title,
                "agent_code": doc.agent_code,
                "content": doc.content,
                "certainty": doc.certainty,
                "version": doc.version,
                "depends_on": doc.depends_on,
            }
            for doc in memory.documents.values()
        ],
        "questions": [
            {
                "from_agent": question.from_agent,
                "to": question.to,
                "question": question.question,
                "context": question.context,
                "answered": question.answered,
                "answer": question.answer,
            }
            for question in memory.questions
        ],
        "agent_logs": memory.agent_logs,
        "iteration": memory.iteration,
        "current_wave": memory.current_wave,
        "wave_validated": sorted(memory.wave_validated),
        "critic_reviews": memory.critic_reviews,
        "user_answers": memory.user_answers,
        "qualification_questions": memory.qualification_questions,
        "qualification_answers": memory.qualification_answers,
    }


def _deserialize_memory(payload: dict[str, object]) -> MissionMemory:
    documents = {
        item["doc_id"]: DocumentDraft(
            doc_id=item["doc_id"],
            title=item["title"],
            agent_code=item["agent_code"],
            content=item["content"],
            certainty=item["certainty"],
            version=item.get("version", 1),
            depends_on=list(item.get("depends_on", [])),
        )
        for item in payload.get("documents", [])
    }
    questions = [
        AgentQuestion(
            from_agent=item["from_agent"],
            to=item["to"],
            question=item["question"],
            context=item["context"],
            answered=item.get("answered", False),
            answer=item.get("answer"),
        )
        for item in payload.get("questions", [])
    ]

    return MissionMemory(
        mission_id=str(payload["mission_id"]),
        intake_text=str(payload["intake_text"]),
        plan=str(payload.get("plan", "free")),
        documents=documents,
        questions=questions,
        agent_logs=list(payload.get("agent_logs", [])),
        iteration=int(payload.get("iteration", 0)),
        current_wave=int(payload.get("current_wave", 0)),
        wave_validated=set(payload.get("wave_validated", [])),
        critic_reviews=list(payload.get("critic_reviews", [])),
        user_answers=list(payload.get("user_answers", [])),
        qualification_questions=list(payload.get("qualification_questions", [])),
        qualification_answers=dict(payload.get("qualification_answers", {})),
    )


def _read_file_snapshot(mission_id: str) -> tuple[MissionMemory, datetime] | None:
    path = _snapshot_path(mission_id)
    if not path.exists():
        return None

    try:
        wrapper = json.loads(path.read_text(encoding="utf-8"))
        touched_at = datetime.fromisoformat(wrapper["touched_at"])
        if touched_at.tzinfo is None:
            touched_at = touched_at.replace(tzinfo=UTC)
        memory = _deserialize_memory(wrapper["mission"])
        return memory, touched_at
    except (json.JSONDecodeError, KeyError, ValueError, OSError):
        logger.exception("mission_store: failed to read snapshot %s", mission_id)
        path.unlink(missing_ok=True)
        return None


def _write_file_snapshot(memory: MissionMemory, touched_at: datetime) -> None:
    wrapper = {
        "touched_at": touched_at.isoformat(),
        "mission": _serialize_memory(memory),
    }
    path = _snapshot_path(memory.mission_id)
    temp_path = path.with_suffix(".json.tmp")
    temp_path.write_text(json.dumps(wrapper, ensure_ascii=False), encoding="utf-8")
    temp_path.replace(path)


def _delete_file_snapshot(mission_id: str) -> None:
    _snapshot_path(mission_id).unlink(missing_ok=True)


def _read_db_snapshot(mission_id: str) -> tuple[MissionMemory, datetime] | None:
    if _engine is None:
        return None

    with _engine.begin() as connection:
        row = connection.execute(
            select(_state_table.c.payload_json, _state_table.c.touched_at).where(
                _state_table.c.mission_id == mission_id
            )
        ).mappings().first()

    if row is None:
        return None

    memory = _deserialize_memory(json.loads(row["payload_json"]))
    touched_at = row["touched_at"]
    if touched_at.tzinfo is None:
        touched_at = touched_at.replace(tzinfo=UTC)
    return memory, touched_at


def _write_db_snapshot(memory: MissionMemory, touched_at: datetime) -> None:
    if _engine is None:
        return

    payload_json = json.dumps(_serialize_memory(memory), ensure_ascii=False)
    with _engine.begin() as connection:
        connection.execute(delete(_state_table).where(_state_table.c.mission_id == memory.mission_id))
        connection.execute(
            _state_table.insert().values(
                mission_id=memory.mission_id,
                payload_json=payload_json,
                touched_at=touched_at,
            )
        )


def _delete_db_snapshot(mission_id: str) -> None:
    if _engine is None:
        return

    with _engine.begin() as connection:
        connection.execute(delete(_state_table).where(_state_table.c.mission_id == mission_id))


def _load_persisted_snapshot(mission_id: str) -> tuple[MissionMemory, datetime] | None:
    if _engine is not None:
        return _read_db_snapshot(mission_id)
    return _read_file_snapshot(mission_id)


def _persist_snapshot(memory: MissionMemory, touched_at: datetime) -> None:
    if _engine is not None:
        _write_db_snapshot(memory, touched_at)
        return
    _write_file_snapshot(memory, touched_at)


def _delete_snapshot(mission_id: str) -> None:
    if _engine is not None:
        _delete_db_snapshot(mission_id)
        return
    _delete_file_snapshot(mission_id)


def _is_stale(touched_at: datetime, *, now: datetime | None = None) -> bool:
    reference = now or _utc_now()
    return (reference - touched_at) > timedelta(seconds=TTL_SECONDS)


def get(mission_id: str) -> MissionMemory | None:
    """Retrieve a stored MissionMemory and refresh its inactivity timestamp."""
    now = _utc_now()
    entry = _store.get(mission_id)
    if entry is not None:
        memory, touched_at = entry
        if _is_stale(touched_at, now=now):
            remove(mission_id)
            return None
        _store[mission_id] = (memory, now)
        _persist_snapshot(memory, now)
        return memory

    persisted = _load_persisted_snapshot(mission_id)
    if persisted is None:
        return None

    memory, touched_at = persisted
    if _is_stale(touched_at, now=now):
        remove(mission_id)
        return None

    _store[mission_id] = (memory, now)
    _persist_snapshot(memory, now)
    logger.debug("mission_store: restored %s from persistent storage", mission_id)
    return memory


def put(memory: MissionMemory) -> None:
    """Store or update a MissionMemory in cache and persistent storage."""
    touched_at = _utc_now()
    _store[memory.mission_id] = (memory, touched_at)
    _persist_snapshot(memory, touched_at)
    logger.debug("mission_store: stored %s (%d docs)", memory.mission_id, len(memory.documents))


def remove(mission_id: str) -> None:
    """Remove a MissionMemory after mission completion or TTL expiry."""
    _store.pop(mission_id, None)
    _delete_snapshot(mission_id)
    logger.debug("mission_store: removed %s", mission_id)


def evict_stale() -> int:
    """Remove entries older than TTL_SECONDS from cache and persistence."""
    now = _utc_now()
    stale_ids = [
        mission_id
        for mission_id, (_, touched_at) in _store.items()
        if _is_stale(touched_at, now=now)
    ]
    for mission_id in stale_ids:
        remove(mission_id)

    if _engine is not None:
        cutoff = now - timedelta(seconds=TTL_SECONDS)
        with _engine.begin() as connection:
            connection.execute(delete(_state_table).where(_state_table.c.touched_at < cutoff))
    else:
        for path in _snapshot_dir.glob("*.json"):
            snapshot = _read_file_snapshot(path.stem)
            if snapshot is None:
                continue
            _, touched_at = snapshot
            if _is_stale(touched_at, now=now):
                path.unlink(missing_ok=True)

    if stale_ids:
        logger.info("mission_store: evicted %d stale entries", len(stale_ids))
    return len(stale_ids)


# ── Async wrappers with per-mission locking ────────────────────

_locks: dict[str, asyncio.Lock] = {}


def _get_lock(mission_id: str) -> asyncio.Lock:
    """Return (or create) an asyncio.Lock for the given mission_id."""
    if mission_id not in _locks:
        _locks[mission_id] = asyncio.Lock()
    return _locks[mission_id]


async def aget(mission_id: str) -> MissionMemory | None:
    """Async version of get() with per-mission locking."""
    async with _get_lock(mission_id):
        return get(mission_id)


async def aput(memory: MissionMemory) -> None:
    """Async version of put() with per-mission locking."""
    async with _get_lock(memory.mission_id):
        put(memory)


async def aremove(mission_id: str) -> None:
    """Async version of remove() with per-mission locking."""
    lock = _get_lock(mission_id)
    async with lock:
        remove(mission_id)
    _locks.pop(mission_id, None)
