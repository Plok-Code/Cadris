from __future__ import annotations

import json

from sqlalchemy import delete, func, select

from .base import utc_now
from ..models import (
    CitationItem,
    DossierReadModel,
    ExportReadModel,
    MissionInputItem,
)
from ..records import (
    CitationRecord,
    DossierRecord,
    ExportRecord,
    MissionInputRecord,
    MissionRecord,
    ProjectRecord,
)


class DossierRepoMixin:
    """Dossier, citation, export, and mission-input repository methods."""

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

    def update_dossier_doc_status(
        self,
        mission_id: str,
        validated_ids: list[str],
        corrections: dict[str, str],
    ) -> None:
        from ..models import DossierSection as DossierSectionModel

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

    def create_export(
        self,
        *,
        export_id: str,
        mission_id: str,
        format: str,
        token: str | None = None,
        token_hash: str | None = None,
        expires_at: str | None = None,
        bundle_type: str = "MissionDossier",
    ) -> ExportReadModel:
        record = ExportRecord(
            id=export_id,
            mission_id=mission_id,
            bundle_type=bundle_type,
            format=format,
            token=token,
            token_hash=token_hash,
            expires_at=expires_at,
            created_at=utc_now(),
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return self._to_export_read_model(record)

    def get_export_by_token(self, token: str) -> ExportRecord | None:
        """Legacy lookup by plaintext token (backward compat)."""
        statement = select(ExportRecord).where(
            ExportRecord.token == token,
            ExportRecord.revoked == False,  # noqa: E712
        )
        return self.session.scalar(statement)

    def get_export_by_token_hash(self, token_hash: str) -> ExportRecord | None:
        """Lookup by SHA-256 hash of the share token."""
        statement = select(ExportRecord).where(
            ExportRecord.token_hash == token_hash,
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

    def get_shared_export(self, token: str) -> ExportRecord | None:
        """Alias for get_export_by_token."""
        return self.get_export_by_token(token)
