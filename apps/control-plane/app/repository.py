from __future__ import annotations

import json
from datetime import UTC, datetime
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session
from .models import (
    ArtifactBlock,
    CertaintyEntry,
    CitationItem,
    DossierReadModel,
    ExportReadModel,
    MissionInputItem,
    MissionAgent,
    MissionMessage,
    MissionQuestion,
    MissionReadModel,
    ProjectSummary,
)
from .records import (
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


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class ControlPlaneRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def recover_stale_runs(self) -> int:
        """Mark any runs still in 'running' status as 'interrupted'.

        Called at startup to clean up runs that were in progress when
        the server was last shut down or crashed.
        """
        stale = (
            self.session.query(AgentRunRecord)
            .filter(AgentRunRecord.status == "running")
            .all()
        )
        for run in stale:
            run.status = "interrupted"
            run.ended_at = utc_now()
        if stale:
            self.session.commit()
        return len(stale)

    def get_user(self, user_id: str) -> UserRecord | None:
        return self.session.get(UserRecord, user_id)

    def ensure_user(self, user_id: str, email: str) -> UserRecord:
        user = self.session.get(UserRecord, user_id)
        if user is None:
            # Check if email already exists (e.g., user switched auth provider)
            existing = self.session.execute(
                select(UserRecord).where(UserRecord.email == email)
            ).scalar_one_or_none()
            if existing is not None:
                return existing
            user = UserRecord(id=user_id, email=email)
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
        return user

    def list_missions_for_user(self, user_id: str) -> list[dict]:
        """List all missions for a user with basic info (for the Mes projets page)."""
        statement = (
            select(MissionRecord)
            .join(ProjectRecord, MissionRecord.project_id == ProjectRecord.id)
            .where(ProjectRecord.user_id == user_id)
            .order_by(MissionRecord.created_at.desc())
        )
        results = []
        for m in self.session.scalars(statement).all():
            # Count sections in dossier if it exists
            section_count = 0
            dossier = self.session.get(DossierRecord, m.id)
            if dossier and dossier.sections_json:
                try:
                    section_count = len(json.loads(dossier.sections_json))
                except Exception:
                    pass
            results.append({
                "id": m.id,
                "title": m.title,
                "status": m.status,
                "dossierReady": bool(m.dossier_ready),
                "sectionCount": section_count,
                "createdAt": m.created_at,
                "updatedAt": m.updated_at,
                "projectId": m.project_id,
                "intakeText": (m.intake_text or "")[:200],
            })
        return results

    def delete_mission(self, mission_id: str) -> None:
        """Delete a mission and its associated dossier/exports."""
        # Delete dossier
        dossier = self.session.get(DossierRecord, mission_id)
        if dossier:
            self.session.delete(dossier)
        # Delete exports
        self.session.execute(
            delete(ExportRecord).where(ExportRecord.mission_id == mission_id)
        )
        # Delete mission (cascades to agents, artifacts, etc.)
        mission = self.session.get(MissionRecord, mission_id)
        if mission:
            self.session.delete(mission)
        self.session.commit()

    def list_projects_for_user(self, user_id: str) -> list[ProjectSummary]:
        statement = (
            select(ProjectRecord)
            .where(ProjectRecord.user_id == user_id)
            .order_by(ProjectRecord.updated_at.desc())
        )
        return [self._to_project_summary(row) for row in self.session.scalars(statement).all()]

    def create_project(self, *, user_id: str, project_id: str, name: str) -> ProjectSummary:
        record = ProjectRecord(
            id=project_id,
            user_id=user_id,
            name=name,
            created_at=utc_now(),
            updated_at=utc_now(),
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return self._to_project_summary(record)

    def get_project_for_user(self, user_id: str, project_id: str) -> ProjectSummary | None:
        statement = select(ProjectRecord).where(
            ProjectRecord.id == project_id,
            ProjectRecord.user_id == user_id,
        )
        record = self.session.scalar(statement)
        if record is None:
            return None
        return self._to_project_summary(record)

    def update_project_after_mission(
        self,
        *,
        project_id: str,
        active_mission_id: str,
        active_mission_status: str,
        mission_delta: int = 0,
    ) -> ProjectSummary:
        record = self.session.get(ProjectRecord, project_id)
        if record is None:
            raise ValueError("Project not found")

        record.active_mission_id = active_mission_id
        record.active_mission_status = active_mission_status
        record.mission_count += mission_delta
        record.updated_at = utc_now()
        self.session.commit()
        self.session.refresh(record)
        return self._to_project_summary(record)

    def create_agent_run(self, *, mission_id: str, run_id: str, kind: str, idempotency_key: str) -> str:
        record = AgentRunRecord(
            id=run_id,
            mission_id=mission_id,
            kind=kind,
            status="running",
            idempotency_key=idempotency_key,
            started_at=utc_now(),
            created_at=utc_now(),
        )
        self.session.add(record)
        self.session.commit()
        return record.id

    def update_agent_run(self, *, run_id: str, status: str) -> None:
        record = self.session.get(AgentRunRecord, run_id)
        if record is None:
            raise ValueError("Agent run not found")
        record.status = status
        record.ended_at = utc_now()
        self.session.commit()

    def append_mission_input(self, *, mission_id: str, kind: str, source: str, content: str) -> None:
        self.create_mission_input(mission_id=mission_id, kind=kind, source=source, content=content)

    def create_mission_input(
        self,
        *,
        mission_id: str,
        kind: str,
        source: str,
        content: str,
        input_id: str | None = None,
        display_name: str | None = None,
        mime_type: str | None = None,
        byte_size: int | None = None,
        storage_path: str | None = None,
        preview_text: str | None = None,
        openai_file_id: str | None = None,
        vector_store_id: str | None = None,
    ) -> MissionInputItem:
        sort_order = (
            self.session.scalar(
                select(func.count(MissionInputRecord.id)).where(MissionInputRecord.mission_id == mission_id)
            )
            or 0
        )
        record = MissionInputRecord(
            id=input_id or f"{mission_id}:{kind}:{sort_order}",
            mission_id=mission_id,
            kind=kind,
            source=source,
            content=content,
            display_name=display_name,
            mime_type=mime_type,
            byte_size=byte_size,
            storage_path=storage_path,
            preview_text=preview_text,
            openai_file_id=openai_file_id,
            vector_store_id=vector_store_id,
            sort_order=sort_order,
            created_at=utc_now(),
        )
        self.session.add(record)
        self.session.commit()
        return self._to_mission_input_item(record)

    def update_mission_input_file_search(
        self,
        *,
        input_id: str,
        openai_file_id: str,
        vector_store_id: str,
    ) -> None:
        record = self.session.get(MissionInputRecord, input_id)
        if record is None:
            return
        record.openai_file_id = openai_file_id
        record.vector_store_id = vector_store_id
        self.session.commit()

    def list_mission_inputs(self, mission_id: str) -> list[MissionInputRecord]:
        return list(
            self.session.scalars(
                select(MissionInputRecord).where(MissionInputRecord.mission_id == mission_id)
            ).all()
        )

    def get_mission_input_for_user(self, user_id: str, mission_id: str, input_id: str) -> MissionInputRecord | None:
        statement = (
            select(MissionInputRecord)
            .join(MissionRecord, MissionInputRecord.mission_id == MissionRecord.id)
            .join(ProjectRecord, MissionRecord.project_id == ProjectRecord.id)
            .where(
                MissionInputRecord.id == input_id,
                MissionInputRecord.mission_id == mission_id,
                ProjectRecord.user_id == user_id,
            )
        )
        return self.session.scalar(statement)

    def upsert_question(self, *, mission_id: str, question: MissionQuestion | None) -> None:
        if question is None:
            self.session.commit()
            return

        record = self.session.get(MissionQuestionRecord, question.id)
        if record is None:
            sort_order = (
                self.session.scalar(
                    select(func.count(MissionQuestionRecord.id)).where(MissionQuestionRecord.mission_id == mission_id)
                )
                or 0
            )
            record = MissionQuestionRecord(
                id=question.id,
                mission_id=mission_id,
                sort_order=sort_order,
                created_at=utc_now(),
            )
            self.session.add(record)

        record.title = question.title
        record.body = question.body
        record.status = question.status
        record.answer_text = question.answer_text
        record.updated_at = utc_now()
        self.session.commit()

    def answer_latest_question(self, *, mission_id: str, answer_text: str) -> None:
        statement = (
            select(MissionQuestionRecord)
            .where(MissionQuestionRecord.mission_id == mission_id)
            .order_by(MissionQuestionRecord.sort_order.desc(), MissionQuestionRecord.created_at.desc())
        )
        record = self.session.scalar(statement)
        if record is None:
            return
        record.status = "answered"
        record.answer_text = answer_text
        record.updated_at = utc_now()
        self.session.commit()

    def replace_mission_agents(self, *, mission_id: str, agents: list[MissionAgent]) -> None:
        self.session.execute(delete(MissionAgentRecord).where(MissionAgentRecord.mission_id == mission_id))
        for index, agent in enumerate(agents):
            self.session.add(
                MissionAgentRecord(
                    id=f"{mission_id}:{agent.code}",
                    mission_id=mission_id,
                    code=agent.code,
                    label=agent.label,
                    role=agent.role,
                    status=agent.status,
                    prompt_key=agent.prompt_key,
                    prompt_version=agent.prompt_version,
                    summary=agent.summary,
                    sort_order=index,
                    created_at=utc_now(),
                    updated_at=utc_now(),
                )
            )
        self.session.commit()

    def replace_messages(self, *, mission_id: str, messages: list[MissionMessage]) -> None:
        self.session.execute(delete(MissionMessageRecord).where(MissionMessageRecord.mission_id == mission_id))
        for index, message in enumerate(messages):
            self.session.add(
                MissionMessageRecord(
                    id=message.id,
                    mission_id=mission_id,
                    agent_code=message.agent_code,
                    agent_label=message.agent_label,
                    stage=message.stage,
                    title=message.title,
                    body=message.body,
                    sort_order=index,
                    created_at=message.created_at,
                )
            )
        self.session.commit()

    def upsert_mission(self, mission: MissionReadModel) -> MissionReadModel:
        record = self.session.get(MissionRecord, mission.id)
        if record is None:
            record = MissionRecord(id=mission.id, project_id=mission.project_id, created_at=utc_now())
            self.session.add(record)

        record.flow_code = mission.flow_code
        record.flow_label = mission.flow_label
        record.title = mission.title
        record.status = mission.status
        record.summary = mission.summary
        record.next_step = mission.next_step
        record.intake_text = mission.intake_text
        record.timeline_json = json.dumps(
            [item.model_dump(mode="json", by_alias=True) for item in mission.timeline],
            ensure_ascii=True,
        )
        record.dossier_ready = mission.dossier_ready
        record.updated_at = utc_now()

        self.session.flush()
        self.session.execute(delete(ArtifactRecord).where(ArtifactRecord.mission_id == mission.id))
        for index, artifact in enumerate(mission.artifact_blocks):
            self.session.add(
                ArtifactRecord(
                    id=artifact.id,
                    mission_id=mission.id,
                    title=artifact.title,
                    status=artifact.status,
                    certainty=artifact.certainty,
                    summary=artifact.summary,
                    content=artifact.content,
                    sort_order=index,
                    created_at=utc_now(),
                    updated_at=utc_now(),
                )
            )
        self.session.commit()
        self.session.refresh(record)
        return self._to_mission_read_model(record)

    def get_mission_for_user(self, user_id: str, mission_id: str) -> MissionReadModel | None:
        statement = (
            select(MissionRecord)
            .join(ProjectRecord, MissionRecord.project_id == ProjectRecord.id)
            .where(MissionRecord.id == mission_id, ProjectRecord.user_id == user_id)
        )
        record = self.session.scalar(statement)
        if record is None:
            return None
        return self._to_mission_read_model(record)

    def upsert_dossier(self, dossier: DossierReadModel) -> DossierReadModel:
        record = self.session.get(DossierRecord, dossier.mission_id)
        if record is None:
            record = DossierRecord(mission_id=dossier.mission_id, created_at=utc_now())
            self.session.add(record)

        record.title = dossier.title
        record.quality_label = dossier.quality_label
        record.summary = dossier.summary
        record.markdown = dossier.markdown
        record.sections_json = json.dumps(
            [item.model_dump(mode="json", by_alias=True) for item in dossier.sections],
            ensure_ascii=True,
        )
        record.updated_at = utc_now()

        self.session.commit()
        self.session.refresh(record)
        return self._to_dossier_read_model(record)

    def get_dossier(self, mission_id: str) -> DossierReadModel | None:
        """Get dossier by mission_id (no user ownership check — for internal merging)."""
        record = self.session.get(DossierRecord, mission_id)
        if record is None:
            return None
        return self._to_dossier_read_model(record)

    def get_dossier_for_user(self, user_id: str, mission_id: str) -> DossierReadModel | None:
        statement = (
            select(DossierRecord)
            .join(MissionRecord, DossierRecord.mission_id == MissionRecord.id)
            .join(ProjectRecord, MissionRecord.project_id == ProjectRecord.id)
            .where(DossierRecord.mission_id == mission_id, ProjectRecord.user_id == user_id)
        )
        record = self.session.scalar(statement)
        if record is None:
            return None
        return self._to_dossier_read_model(record)

    # ── Mission persistence helpers ──────────────────────────

    def update_mission_phase(self, mission_id: str, phase: str) -> None:
        record = self.session.get(MissionRecord, mission_id)
        if record:
            record.phase = phase
            record.updated_at = utc_now()
            self.session.commit()

    def update_mission_wave(self, mission_id: str, wave: int) -> None:
        record = self.session.get(MissionRecord, mission_id)
        if record:
            record.current_wave = wave
            record.updated_at = utc_now()
            self.session.commit()

    def save_qualification_answers(self, mission_id: str, answers: dict[str, str]) -> None:
        record = self.session.get(MissionRecord, mission_id)
        if record:
            record.qualification_answers_json = json.dumps(answers, ensure_ascii=False)
            record.updated_at = utc_now()
            self.session.commit()

    def save_qualification_questions(self, mission_id: str, questions: list[dict]) -> None:
        record = self.session.get(MissionRecord, mission_id)
        if record:
            record.qualification_questions_json = json.dumps(questions, ensure_ascii=False)
            record.updated_at = utc_now()
            self.session.commit()

    def update_dossier_doc_status(
        self,
        mission_id: str,
        validated_ids: list[str],
        corrections: dict[str, str],
    ) -> None:
        """Update validated/correction fields on dossier sections."""
        from .models import DossierSection as DossierSectionModel

        record = self.session.get(DossierRecord, mission_id)
        if not record or not record.sections_json:
            return

        sections = json.loads(record.sections_json)
        for section in sections:
            sid = section.get("id", "")
            if sid in validated_ids:
                section["validated"] = True
            if sid in corrections:
                section["correction"] = corrections[sid]

        record.sections_json = json.dumps(sections, ensure_ascii=False)
        record.updated_at = utc_now()
        self.session.commit()

    def get_mission_state(self, user_id: str, mission_id: str) -> dict | None:
        """Get full mission state for resume, including dossier sections and questions."""
        statement = (
            select(MissionRecord)
            .join(ProjectRecord, MissionRecord.project_id == ProjectRecord.id)
            .where(MissionRecord.id == mission_id, ProjectRecord.user_id == user_id)
        )
        record = self.session.scalar(statement)
        if record is None:
            return None

        # Load dossier sections
        documents = []
        dossier = self.session.get(DossierRecord, mission_id)
        if dossier and dossier.sections_json:
            try:
                documents = json.loads(dossier.sections_json)
            except Exception:
                pass

        # Load question history
        questions = sorted(record.questions, key=lambda q: (q.sort_order, q.created_at))
        question_history = [
            {
                "id": q.id,
                "title": q.title,
                "body": q.body,
                "status": q.status,
                "answerText": q.answer_text,
            }
            for q in questions
        ]

        # Parse qualification answers
        try:
            qual_answers = json.loads(record.qualification_answers_json or "{}")
        except Exception:
            qual_answers = {}

        # Parse qualification questions
        try:
            qual_questions = json.loads(record.qualification_questions_json or "[]")
        except Exception:
            qual_questions = []

        return {
            "id": record.id,
            "phase": record.phase or "intake",
            "currentWave": record.current_wave or 0,
            "intakeText": record.intake_text or "",
            "qualificationAnswers": qual_answers,
            "qualificationQuestions": qual_questions,
            "documents": documents,
            "dossierReady": bool(record.dossier_ready),
            "questionHistory": question_history,
        }

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
            inputs=[ControlPlaneRepository._to_mission_input_item(item) for item in inputs],
            artifact_blocks=[
                ArtifactBlock(
                    id=item.id,
                    title=item.title,
                    status=item.status,
                    certainty=item.certainty,
                    summary=item.summary,
                    content=item.content,
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
                    impact=ControlPlaneRepository._certainty_impact(item.certainty),
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

    def create_citation(
        self,
        *,
        citation_id: str,
        mission_id: str,
        input_id: str,
        agent_code: str,
        excerpt: str,
        locator: str | None = None,
        score: float | None = None,
    ) -> CitationItem:
        record = CitationRecord(
            id=citation_id,
            mission_id=mission_id,
            input_id=input_id,
            agent_code=agent_code,
            excerpt=excerpt,
            locator=locator,
            score=score,
            created_at=utc_now(),
        )
        self.session.add(record)
        self.session.commit()
        input_record = self.session.get(MissionInputRecord, input_id)
        return CitationItem(
            id=record.id,
            mission_id=record.mission_id,
            input_id=record.input_id,
            agent_code=record.agent_code,
            excerpt=record.excerpt,
            locator=record.locator,
            score=record.score,
            display_name=input_record.display_name if input_record else None,
            created_at=record.created_at,
        )

    def list_citations_for_mission(self, mission_id: str) -> list[CitationItem]:
        statement = (
            select(CitationRecord)
            .where(CitationRecord.mission_id == mission_id)
            .order_by(CitationRecord.created_at)
        )
        records = self.session.scalars(statement).all()
        result: list[CitationItem] = []
        for rec in records:
            input_record = self.session.get(MissionInputRecord, rec.input_id)
            result.append(
                CitationItem(
                    id=rec.id,
                    mission_id=rec.mission_id,
                    input_id=rec.input_id,
                    agent_code=rec.agent_code,
                    excerpt=rec.excerpt,
                    locator=rec.locator,
                    score=rec.score,
                    display_name=input_record.display_name if input_record else None,
                    created_at=rec.created_at,
                )
            )
        return result

    def get_vector_store_id_for_mission(self, mission_id: str) -> str | None:
        statement = (
            select(MissionInputRecord.vector_store_id)
            .where(
                MissionInputRecord.mission_id == mission_id,
                MissionInputRecord.vector_store_id.isnot(None),
            )
            .limit(1)
        )
        return self.session.scalar(statement)

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

    def create_export(
        self,
        *,
        export_id: str,
        mission_id: str,
        format: str,
        token: str | None = None,
        bundle_type: str = "MissionDossier",
    ) -> ExportReadModel:
        record = ExportRecord(
            id=export_id,
            mission_id=mission_id,
            bundle_type=bundle_type,
            format=format,
            token=token,
            created_at=utc_now(),
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return self._to_export_read_model(record)

    def get_export_by_token(self, token: str) -> ExportRecord | None:
        statement = select(ExportRecord).where(
            ExportRecord.token == token,
            ExportRecord.revoked == False,  # noqa: E712
        )
        return self.session.scalar(statement)

    def revoke_export(self, export_id: str, user_id: str) -> ExportReadModel | None:
        statement = (
            select(ExportRecord)
            .join(MissionRecord, ExportRecord.mission_id == MissionRecord.id)
            .join(ProjectRecord, MissionRecord.project_id == ProjectRecord.id)
            .where(ExportRecord.id == export_id, ProjectRecord.user_id == user_id)
        )
        record = self.session.scalar(statement)
        if record is None:
            return None
        record.revoked = True
        record.revoked_at = utc_now()
        self.session.commit()
        self.session.refresh(record)
        return self._to_export_read_model(record)

    def list_exports_for_mission(self, mission_id: str) -> list[ExportReadModel]:
        statement = (
            select(ExportRecord)
            .where(ExportRecord.mission_id == mission_id)
            .order_by(ExportRecord.created_at.desc())
        )
        return [self._to_export_read_model(r) for r in self.session.scalars(statement).all()]

    @staticmethod
    def _to_export_read_model(record: ExportRecord) -> ExportReadModel:
        return ExportReadModel(
            id=record.id,
            mission_id=record.mission_id,
            bundle_type=record.bundle_type,
            format=record.format,
            snapshot_version=record.snapshot_version,
            partial=record.partial,
            token=record.token,
            file_url=record.file_url,
            revoked=record.revoked,
            created_at=record.created_at,
        )

    # ── Auth (email + password) ──────────────────────────────────────

    def get_user_by_email(self, email: str) -> UserRecord | None:
        statement = select(UserRecord).where(UserRecord.email == email)
        return self.session.scalar(statement)

    def register_user(
        self, *, user_id: str, email: str, name: str, password_hash: str
    ) -> UserRecord:
        user = UserRecord(
            id=user_id,
            email=email,
            name=name or None,
            password_hash=password_hash,
            plan="free",
            created_at=utc_now(),
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_password_hash(self, *, user_id: str, password_hash: str) -> None:
        user = self.session.get(UserRecord, user_id)
        if user:
            user.password_hash = password_hash
            self.session.commit()

    def create_password_reset_token(
        self, *, token_id: str, user_id: str, token_hash: str, expires_at: str
    ) -> None:
        record = PasswordResetTokenRecord(
            id=token_id,
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            created_at=utc_now(),
        )
        self.session.add(record)
        self.session.commit()

    def get_valid_reset_token(self, token_hash: str) -> PasswordResetTokenRecord | None:
        statement = select(PasswordResetTokenRecord).where(
            PasswordResetTokenRecord.token_hash == token_hash,
            PasswordResetTokenRecord.used == 0,
        )
        return self.session.scalar(statement)

    def mark_reset_token_used(self, token_id: str) -> None:
        record = self.session.get(PasswordResetTokenRecord, token_id)
        if record:
            record.used = 1
            self.session.commit()

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
