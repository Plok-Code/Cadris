"""Tests for the async EventEmitter (SSE streaming queue)."""

from __future__ import annotations

import asyncio
import logging

import pytest

from cadris_runtime.event_emitter import EventEmitter, _DONE
from cadris_runtime.event_types import EventType, SSEEvent


# ── Basic emit / consume ────────────────────────────────────────


@pytest.mark.asyncio
async def test_emit_and_consume_single_event():
    """A single emitted event should be consumable via async iteration."""
    emitter = EventEmitter()

    await emitter.emit(EventType.AGENT_STARTED, {"agent": "strategy"})
    await emitter.close()

    events: list[SSEEvent] = []
    async for event in emitter:
        events.append(event)

    assert len(events) == 1
    assert events[0].type == EventType.AGENT_STARTED
    assert events[0].data == {"agent": "strategy"}


@pytest.mark.asyncio
async def test_multiple_events_in_order():
    """Events should be consumed in FIFO order."""
    emitter = EventEmitter()

    event_types = [
        EventType.MISSION_STARTED,
        EventType.AGENT_STARTED,
        EventType.AGENT_THINKING,
        EventType.DOCUMENT_UPDATED,
        EventType.AGENT_COMPLETED,
    ]

    for i, et in enumerate(event_types):
        await emitter.emit(et, {"index": i})
    await emitter.close()

    consumed: list[SSEEvent] = []
    async for event in emitter:
        consumed.append(event)

    assert len(consumed) == len(event_types)
    for i, event in enumerate(consumed):
        assert event.type == event_types[i]
        assert event.data["index"] == i


# ── close() behaviour ──────────────────────────────────────────


@pytest.mark.asyncio
async def test_close_sends_sentinel():
    """After close(), the async iterator should stop."""
    emitter = EventEmitter()
    await emitter.close()

    events: list[SSEEvent] = []
    async for event in emitter:
        events.append(event)

    assert events == []


@pytest.mark.asyncio
async def test_close_sets_closed_flag():
    emitter = EventEmitter()
    assert emitter._closed is False
    await emitter.close()
    assert emitter._closed is True


# ── emit after close ───────────────────────────────────────────


@pytest.mark.asyncio
async def test_emit_after_close_logs_warning(caplog):
    """Emitting after close should log a warning and not enqueue."""
    emitter = EventEmitter()
    await emitter.close()

    with caplog.at_level(logging.WARNING, logger="cadris_runtime.event_emitter"):
        await emitter.emit(EventType.ERROR, {"msg": "too late"})

    assert any("emit called on closed emitter" in record.message for record in caplog.records)

    # The sentinel is the only item in the queue; no extra event was added.
    # Drain the queue to verify only _DONE is present.
    items = []
    while not emitter._queue.empty():
        items.append(emitter._queue.get_nowait())
    # The sentinel was already put by close()
    assert items == [_DONE]


# ── Backpressure timeout ───────────────────────────────────────


@pytest.mark.asyncio
async def test_emit_timeout_on_full_queue(caplog):
    """When the queue is full and nobody consumes, emit should time out."""
    emitter = EventEmitter(maxsize=1)
    # Override timeout to a very short value so the test runs fast
    emitter._EMIT_TIMEOUT = 0.05

    # Fill the queue
    await emitter.emit(EventType.MISSION_STARTED, {"fill": True})

    # Next emit should time out because queue is full
    with caplog.at_level(logging.WARNING, logger="cadris_runtime.event_emitter"):
        await emitter.emit(EventType.ERROR, {"overflow": True})

    assert any("emit timed out" in record.message for record in caplog.records)

    # Only the first event is in the queue (the second was dropped)
    item = emitter._queue.get_nowait()
    assert isinstance(item, SSEEvent)
    assert item.data == {"fill": True}
    assert emitter._queue.empty()


# ── Concurrent producer / consumer ─────────────────────────────


@pytest.mark.asyncio
async def test_concurrent_producer_consumer():
    """Producer and consumer running concurrently should not deadlock."""
    emitter = EventEmitter(maxsize=5)
    n_events = 20

    async def producer():
        for i in range(n_events):
            await emitter.emit(EventType.AGENT_THINKING, {"i": i})
        await emitter.close()

    consumed: list[SSEEvent] = []

    async def consumer():
        async for event in emitter:
            consumed.append(event)

    await asyncio.gather(producer(), consumer())

    assert len(consumed) == n_events
    assert [e.data["i"] for e in consumed] == list(range(n_events))


# ── __aiter__ returns self ─────────────────────────────────────


@pytest.mark.asyncio
async def test_aiter_returns_self():
    emitter = EventEmitter()
    assert emitter.__aiter__() is emitter
