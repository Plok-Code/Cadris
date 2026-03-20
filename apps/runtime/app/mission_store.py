"""In-memory mission store for persisting MissionMemory across SSE sessions.

When the stream pauses after a wave (waiting for user validation),
the MissionMemory is stored here so the resume endpoint can reload it.

V1: simple dict. V2: Redis or database persistence.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from .memory import MissionMemory

logger = logging.getLogger(__name__)

_store: dict[str, tuple[MissionMemory, datetime]] = {}

TTL_SECONDS = 3600  # evict after 1 hour of inactivity


def get(mission_id: str) -> MissionMemory | None:
    """Retrieve a stored MissionMemory, refreshing its timestamp."""
    entry = _store.get(mission_id)
    if entry is None:
        return None
    memory, _ = entry
    _store[mission_id] = (memory, datetime.now(UTC))
    return memory


def put(memory: MissionMemory) -> None:
    """Store or update a MissionMemory."""
    _store[memory.mission_id] = (memory, datetime.now(UTC))
    logger.debug("mission_store: stored %s (%d docs)", memory.mission_id, len(memory.documents))


def remove(mission_id: str) -> None:
    """Remove a MissionMemory after mission completion."""
    _store.pop(mission_id, None)
    logger.debug("mission_store: removed %s", mission_id)


def evict_stale() -> int:
    """Remove entries older than TTL_SECONDS. Call periodically if needed."""
    now = datetime.now(UTC)
    stale = [
        mid
        for mid, (_, ts) in _store.items()
        if (now - ts).total_seconds() > TTL_SECONDS
    ]
    for mid in stale:
        del _store[mid]
    if stale:
        logger.info("mission_store: evicted %d stale entries", len(stale))
    return len(stale)
