from __future__ import annotations

import json


from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from ..models import (
    ArtifactBlock,
    ArtifactSectionItem,
    CertaintyEntry,
    CitationItem,
    DossierReadModel,
    ExportReadModel,
    MissionAgent,
    MissionInputItem,
    MissionMessage,
    MissionQuestion,
    MissionReadModel,
    ProjectSummary,
)
from ..records import (
    AgentRunRecord,
    ArtifactRecord,
    CitationRecord,
    DossierRecord,
    ExportRecord,
    MissionAgentRecord,
    MissionInputRecord,
    MissionMessageRecord,
    MissionQuestionRecord,
    MissionRecord,
    PasswordResetTokenRecord,
    ProjectRecord,
    UserRecord,
)


from ..models.base import utc_now  # single source of truth — no duplicates


class BaseRepository:
    """Base repository with session management and shared helpers."""

    def __init__(self, session: Session) -> None:
        self.session = session

    # ── Shared static helpers ────────────────────────────────

    @staticmethod
    def _to_mission_read_model(record: MissionRecord) -> MissionReadModel:
        inputs = sorted(record.inputs, key=lambda item: item.sort_order)
        artifacts = sorted(record.artifacts, key=lambda item: item.sort_order)
        agents = sorted(record.agents, key=lambda item: item.sort_order)
        messages = sorted(record.messages, key=lambda item: item.sort_order)
        questions = sorted(record.questions, key=lambda item: (item.sort_order, item.created_at))
        active_question = next((item for item in questions if item.status == "waiting"), None)
        return MissionReadModel(
            id=record.id,
            project_id=record.project_id,
            flow_code=record.flow_code,
            flow_label=record.flow_label,
            title=record.title,
            status=record.status,
            summary=record.summary,
            next_step=record.next_step,
            intake_text=record.intake_text,
            inputs=[BaseRepository._to_mission_input_item(item) for item in inputs],
            artifact_blocks=[
                ArtifactBlock(
                    id=item.id,
                    title=item.title,
                    status=item.status,
                    certainty=item.certainty,
                    summary=item.summary,
                    content=item.content,
                    sections=[
                        ArtifactSectionItem(**s)
                        for s in json.loads(item.sections_json or "[]")
                    ],
                )
                for item in artifacts
            ],
            active_question=(
                MissionQuestion(
                    id=active_question.id,
                    title=active_question.title,
                    body=active_question.body,
                    status=active_question.status,
                    answer_text=active_question.answer_text,
                )
                if active_question is not None
                else None
            ),
            question_history=[
                MissionQuestion(
                    id=item.id,
                    title=item.title,
                    body=item.body,
                    status=item.status,
                    answer_text=item.answer_text,
                )
                for item in questions
            ],
            certainty_entries=[
                CertaintyEntry(
                    id=f"{item.id}:certainty",
                    title=item.summary,
                    status=item.certainty,
                    impact=BaseRepository._certainty_impact(item.certainty),
                    source_label=item.title,
                )
                for item in artifacts
            ],
            active_agents=[
                MissionAgent(
                    code=item.code,
                    label=item.label,
                    role=item.role,
                    status=item.status,
                    prompt_key=item.prompt_key,
                    prompt_version=item.prompt_version,
                    summary=item.summary,
                )
                for item in agents
            ],
            recent_messages=[
                MissionMessage(
                    id=item.id,
                    agent_code=item.agent_code,
                    agent_label=item.agent_label,
                    stage=item.stage,
                    title=item.title,
                    body=item.body,
                    created_at=item.created_at,
                )
                for item in messages
            ],
            timeline=json.loads(record.timeline_json),
            dossier_ready=record.dossier_ready,
            updated_at=record.updated_at,
        )

    @staticmethod
    def _certainty_impact(certainty: str) -> str:
        if certainty == "solid":
            return "Ce point peut servir d'appui direct pour la transmission."
        if certainty == "to_confirm":
            return "Ce point tient, mais doit encore etre confirme avant de figer le dossier."
        if certainty == "blocking":
            return "Ce point fragilise fortement le dossier et peut bloquer la suite."
        return "Ce point reste insuffisamment connu et limite la qualite de decision."

    @staticmethod
    def _to_mission_input_item(record: MissionInputRecord) -> MissionInputItem:
        return MissionInputItem(
            id=record.id,
            kind=record.kind,
            source=record.source,
            content=record.content,
            display_name=record.display_name,
            mime_type=record.mime_type,
            byte_size=record.byte_size,
            preview_text=record.preview_text,
            openai_file_id=record.openai_file_id,
            vector_store_id=record.vector_store_id,
            created_at=record.created_at,
        )

    @staticmethod
    def _to_dossier_read_model(record: DossierRecord) -> DossierReadModel:
        return DossierReadModel(
            mission_id=record.mission_id,
            title=record.title,
            quality_label=record.quality_label,
            summary=record.summary,
            markdown=record.markdown,
            sections=json.loads(record.sections_json),
            updated_at=record.updated_at,
        )

    @staticmethod
    def _to_export_read_model(record: ExportRecord) -> ExportReadModel:
        return ExportReadModel(
            id=record.id,
            mission_id=record.mission_id,
            bundle_type=record.bundle_type,
            format=record.format,
            snapshot_version=record.snapshot_version,
            partial=record.partial,
            token=None,  # Never expose raw tokens in API responses
            file_url=record.file_url,
            revoked=record.revoked,
            created_at=record.created_at,
        )

    @staticmethod
    def _to_project_summary(record: ProjectRecord) -> ProjectSummary:
        return ProjectSummary(
            id=record.id,
            name=record.name,
            mission_count=record.mission_count,
            active_mission_id=record.active_mission_id,
            active_mission_status=record.active_mission_status,
            updated_at=record.updated_at,
        )
