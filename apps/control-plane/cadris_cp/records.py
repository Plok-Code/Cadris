from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from .models.base import utc_now  # single source of truth


class Base(DeclarativeBase):
    pass


class UserRecord(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str | None] = mapped_column(Text(), nullable=True)
    plan: Mapped[str] = mapped_column(default="free")
    stripe_customer_id: Mapped[str | None] = mapped_column(Text(), nullable=True, index=True)
    plan_expires_at: Mapped[str | None] = mapped_column(Text(), nullable=True)
    missions_this_month: Mapped[int] = mapped_column(Integer, default=0)
    month_reset_at: Mapped[str | None] = mapped_column(Text(), nullable=True)
    password_hash: Mapped[str | None] = mapped_column(Text(), nullable=True)
    created_at: Mapped[str] = mapped_column(default=utc_now)

    projects: Mapped[list["ProjectRecord"]] = relationship(back_populates="user")


class PasswordResetTokenRecord(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[str] = mapped_column(Text())
    expires_at: Mapped[str] = mapped_column(Text())
    used: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[str] = mapped_column(default=utc_now)


class ProjectRecord(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(default="active")
    mission_count: Mapped[int] = mapped_column(Integer, default=0)
    active_mission_id: Mapped[str | None] = mapped_column(nullable=True)
    active_mission_status: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[str] = mapped_column(default=utc_now)
    updated_at: Mapped[str] = mapped_column(default=utc_now)

    user: Mapped[UserRecord] = relationship(back_populates="projects")
    missions: Mapped[list["MissionRecord"]] = relationship(back_populates="project")


class MissionRecord(Base):
    __tablename__ = "missions"

    id: Mapped[str] = mapped_column(primary_key=True)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), index=True)
    flow_code: Mapped[str] = mapped_column(default="demarrage")
    flow_label: Mapped[str] = mapped_column(default="Nouveau projet")
    title: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(default="draft")
    summary: Mapped[str] = mapped_column(Text())
    next_step: Mapped[str] = mapped_column(Text())
    intake_text: Mapped[str] = mapped_column(Text())
    timeline_json: Mapped[str] = mapped_column(Text())
    dossier_ready: Mapped[bool] = mapped_column(Boolean, default=False)
    phase: Mapped[str] = mapped_column(Text(), default="intake")
    current_wave: Mapped[int] = mapped_column(Integer, default=0)
    qualification_answers_json: Mapped[str] = mapped_column(Text(), default="{}")
    qualification_questions_json: Mapped[str] = mapped_column(Text(), default="[]")
    created_at: Mapped[str] = mapped_column(default=utc_now)
    updated_at: Mapped[str] = mapped_column(default=utc_now)

    project: Mapped[ProjectRecord] = relationship(back_populates="missions")
    dossier: Mapped["DossierRecord | None"] = relationship(back_populates="mission")
    inputs: Mapped[list["MissionInputRecord"]] = relationship(back_populates="mission")
    agent_runs: Mapped[list["AgentRunRecord"]] = relationship(back_populates="mission")
    agents: Mapped[list["MissionAgentRecord"]] = relationship(back_populates="mission")
    messages: Mapped[list["MissionMessageRecord"]] = relationship(back_populates="mission")
    questions: Mapped[list["MissionQuestionRecord"]] = relationship(back_populates="mission")
    artifacts: Mapped[list["ArtifactRecord"]] = relationship(back_populates="mission")
    citations: Mapped[list["CitationRecord"]] = relationship(back_populates="mission")


class MissionInputRecord(Base):
    __tablename__ = "mission_inputs"

    id: Mapped[str] = mapped_column(primary_key=True)
    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(Text())
    source: Mapped[str] = mapped_column(Text())
    content: Mapped[str] = mapped_column(Text())
    display_name: Mapped[str | None] = mapped_column(Text(), nullable=True)
    mime_type: Mapped[str | None] = mapped_column(Text(), nullable=True)
    byte_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    storage_path: Mapped[str | None] = mapped_column(Text(), nullable=True)
    preview_text: Mapped[str | None] = mapped_column(Text(), nullable=True)
    openai_file_id: Mapped[str | None] = mapped_column(Text(), nullable=True)
    vector_store_id: Mapped[str | None] = mapped_column(Text(), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[str] = mapped_column(default=utc_now)

    mission: Mapped[MissionRecord] = relationship(back_populates="inputs")
    citations: Mapped[list["CitationRecord"]] = relationship(back_populates="input")


class AgentRunRecord(Base):
    __tablename__ = "agent_runs"

    id: Mapped[str] = mapped_column(primary_key=True)
    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(Text())
    idempotency_key: Mapped[str] = mapped_column(Text(), unique=True)
    started_at: Mapped[str] = mapped_column(default=utc_now)
    ended_at: Mapped[str | None] = mapped_column(nullable=True)
    created_at: Mapped[str] = mapped_column(default=utc_now)

    mission: Mapped[MissionRecord] = relationship(back_populates="agent_runs")


class MissionAgentRecord(Base):
    __tablename__ = "mission_agents"

    id: Mapped[str] = mapped_column(primary_key=True)
    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), index=True)
    code: Mapped[str] = mapped_column(Text())
    label: Mapped[str] = mapped_column(Text())
    role: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(Text())
    prompt_key: Mapped[str] = mapped_column(Text())
    prompt_version: Mapped[str] = mapped_column(Text())
    summary: Mapped[str] = mapped_column(Text())
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[str] = mapped_column(default=utc_now)
    updated_at: Mapped[str] = mapped_column(default=utc_now)

    mission: Mapped[MissionRecord] = relationship(back_populates="agents")


class MissionMessageRecord(Base):
    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(primary_key=True)
    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), index=True)
    agent_code: Mapped[str] = mapped_column(Text())
    agent_label: Mapped[str] = mapped_column(Text())
    stage: Mapped[str] = mapped_column(Text())
    title: Mapped[str] = mapped_column(Text())
    body: Mapped[str] = mapped_column(Text())
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[str] = mapped_column(default=utc_now)

    mission: Mapped[MissionRecord] = relationship(back_populates="messages")


class MissionQuestionRecord(Base):
    __tablename__ = "mission_questions"

    id: Mapped[str] = mapped_column(primary_key=True)
    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(Text())
    body: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(Text())
    answer_text: Mapped[str | None] = mapped_column(Text(), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[str] = mapped_column(default=utc_now)
    updated_at: Mapped[str] = mapped_column(default=utc_now)

    mission: Mapped[MissionRecord] = relationship(back_populates="questions")


class ArtifactRecord(Base):
    __tablename__ = "artifacts"

    id: Mapped[str] = mapped_column(primary_key=True)
    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(Text())
    status: Mapped[str] = mapped_column(Text())
    certainty: Mapped[str] = mapped_column(Text())
    summary: Mapped[str] = mapped_column(Text())
    content: Mapped[str] = mapped_column(Text())
    sections_json: Mapped[str] = mapped_column(Text(), default="[]")
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[str] = mapped_column(default=utc_now)
    updated_at: Mapped[str] = mapped_column(default=utc_now)

    mission: Mapped[MissionRecord] = relationship(back_populates="artifacts")


class DossierRecord(Base):
    __tablename__ = "dossiers"

    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), primary_key=True)
    title: Mapped[str] = mapped_column(Text())
    quality_label: Mapped[str] = mapped_column(Text())
    summary: Mapped[str] = mapped_column(Text())
    markdown: Mapped[str] = mapped_column(Text())
    sections_json: Mapped[str] = mapped_column(Text())
    created_at: Mapped[str] = mapped_column(default=utc_now)
    updated_at: Mapped[str] = mapped_column(default=utc_now)

    mission: Mapped[MissionRecord] = relationship(back_populates="dossier")


class ExportRecord(Base):
    __tablename__ = "exports"

    id: Mapped[str] = mapped_column(primary_key=True)
    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), index=True)
    bundle_type: Mapped[str] = mapped_column(Text(), default="MissionDossier")
    format: Mapped[str] = mapped_column(Text())
    snapshot_version: Mapped[int] = mapped_column(Integer, default=1)
    partial: Mapped[bool] = mapped_column(Boolean, default=False)
    token: Mapped[str | None] = mapped_column(Text(), unique=True, nullable=True)
    token_hash: Mapped[str | None] = mapped_column(Text(), nullable=True)
    file_url: Mapped[str | None] = mapped_column(Text(), nullable=True)
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    expires_at: Mapped[str | None] = mapped_column(Text(), nullable=True)
    created_at: Mapped[str] = mapped_column(default=utc_now)
    revoked_at: Mapped[str | None] = mapped_column(nullable=True)

    mission: Mapped[MissionRecord] = relationship()


class CitationRecord(Base):
    __tablename__ = "citations"

    id: Mapped[str] = mapped_column(primary_key=True)
    mission_id: Mapped[str] = mapped_column(ForeignKey("missions.id", ondelete="CASCADE"), index=True)
    input_id: Mapped[str] = mapped_column(ForeignKey("mission_inputs.id", ondelete="CASCADE"), index=True)
    agent_code: Mapped[str] = mapped_column(Text())
    excerpt: Mapped[str] = mapped_column(Text())
    locator: Mapped[str | None] = mapped_column(Text(), nullable=True)
    score: Mapped[float | None] = mapped_column(nullable=True)
    created_at: Mapped[str] = mapped_column(default=utc_now)

    mission: Mapped[MissionRecord] = relationship(back_populates="citations")
    input: Mapped[MissionInputRecord] = relationship(back_populates="citations")
