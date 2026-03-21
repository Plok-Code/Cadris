from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

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


class ArtifactSectionItem(ApiModel):
    key: str
    title: str
    content: str
    certainty: CertaintyStatus = "unknown"


class ArtifactBlock(ApiModel):
    id: str
    title: str
    status: BlockStatus
    certainty: CertaintyStatus
    summary: str
    content: str
    sections: list[ArtifactSectionItem] = Field(default_factory=list)


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
    openai_file_id: str | None = None
    vector_store_id: str | None = None
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
    agent: str = ""
    version: int = 1
    wave: int = 0
    validated: bool = False
    correction: str = ""


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
    flow_code: FlowCode = "demarrage"
    template_id: str | None = Field(default=None, max_length=50)


class AnswerQuestionRequest(ApiModel):
    answer_text: str = Field(default="", max_length=5000)
    action: Literal["refine_wave", "next_wave", "answer_qualification"] = "next_wave"


class UploadMissionInputResponse(ApiModel):
    mission: MissionReadModel
    input: MissionInputItem


class CitationItem(ApiModel):
    id: str
    mission_id: str
    input_id: str
    agent_code: str
    excerpt: str
    locator: str | None = None
    score: float | None = None
    display_name: str | None = None
    created_at: str = Field(default_factory=utc_now)


class SearchMissionInputsRequest(ApiModel):
    query: str = Field(min_length=3, max_length=1000)
    max_results: int = Field(default=5, ge=1, le=20)


class SearchMissionInputsResponse(ApiModel):
    results: list[CitationItem]


class CreateMissionResponse(ApiModel):
    project: ProjectSummary
    mission: MissionReadModel


class AnswerQuestionResponse(ApiModel):
    mission: MissionReadModel
    dossier: DossierReadModel | None = None


PlanCode = Literal["free", "starter", "pro", "expert"]


class RuntimeStartRequest(ApiModel):
    mission_id: str
    project_name: str
    intake_text: str
    flow_code: FlowCode = "demarrage"
    plan: PlanCode = "free"
    template_id: str | None = None
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
    answer_text: str = ""
    flow_code: FlowCode = "demarrage"
    plan: PlanCode = "free"
    cycle_number: int = 1
    previous_answers: list[str] = Field(default_factory=list)
    supporting_inputs: list[RuntimeInputItem] = Field(default_factory=list)
    action: Literal["refine_wave", "next_wave", "answer_qualification"] = "next_wave"


class RuntimeResumeResponse(ApiModel):
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


class ExportReadModel(ApiModel):
    id: str
    mission_id: str
    bundle_type: str
    format: str
    snapshot_version: int
    partial: bool = False
    token: str | None = None
    file_url: str | None = None
    revoked: bool = False
    created_at: str = Field(default_factory=utc_now)


class CreateShareLinkRequest(ApiModel):
    pass


class CreateShareLinkResponse(ApiModel):
    export: ExportReadModel
    share_url: str


class RendererRequest(ApiModel):
    title: str
    summary: str
    quality_label: str | None = None
    sections: list[DossierSection]


class RendererResponse(ApiModel):
    markdown: str


class QualificationQuestionItem(ApiModel):
    question: str
    context: str = ""


class MissionStateResponse(ApiModel):
    id: str
    phase: str
    current_wave: int
    intake_text: str
    qualification_answers: dict[str, str] = Field(default_factory=dict)
    qualification_questions: list[QualificationQuestionItem] = Field(default_factory=list)
    documents: list[DossierSection] = Field(default_factory=list)
    dossier_ready: bool = False
    question_history: list[MissionQuestion] = Field(default_factory=list)


class ValidateDocsRequest(ApiModel):
    validated_doc_ids: list[str] = Field(default_factory=list)
    corrections: dict[str, str] = Field(default_factory=dict)


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str = ""


class LoginRequest(BaseModel):
    email: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    password: str


class CheckoutRequest(BaseModel):
    plan: str


class LogoGenerateRequest(BaseModel):
    project_name: str
    project_brief: str
    num_variants: int = 3
