"""Dossier, export, and renderer models."""
from __future__ import annotations

from pydantic import Field

from .base import ApiModel, utc_now
from .mission import DossierSection, MissionQuestion


class DossierReadModel(ApiModel):
    mission_id: str = Field(max_length=64)
    title: str = Field(max_length=500)
    quality_label: str = Field(max_length=100)
    summary: str = Field(max_length=10_000)
    markdown: str = Field(max_length=500_000)  # full dossier can be large
    sections: list[DossierSection]
    updated_at: str = Field(default_factory=utc_now)


class ExportReadModel(ApiModel):
    id: str = Field(max_length=64)
    mission_id: str = Field(max_length=64)
    bundle_type: str = Field(max_length=64)
    format: str = Field(max_length=32)
    snapshot_version: int
    partial: bool = False
    token: str | None = Field(default=None, max_length=256)
    file_url: str | None = Field(default=None, max_length=2000)
    revoked: bool = False
    created_at: str = Field(default_factory=utc_now)


class CreateShareLinkRequest(ApiModel):
    pass


class CreateShareLinkResponse(ApiModel):
    export: ExportReadModel
    share_url: str = Field(max_length=2000)


class RendererRequest(ApiModel):
    title: str = Field(max_length=500)
    summary: str = Field(max_length=10000)
    quality_label: str | None = Field(default=None, max_length=100)
    sections: list[DossierSection]


class RendererResponse(ApiModel):
    markdown: str = Field(max_length=500_000)


class QualificationQuestionItem(ApiModel):
    question: str = Field(max_length=2000)
    context: str = Field(default="", max_length=5000)


class MissionStateResponse(ApiModel):
    id: str = Field(max_length=64)
    phase: str = Field(max_length=64)
    current_wave: int
    intake_text: str = Field(max_length=50_000)
    qualification_answers: dict[str, str] = Field(default_factory=dict)
    qualification_questions: list[QualificationQuestionItem] = Field(default_factory=list)
    documents: list[DossierSection] = Field(default_factory=list)
    dossier_ready: bool = False
    question_history: list[MissionQuestion] = Field(default_factory=list)


class CitationItem(ApiModel):
    id: str = Field(max_length=64)
    mission_id: str = Field(max_length=64)
    input_id: str = Field(max_length=64)
    agent_code: str = Field(max_length=64)
    excerpt: str = Field(max_length=2000)
    locator: str | None = Field(default=None, max_length=500)
    score: float | None = None
    display_name: str | None = Field(default=None, max_length=200)
    created_at: str = Field(default_factory=utc_now)


class SearchMissionInputsResponse(ApiModel):
    results: list[CitationItem]
