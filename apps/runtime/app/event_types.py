"""SSE event types for the collaborative agent engine."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class EventType(str, Enum):
    MISSION_STARTED = "mission_started"
    AGENT_STARTED = "agent_started"
    AGENT_THINKING = "agent_thinking"
    AGENT_COMPLETED = "agent_completed"
    DOCUMENT_UPDATED = "document_updated"
    INTER_AGENT_QUERY = "inter_agent_query"
    QUESTION_FOR_USER = "question_for_user"
    MISSION_COMPLETED = "mission_completed"
    ERROR = "error"
    # ── Wave-level events (Phase 2) ───────────────────────
    QUALIFICATION_QUESTIONS = "qualification_questions"
    WAVE_STARTED = "wave_started"
    WAVE_REVIEW = "wave_review"
    WAVE_COMPLETED = "wave_completed"


class SSEEvent(BaseModel):
    type: EventType
    data: dict
