from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field

MissionStatus = Literal["draft", "in_progress", "waiting_user", "completed"]
BlockStatus = Literal["not_started", "in_progress", "ready_to_decide", "complete", "to_revise"]
CertaintyStatus = Literal["solid", "to_confirm", "unknown", "blocking"]
TimelineStatus = Literal["not_started", "in_progress", "waiting_user", "completed"]
AgentStatus = Literal["active", "waiting", "done"]


class TimelineItem(BaseModel):
    id: str
    label: str
    status: TimelineStatus


class ArtifactBlock(BaseModel):
    id: str
    title: str
    status: BlockStatus
    certainty: CertaintyStatus
    summary: str
    content: str


class MissionQuestion(BaseModel):
    id: str
    title: str
    body: str
    status: Literal["waiting", "answered"] = "waiting"
    answer_text: str | None = None


class MissionAgent(BaseModel):
    code: str
    label: str
    role: str
    status: AgentStatus
    prompt_key: str
    prompt_version: str
    summary: str


class MissionMessage(BaseModel):
    id: str
    agent_code: str
    agent_label: str
    stage: str
    title: str
    body: str
    created_at: str


class CertaintyEntry(BaseModel):
    id: str
    title: str
    status: CertaintyStatus
    impact: str
    source_label: str


class RuntimeInputItem(BaseModel):
    id: str
    kind: str
    source: str
    content: str
    display_name: str | None = None
    mime_type: str | None = None
    byte_size: int | None = None
    preview_text: str | None = None


class DossierSection(BaseModel):
    id: str
    title: str
    content: str
    certainty: CertaintyStatus


class RuntimeStartRequest(BaseModel):
    mission_id: str
    project_name: str
    intake_text: str = Field(min_length=20)
    supporting_inputs: list[RuntimeInputItem] = Field(default_factory=list)


class RuntimeStartResponse(BaseModel):
    summary: str
    next_step: str
    artifact_blocks: list[ArtifactBlock]
    active_question: MissionQuestion
    active_agents: list[MissionAgent]
    recent_messages: list[MissionMessage]
    timeline: list[TimelineItem]
    status: MissionStatus


class RuntimeResumeRequest(BaseModel):
    mission_id: str
    project_name: str
    intake_text: str
    answer_text: str = Field(min_length=10)
    supporting_inputs: list[RuntimeInputItem] = Field(default_factory=list)


class RuntimeResumeResponse(BaseModel):
    summary: str
    next_step: str
    artifact_blocks: list[ArtifactBlock]
    active_agents: list[MissionAgent]
    recent_messages: list[MissionMessage]
    timeline: list[TimelineItem]
    status: MissionStatus
    dossier_title: str
    dossier_summary: str
    dossier_sections: list[DossierSection]
    quality_label: str
