"""Request and response models for API endpoints."""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .base import ApiModel, FlowCode, MissionStatus, PlanCode
from .mission import (
    ArtifactBlock,
    CertaintyEntry,
    DossierSection,
    MissionAgent,
    MissionInputItem,
    MissionMessage,
    MissionQuestion,
    MissionReadModel,
    ProjectSummary,
    RuntimeInputItem,
    TimelineItem,
)
from .dossier import DossierReadModel


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


class CreateMissionResponse(ApiModel):
    project: ProjectSummary
    mission: MissionReadModel


class AnswerQuestionResponse(ApiModel):
    mission: MissionReadModel
    dossier: DossierReadModel | None = None


class SearchMissionInputsRequest(ApiModel):
    query: str = Field(min_length=3, max_length=1000)
    max_results: int = Field(default=5, ge=1, le=20)


class ValidateDocsRequest(ApiModel):
    validated_doc_ids: list[str] = Field(default_factory=list, max_length=50)
    corrections: dict[str, str] = Field(default_factory=dict, max_length=50)


class RuntimeStartRequest(ApiModel):
    mission_id: str = Field(max_length=64)
    project_name: str = Field(max_length=200)
    intake_text: str = Field(max_length=50_000)
    flow_code: FlowCode = "demarrage"
    plan: PlanCode = "free"
    template_id: str | None = Field(default=None, max_length=50)
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
    mission_id: str = Field(max_length=64)
    project_name: str = Field(max_length=200)
    intake_text: str = Field(max_length=50_000)
    answer_text: str = Field(default="", max_length=20_000)
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


# Auth models (use BaseModel, not ApiModel — no camelCase aliasing)
class RegisterRequest(BaseModel):
    email: str = Field(max_length=256)
    password: str = Field(min_length=8, max_length=128)
    name: str = Field(default="", max_length=200)


class LoginRequest(BaseModel):
    email: str = Field(max_length=256)
    password: str = Field(min_length=8, max_length=128)


class ForgotPasswordRequest(BaseModel):
    email: str = Field(max_length=256)


class ResetPasswordRequest(BaseModel):
    token: str = Field(max_length=256)
    password: str = Field(min_length=8, max_length=128)


class CheckoutRequest(BaseModel):
    plan: str = Field(max_length=32)


class LogoGenerateRequest(ApiModel):
    project_name: str = Field(max_length=200)
    project_brief: str = Field(max_length=5000)
    num_variants: int = Field(default=3, ge=1, le=4)
