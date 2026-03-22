"""Shared base types, helpers, and type aliases used across all models."""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

FlowCode = Literal["demarrage", "projet_flou", "pivot"]

FLOW_LABELS: dict[str, str] = {
    "demarrage": "Nouveau projet",
    "projet_flou": "Projet a recadrer",
    "pivot": "Refonte / pivot",
}

MissionStatus = Literal["draft", "in_progress", "waiting_user", "completed"]
BlockStatus = Literal["not_started", "in_progress", "ready_to_decide", "complete", "to_revise"]
CertaintyStatus = Literal["solid", "to_confirm", "unknown", "blocking"]
TimelineStatus = Literal["not_started", "in_progress", "waiting_user", "completed"]
AgentStatus = Literal["active", "waiting", "done"]
PlanCode = Literal["free", "starter", "pro", "expert"]


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def to_camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.capitalize() for part in parts[1:])


class ApiModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        alias_generator=to_camel,
    )


class ApiErrorEnvelope(ApiModel):
    code: str
    category: Literal["validation", "domain", "auth", "integration", "internal"]
    retryable: bool
    message: str
    request_id: str
    details: dict[str, object] | None = None
