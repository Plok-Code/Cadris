from __future__ import annotations

from datetime import UTC, datetime
from sqlalchemy import Boolean, ForeignKey, Integer, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class Base(DeclarativeBase):
    pass


class UserRecord(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    plan: Mapped[str] = mapped_column(default="core")
    created_at: Mapped[str] = mapped_column(default=utc_now)

    projects: Mapped[list["ProjectRecord"]] = relationship(back_populates="user")


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
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[str] = mapped_column(default=utc_now)

    mission: Mapped[MissionRecord] = relationship(back_populates="inputs")


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
