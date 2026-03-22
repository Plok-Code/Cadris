from __future__ import annotations

import json

from sqlalchemy import delete, func, select
from sqlalchemy.orm import selectinload

from .base import utc_now
from ..models import (
    MissionAgent,
    MissionMessage,
    MissionQuestion,
    MissionReadModel,
)
from ..records import (
    AgentRunRecord,
    ArtifactRecord,
    DossierRecord,
    ExportRecord,
    MissionAgentRecord,
    MissionInputRecord,
    MissionMessageRecord,
    MissionQuestionRecord,
    MissionRecord,
    ProjectRecord,
)


class MissionRepoMixin:
    """Mission-related repository methods."""

    def recover_stale_runs(self) -> int:
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

    def create_mission(self, mission: MissionReadModel) -> MissionReadModel:
        """Alias for upsert_mission (kept for backward compat)."""
        return self.upsert_mission(mission)

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
                    sections_json=json.dumps(
                        [s.model_dump(mode="json", by_alias=True) for s in artifact.sections],
                        ensure_ascii=True,
                    ),
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
            .options(
                selectinload(MissionRecord.inputs),
                selectinload(MissionRecord.artifacts),
                selectinload(MissionRecord.agents),
                selectinload(MissionRecord.messages),
                selectinload(MissionRecord.questions),
            )
        )
        record = self.session.scalar(statement)
        if record is None:
            return None
        return self._to_mission_read_model(record)

    def delete_mission(self, mission_id: str) -> None:
        dossier = self.session.get(DossierRecord, mission_id)
        if dossier:
            self.session.delete(dossier)
        self.session.execute(
            delete(ExportRecord).where(ExportRecord.mission_id == mission_id)
        )
        mission = self.session.get(MissionRecord, mission_id)
        if mission:
            self.session.delete(mission)
        self.session.commit()

    def list_missions_for_user(self, user_id: str, *, skip: int = 0, limit: int = 50) -> list[dict]:
        statement = (
            select(MissionRecord)
            .join(ProjectRecord, MissionRecord.project_id == ProjectRecord.id)
            .where(ProjectRecord.user_id == user_id)
            .order_by(MissionRecord.created_at.desc())
            .offset(skip)
            .limit(limit)
            .options(selectinload(MissionRecord.dossier))
        )
        results = []
        for m in self.session.scalars(statement).all():
            section_count = 0
            if m.dossier and m.dossier.sections_json:
                try:
                    section_count = len(json.loads(m.dossier.sections_json))
                except (json.JSONDecodeError, TypeError):
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

    def get_mission_state(self, user_id: str, mission_id: str) -> dict | None:
        statement = (
            select(MissionRecord)
            .join(ProjectRecord, MissionRecord.project_id == ProjectRecord.id)
            .where(MissionRecord.id == mission_id, ProjectRecord.user_id == user_id)
            .options(
                selectinload(MissionRecord.dossier),
                selectinload(MissionRecord.questions),
            )
        )
        record = self.session.scalar(statement)
        if record is None:
            return None

        documents = []
        dossier = record.dossier
        if dossier and dossier.sections_json:
            try:
                documents = json.loads(dossier.sections_json)
            except (json.JSONDecodeError, TypeError):
                pass

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

        try:
            qual_answers = json.loads(record.qualification_answers_json or "{}")
        except (json.JSONDecodeError, TypeError):
            qual_answers = {}

        try:
            qual_questions = json.loads(record.qualification_questions_json or "[]")
        except (json.JSONDecodeError, TypeError):
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

    def list_mission_inputs(self, mission_id: str) -> list[MissionInputRecord]:
        return list(
            self.session.scalars(
                select(MissionInputRecord).where(MissionInputRecord.mission_id == mission_id)
            ).all()
        )

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
