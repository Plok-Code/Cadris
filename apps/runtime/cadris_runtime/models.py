from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field

MissionStatus = Literal["draft", "in_progress", "waiting_user", "completed"]
BlockStatus = Literal["not_started", "in_progress", "ready_to_decide", "complete", "to_revise"]
CertaintyStatus = Literal["solid", "to_confirm", "unknown", "blocking"]
TimelineStatus = Literal["not_started", "in_progress", "waiting_user", "completed"]
AgentStatus = Literal["active", "waiting", "done"]


class TimelineItem(BaseModel):
    id: str = Field(max_length=64)
    label: str = Field(max_length=200)
    status: TimelineStatus


class ArtifactSection(BaseModel):
    key: str = Field(max_length=64)
    title: str = Field(max_length=500)
    content: str = Field(max_length=50_000)
    certainty: CertaintyStatus = "unknown"


class ArtifactBlock(BaseModel):
    id: str = Field(max_length=64)
    title: str = Field(max_length=500)
    status: BlockStatus
    certainty: CertaintyStatus
    summary: str = Field(max_length=2000)
    content: str = Field(max_length=50_000)
    sections: list[ArtifactSection] = Field(default_factory=list)


class MissionQuestion(BaseModel):
    id: str = Field(max_length=128)
    title: str = Field(max_length=500)
    body: str = Field(max_length=5000)
    status: Literal["waiting", "answered"] = "waiting"
    answer_text: str | None = Field(default=None, max_length=5000)


class MissionAgent(BaseModel):
    code: str = Field(max_length=64)
    label: str = Field(max_length=200)
    role: str = Field(max_length=500)
    status: AgentStatus
    prompt_key: str = Field(max_length=128)
    prompt_version: str = Field(max_length=32)
    summary: str = Field(max_length=2000)


class MissionMessage(BaseModel):
    id: str = Field(max_length=128)
    agent_code: str = Field(max_length=64)
    agent_label: str = Field(max_length=200)
    stage: str = Field(max_length=64)
    title: str = Field(max_length=500)
    body: str = Field(max_length=10_000)
    created_at: str


class CertaintyEntry(BaseModel):
    id: str = Field(max_length=128)
    title: str = Field(max_length=500)
    status: CertaintyStatus
    impact: str = Field(max_length=2000)
    source_label: str = Field(max_length=200)


class RuntimeInputItem(BaseModel):
    id: str = Field(max_length=64)
    kind: str = Field(max_length=64)
    source: str = Field(max_length=200)
    content: str = Field(max_length=50_000)
    display_name: str | None = Field(default=None, max_length=200)
    mime_type: str | None = Field(default=None, max_length=128)
    byte_size: int | None = None
    preview_text: str | None = Field(default=None, max_length=2000)


class DossierSection(BaseModel):
    id: str = Field(max_length=128)
    title: str = Field(max_length=500)
    content: str = Field(max_length=50_000)
    certainty: CertaintyStatus


FlowCode = Literal["demarrage", "projet_flou", "pivot"]
PlanCode = Literal["free", "starter", "pro", "expert"]


class RuntimeStartRequest(BaseModel):
    mission_id: str = Field(max_length=128, pattern=r"^[a-zA-Z0-9_-]+$")
    project_name: str = Field(max_length=200)
    intake_text: str = Field(min_length=20, max_length=50_000)
    flow_code: FlowCode = "demarrage"
    plan: PlanCode = "free"
    template_id: str | None = Field(default=None, max_length=50)
    supporting_inputs: list[RuntimeInputItem] = Field(default_factory=list)


class RuntimeStartResponse(BaseModel):
    summary: str = Field(max_length=10_000)
    next_step: str = Field(max_length=5_000)
    artifact_blocks: list[ArtifactBlock]
    active_question: MissionQuestion
    active_agents: list[MissionAgent]
    recent_messages: list[MissionMessage]
    timeline: list[TimelineItem]
    status: MissionStatus


class RuntimeResumeRequest(BaseModel):
    mission_id: str = Field(max_length=128, pattern=r"^[a-zA-Z0-9_-]+$")
    project_name: str = Field(max_length=200)
    intake_text: str = Field(max_length=50_000)
    answer_text: str = Field(default="", max_length=20_000)
    flow_code: FlowCode = "demarrage"
    plan: PlanCode = "free"
    cycle_number: int = 1
    previous_answers: list[str] = Field(default_factory=list)
    supporting_inputs: list[RuntimeInputItem] = Field(default_factory=list)
    action: Literal["refine_wave", "next_wave", "answer_qualification"] = "next_wave"


class RuntimeResumeResponse(BaseModel):
    summary: str = Field(max_length=10_000)
    next_step: str = Field(max_length=5_000)
    artifact_blocks: list[ArtifactBlock]
    active_question: MissionQuestion | None = None
    certainty_entries: list[CertaintyEntry] = Field(default_factory=list)
    active_agents: list[MissionAgent]
    recent_messages: list[MissionMessage]
    timeline: list[TimelineItem]
    status: MissionStatus
    dossier_title: str | None = Field(default=None, max_length=500)
    dossier_summary: str | None = Field(default=None, max_length=10_000)
    dossier_sections: list[DossierSection] = Field(default_factory=list)
    quality_label: str | None = Field(default=None, max_length=100)
