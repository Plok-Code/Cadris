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


class ArtifactSection(BaseModel):
    key: str
    title: str
    content: str
    certainty: CertaintyStatus = "unknown"


class ArtifactBlock(BaseModel):
    id: str
    title: str
    status: BlockStatus
    certainty: CertaintyStatus
    summary: str
    content: str
    sections: list[ArtifactSection] = Field(default_factory=list)


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


FlowCode = Literal["demarrage", "projet_flou", "pivot"]
PlanCode = Literal["free", "starter", "pro", "expert"]


class RuntimeStartRequest(BaseModel):
    mission_id: str
    project_name: str
    intake_text: str = Field(min_length=20, max_length=50_000)
    flow_code: FlowCode = "demarrage"
    plan: PlanCode = "free"
    template_id: str | None = None
    supporting_inputs: list[RuntimeInputItem] = Field(default_factory=list, max_length=20)


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
    intake_text: str = Field(max_length=50_000)
    answer_text: str = Field(default="", max_length=20_000)
    flow_code: FlowCode = "demarrage"
    plan: PlanCode = "free"
    cycle_number: int = 1
    previous_answers: list[str] = Field(default_factory=list)
    supporting_inputs: list[RuntimeInputItem] = Field(default_factory=list)
    action: Literal["refine_wave", "next_wave", "answer_qualification"] = "next_wave"


class RuntimeResumeResponse(BaseModel):
    summary: str
    next_step: str
    artifact_blocks: list[ArtifactBlock]
    active_question: MissionQuestion | None = None
    certainty_entries: list[CertaintyEntry] = Field(default_factory=list)
    active_agents: list[MissionAgent]
    recent_messages: list[MissionMessage]
    timeline: list[TimelineItem]
    status: MissionStatus
    dossier_title: str | None = None
    dossier_summary: str | None = None
    dossier_sections: list[DossierSection] = Field(default_factory=list)
    quality_label: str | None = None
