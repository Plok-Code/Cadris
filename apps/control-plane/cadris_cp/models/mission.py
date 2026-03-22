"""Mission-related models: read models, agents, messages, timeline."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .base import (
    AgentStatus,
    ApiModel,
    BlockStatus,
    CertaintyStatus,
    FlowCode,
    MissionStatus,
    TimelineStatus,
    utc_now,
)


class TimelineItem(ApiModel):
    id: str = Field(max_length=64)
    label: str = Field(max_length=200)
    status: TimelineStatus


class ArtifactSectionItem(ApiModel):
    key: str = Field(max_length=64)
    title: str = Field(max_length=500)
    content: str = Field(max_length=50_000)
    certainty: CertaintyStatus = "unknown"


class ArtifactBlock(ApiModel):
    id: str = Field(max_length=64)
    title: str = Field(max_length=500)
    status: BlockStatus
    certainty: CertaintyStatus
    summary: str = Field(max_length=2000)
    content: str = Field(max_length=50_000)
    sections: list[ArtifactSectionItem] = Field(default_factory=list)


class MissionQuestion(ApiModel):
    id: str = Field(max_length=128)
    title: str = Field(max_length=500)
    body: str = Field(max_length=5000)
    status: Literal["waiting", "answered"] = "waiting"
    answer_text: str | None = Field(default=None, max_length=5000)


class MissionInputItem(ApiModel):
    id: str = Field(max_length=64)
    kind: str = Field(max_length=64)
    source: str = Field(max_length=200)
    content: str = Field(max_length=50_000)
    display_name: str | None = Field(default=None, max_length=200)
    mime_type: str | None = Field(default=None, max_length=128)
    byte_size: int | None = None
    preview_text: str | None = Field(default=None, max_length=2000)
    openai_file_id: str | None = Field(default=None, max_length=128)
    vector_store_id: str | None = Field(default=None, max_length=128)
    created_at: str = Field(default_factory=utc_now)


class RuntimeInputItem(ApiModel):
    id: str = Field(max_length=64)
    kind: str = Field(max_length=64)
    source: str = Field(max_length=200)
    content: str = Field(max_length=50_000)
    display_name: str | None = Field(default=None, max_length=200)
    mime_type: str | None = Field(default=None, max_length=128)
    byte_size: int | None = None
    preview_text: str | None = Field(default=None, max_length=2000)


class MissionAgent(ApiModel):
    code: str = Field(max_length=64)
    label: str = Field(max_length=200)
    role: str = Field(max_length=500)
    status: AgentStatus
    prompt_key: str = Field(max_length=128)
    prompt_version: str = Field(max_length=32)
    summary: str = Field(max_length=2000)


class MissionMessage(ApiModel):
    id: str = Field(max_length=128)
    agent_code: str = Field(max_length=64)
    agent_label: str = Field(max_length=200)
    stage: str = Field(max_length=64)
    title: str = Field(max_length=500)
    body: str = Field(max_length=10000)
    created_at: str = Field(default_factory=utc_now)


class CertaintyEntry(ApiModel):
    id: str = Field(max_length=128)
    title: str = Field(max_length=500)
    status: CertaintyStatus
    impact: str = Field(max_length=2000)
    source_label: str = Field(max_length=200)


class MissionReadModel(ApiModel):
    id: str = Field(max_length=64)
    project_id: str = Field(max_length=64)
    flow_code: FlowCode
    flow_label: str = Field(max_length=200)
    title: str = Field(max_length=500)
    status: MissionStatus
    summary: str = Field(max_length=2000)
    next_step: str = Field(max_length=2000)
    intake_text: str = Field(max_length=50_000)
    inputs: list[MissionInputItem] = Field(default_factory=list)
    artifact_blocks: list[ArtifactBlock]
    active_question: MissionQuestion | None
    question_history: list[MissionQuestion] = Field(default_factory=list)
    certainty_entries: list[CertaintyEntry] = Field(default_factory=list)
    active_agents: list[MissionAgent] = Field(default_factory=list)
    recent_messages: list[MissionMessage] = Field(default_factory=list)
    timeline: list[TimelineItem]
    dossier_ready: bool
    updated_at: str = Field(default_factory=utc_now)


class ProjectSummary(ApiModel):
    id: str = Field(max_length=64)
    name: str = Field(max_length=200)
    mission_count: int = 0
    active_mission_id: str | None = Field(default=None, max_length=64)
    active_mission_status: MissionStatus | None = None
    updated_at: str = Field(default_factory=utc_now)


class DossierSection(ApiModel):
    id: str = Field(max_length=128)
    title: str = Field(max_length=500)
    content: str = Field(max_length=50000)
    certainty: CertaintyStatus
    agent: str = Field(default="", max_length=64)
    version: int = 1
    wave: int = 0
    validated: bool = False
    correction: str = Field(default="", max_length=5000)
