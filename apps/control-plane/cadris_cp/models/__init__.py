"""Models package — re-exports all models for backward compatibility.

Import from submodules for new code:
  from cadris_cp.models.base import ApiModel, FlowCode
  from cadris_cp.models.mission import MissionReadModel
  from cadris_cp.models.requests import CreateMissionRequest

Or import from here for convenience:
  from cadris_cp.models import MissionReadModel, CreateMissionRequest
"""

# Base types and helpers
from .base import (
    AgentStatus,
    ApiErrorEnvelope,
    ApiModel,
    BlockStatus,
    CertaintyStatus,
    FLOW_LABELS,
    FlowCode,
    MissionStatus,
    PlanCode,
    TimelineStatus,
    to_camel,
    utc_now,
)

# Mission models
from .mission import (
    ArtifactBlock,
    ArtifactSectionItem,
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

# Dossier models
from .dossier import (
    CitationItem,
    CreateShareLinkRequest,
    CreateShareLinkResponse,
    DossierReadModel,
    ExportReadModel,
    MissionStateResponse,
    QualificationQuestionItem,
    RendererRequest,
    RendererResponse,
    SearchMissionInputsResponse,
)

# Request/response models
from .requests import (
    AnswerQuestionRequest,
    AnswerQuestionResponse,
    CheckoutRequest,
    CreateMissionRequest,
    CreateMissionResponse,
    CreateProjectRequest,
    ForgotPasswordRequest,
    LoginRequest,
    LogoGenerateRequest,
    RegisterRequest,
    ResetPasswordRequest,
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
    SearchMissionInputsRequest,
    UploadMissionInputResponse,
    ValidateDocsRequest,
)

__all__ = [
    # Base
    "AgentStatus", "ApiErrorEnvelope", "ApiModel", "BlockStatus",
    "CertaintyStatus", "FLOW_LABELS", "FlowCode", "MissionStatus",
    "PlanCode", "TimelineStatus", "to_camel", "utc_now",
    # Mission
    "ArtifactBlock", "ArtifactSectionItem", "CertaintyEntry",
    "DossierSection", "MissionAgent", "MissionInputItem",
    "MissionMessage", "MissionQuestion", "MissionReadModel",
    "ProjectSummary", "RuntimeInputItem", "TimelineItem",
    # Dossier
    "CitationItem", "CreateShareLinkRequest", "CreateShareLinkResponse",
    "DossierReadModel", "ExportReadModel", "MissionStateResponse",
    "QualificationQuestionItem", "RendererRequest", "RendererResponse",
    "SearchMissionInputsResponse",
    # Requests
    "AnswerQuestionRequest", "AnswerQuestionResponse", "CheckoutRequest",
    "CreateMissionRequest", "CreateMissionResponse", "CreateProjectRequest",
    "ForgotPasswordRequest", "LoginRequest", "LogoGenerateRequest",
    "RegisterRequest", "ResetPasswordRequest", "RuntimeResumeRequest",
    "RuntimeResumeResponse", "RuntimeStartRequest", "RuntimeStartResponse",
    "SearchMissionInputsRequest", "UploadMissionInputResponse",
    "ValidateDocsRequest",
]
