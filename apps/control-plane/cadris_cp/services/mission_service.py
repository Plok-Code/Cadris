"""SSE persistence helpers for mission streaming."""
from __future__ import annotations

import logging

from sqlalchemy.orm import Session

from ..models import DossierReadModel, DossierSection as DossierSectionModel, RuntimeInputItem, utc_now
from ..repository import ControlPlaneRepository

logger = logging.getLogger(__name__)


def persist_dossier_from_docs(
    db_session: Session,
    mission_id: str,
    collected_docs: dict[str, dict],
    *,
    is_final: bool = False,
) -> None:
    """Build and persist a DossierReadModel from streamed document_updated events.

    Merges new docs with any existing dossier sections from previous waves,
    so the final dossier contains ALL documents across all waves.
    """
    if not collected_docs:
        return
    try:
        repo = ControlPlaneRepository(db_session)

        # Load existing sections from previous waves (if any)
        existing_dossier = repo.get_dossier(mission_id)
        existing_map: dict[str, DossierSectionModel] = {}
        if existing_dossier:
            for s in existing_dossier.sections:
                existing_map[s.id] = s

        # Merge: new docs override existing ones with same id
        for doc_id, doc in collected_docs.items():
            existing_map[doc_id] = DossierSectionModel(
                id=doc_id,
                title=doc.get("title", doc_id),
                content=doc.get("content", ""),
                certainty=doc.get("certainty", "unknown"),
                agent=doc.get("agent", ""),
                version=doc.get("version", 1),
                wave=doc.get("wave", 0),
            )

        sections = list(existing_map.values())

        # Build combined markdown
        md_parts = ["# Dossier de cadrage\n"]
        for s in sections:
            md_parts.append(f"## {s.title}\n\n{s.content}\n")
        markdown = "\n".join(md_parts)

        dossier = DossierReadModel(
            mission_id=mission_id,
            title="Dossier de cadrage",
            quality_label="",
            summary="Dossier genere par les agents Cadris.",
            markdown=markdown,
            sections=sections,
            updated_at=utc_now(),
        )
        repo.upsert_dossier(dossier)

        if is_final:
            from ..records import MissionRecord
            record = db_session.get(MissionRecord, mission_id)
            if record:
                record.status = "completed"
                record.dossier_ready = True
                db_session.commit()

        logger.info("persisted dossier for mission %s (%d sections, final=%s)", mission_id, len(sections), is_final)
    except Exception:  # noqa: BLE001 — best-effort persistence; must not crash SSE stream
        logger.error("failed to persist dossier for mission %s", mission_id, exc_info=True)


def save_sse_state(
    db_session: Session,
    mission_id: str,
    event: dict,
    collected_docs: dict[str, dict],
    repository: ControlPlaneRepository,
) -> None:
    """Save mission state at each SSE checkpoint for resume support."""
    etype = event["event"]
    data = event.get("data", {})

    try:
        if etype == "document_updated":
            d = data
            collected_docs[d.get("doc_id", "")] = d
            persist_dossier_from_docs(db_session, mission_id, collected_docs)
        elif etype == "qualification_questions":
            repository.update_mission_phase(mission_id, "qualification")
            questions = data.get("questions", [])
            if questions:
                repository.save_qualification_questions(mission_id, questions)
        elif etype == "wave_started":
            wave = data.get("wave", 0)
            repository.update_mission_wave(mission_id, wave)
            repository.update_mission_phase(mission_id, "wave_running")
        elif etype == "wave_completed":
            persist_dossier_from_docs(db_session, mission_id, collected_docs)
            repository.update_mission_phase(mission_id, "doc_review")
        elif etype == "mission_completed":
            persist_dossier_from_docs(db_session, mission_id, collected_docs, is_final=True)
            repository.update_mission_phase(mission_id, "completed")
    except Exception:  # noqa: BLE001 — best-effort SSE state save; must not crash stream
        logger.error("failed to save SSE state for %s event=%s", mission_id, etype, exc_info=True)


def to_runtime_inputs(items) -> list[RuntimeInputItem]:
    return [
        RuntimeInputItem(
            id=item.id,
            kind=item.kind,
            source=item.source,
            content=item.content,
            display_name=item.display_name,
            mime_type=item.mime_type,
            byte_size=item.byte_size,
            preview_text=item.preview_text,
        )
        for item in items
        if item.kind == "uploaded_file"
    ]
