"""Async event emitter for SSE streaming.

The EventEmitter acts as an async queue: the agent_manager pushes events,
and the SSE endpoint consumes them as an async iterator.
"""

from __future__ import annotations

import asyncio
import logging
from typing import AsyncIterator

from .event_types import EventType, SSEEvent

logger = logging.getLogger(__name__)

# Sentinel value to signal the end of the stream
_DONE = object()


class EventEmitter:
    """Async event emitter backed by an asyncio.Queue.

    Usage:
        emitter = EventEmitter()

        # Producer side (agent_manager):
        await emitter.emit(EventType.AGENT_STARTED, {"agent": "strategy"})
        await emitter.close()

        # Consumer side (SSE endpoint):
        async for event in emitter:
            yield f"event: {event.type}\\ndata: ...\\n\\n"
    """

    def __init__(self, maxsize: int = 200) -> None:
        self._queue: asyncio.Queue[SSEEvent | object] = asyncio.Queue(maxsize=maxsize)
        self._closed = False

    _EMIT_TIMEOUT = 30.0  # seconds — if consumer is gone, don't block forever

    async def emit(self, event_type: EventType, data: dict) -> None:
        """Push an event into the stream with backpressure timeout.

        If the consumer has disconnected or is too slow, the put() will
        time out after _EMIT_TIMEOUT seconds. The event is dropped with
        a warning rather than blocking the mission indefinitely.
        """
        if self._closed:
            logger.warning("emit called on closed emitter: %s", event_type)
            return
        event = SSEEvent(type=event_type, data=data)
        try:
            await asyncio.wait_for(self._queue.put(event), timeout=self._EMIT_TIMEOUT)
        except TimeoutError:
            logger.warning(
                "emit timed out after %.0fs for %s (queue full, consumer likely disconnected)",
                self._EMIT_TIMEOUT, event_type.value,
            )
            return
        logger.debug("emitted %s", event_type.value)

    async def close(self) -> None:
        """Signal the end of the event stream."""
        self._closed = True
        await self._queue.put(_DONE)

    def __aiter__(self) -> AsyncIterator[SSEEvent]:
        return self

    async def __anext__(self) -> SSEEvent:
        item = await self._queue.get()
        if item is _DONE:
            raise StopAsyncIteration
        return item  # type: ignore[return-value]
