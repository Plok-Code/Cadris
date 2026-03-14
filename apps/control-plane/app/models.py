from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

FlowCode = Literal["demarrage"]
MissionStatus = Literal["draft", "in_progress", "waiting_user", "completed"]
BlockStatus = Literal["not_started", "in_progress", "ready_to_decide", "complete", "to_revise"]
CertaintyStatus = Literal["solid", "to_confirm", "unknown", "blocking"]
TimelineStatus = Literal["not_started", "in_progress", "waiting_user", "completed"]
AgentStatus = Literal["active", "waiting", "done"]


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


class TimelineItem(ApiModel):
    id: str
    label: str
    status: TimelineStatus


class ArtifactBlock(ApiModel):
    id: str
    title: str
    status: BlockStatus
    certainty: CertaintyStatus
    summary: str
    content: str


class MissionQuestion(ApiModel):
    id: str
    title: str
    body: str
    status: Literal["waiting", "answered"]
    answer_text: str | None = None


class MissionInputItem(ApiModel):
    id: str
    kind: str
    source: str
    content: str
    display_name: str | None = None
    mime_type: str | None = None
    byte_size: int | None = None
    preview_text: str | None = None
    created_at: str = Field(default_factory=utc_now)


class RuntimeInputItem(ApiModel):
    id: str
    kind: str
    source: str
    content: str
    display_name: str | None = None
    mime_type: str | None = None
    byte_size: int | None = None
    preview_text: str | None = None


class MissionAgent(ApiModel):
    code: str
    label: str
    role: str
    status: AgentStatus
    prompt_key: str
    prompt_version: str
    summary: str


class MissionMessage(ApiModel):
    id: str
    agent_code: str
    agent_label: str
    stage: str
    title: str
    body: str
    created_at: str = Field(default_factory=utc_now)


class CertaintyEntry(ApiModel):
    id: str
    title: str
    status: CertaintyStatus
    impact: str
    source_label: str


class MissionReadModel(ApiModel):
    id: str
    project_id: str
    flow_code: FlowCode
    flow_label: str
    title: str
    status: MissionStatus
    summary: str
    next_step: str
    intake_text: str
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
    id: str
    name: str
    mission_count: int = 0
    active_mission_id: str | None = None
    active_mission_status: MissionStatus | None = None
    updated_at: str = Field(default_factory=utc_now)


class DossierSection(ApiModel):
    id: str
    title: str
    content: str
    certainty: CertaintyStatus


class DossierReadModel(ApiModel):
    mission_id: str
    title: str
    quality_label: str
    summary: str
    markdown: str
    sections: list[DossierSection]
    updated_at: str = Field(default_factory=utc_now)


class CreateProjectRequest(ApiModel):
    name: str = Field(min_length=3, max_length=120)


class CreateMissionRequest(ApiModel):
    intake_text: str = Field(min_length=20, max_length=5000)


class AnswerQuestionRequest(ApiModel):
    answer_text: str = Field(min_length=10, max_length=5000)


class UploadMissionInputResponse(ApiModel):
    mission: MissionReadModel
    input: MissionInputItem


class CreateMissionResponse(ApiModel):
    project: ProjectSummary
    mission: MissionReadModel


class AnswerQuestionResponse(ApiModel):
    mission: MissionReadModel
    dossier: DossierReadModel


class RuntimeStartRequest(ApiModel):
    mission_id: str
    project_name: str
    intake_text: str
    supporting_inputs: list[RuntimeInputItem] = Field(default_factory=list)


class RuntimeStartResponse(ApiModel):
    summary: str
    next_step: str
    artifact_blocks: list[ArtifactBlock]
    active_question: MissionQuestion
    active_agents: list[MissionAgent]
    recent_messages: list[MissionMessage]
    timeline: list[TimelineItem]
    status: MissionStatus


class RuntimeResumeRequest(ApiModel):
    mission_id: str
    project_name: str
    intake_text: str
    answer_text: str
    supporting_inputs: list[RuntimeInputItem] = Field(default_factory=list)


class RuntimeResumeResponse(ApiModel):
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


class RendererRequest(ApiModel):
    title: str
    summary: str
    sections: list[DossierSection]


class RendererResponse(ApiModel):
    markdown: str
