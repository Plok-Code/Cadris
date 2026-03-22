"""Response builder helpers for the collaborative engine.

Pure converter functions that transform MissionMemory into the legacy
RuntimeStartResponse / RuntimeResumeResponse formats. Extracted from
collaborative_engine.py to keep each module under 400 lines.
"""

from __future__ import annotations

from datetime import UTC, datetime

from .agent_specs import AGENT_SPECS
from .memory import MissionMemory
from .models import (
    ArtifactBlock,
    DossierSection,
    MissionAgent,
    MissionMessage,
    MissionQuestion,
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
    TimelineItem,
)


# ── Response builders ──────────────────────────────────────────


def _memory_to_start_response(
    memory: MissionMemory,
    payload: RuntimeStartRequest,
) -> RuntimeStartResponse:
    """Convert MissionMemory to the legacy RuntimeStartResponse format."""
    now = datetime.now(UTC).isoformat()

    artifact_blocks = _build_artifact_blocks(memory, payload.mission_id)
    active_agents = _build_agents_list(memory)
    recent_messages = _build_messages(memory, payload.mission_id, now)

    unanswered = [q for q in memory.questions if q.to == "user" and not q.answered]
    active_question = None
    if unanswered:
        q = unanswered[0]
        active_question = MissionQuestion(
            id=f"{payload.mission_id}:question:1",
            title="Question de cadrage",
            body=q.question,
        )

    status = "waiting_user" if active_question else "completed"
    if not memory.documents:
        status = "in_progress"

    exec_doc = memory.documents.get("executive_summary")
    summary = exec_doc.content[:300] if exec_doc else "Mission en cours de cadrage."

    return RuntimeStartResponse(
        summary=summary,
        next_step="Repondez a la question pour affiner le cadrage." if active_question else "Le dossier est pret.",
        artifact_blocks=artifact_blocks,
        active_question=active_question or MissionQuestion(
            id=f"{payload.mission_id}:question:1",
            title="Cadrage en cours",
            body="Les agents travaillent sur votre projet...",
        ),
        active_agents=active_agents,
        recent_messages=recent_messages,
        timeline=[
            TimelineItem(id="intake", label="Intake recu", status="completed"),
            TimelineItem(id="agents", label="Agents collaboratifs", status="completed" if memory.documents else "in_progress"),
            TimelineItem(id="question", label="Question utile", status="waiting_user" if active_question else "completed"),
            TimelineItem(id="dossier", label="Dossier final", status="not_started" if active_question else "completed"),
        ],
        status=status,
    )


def _memory_to_resume_response(
    memory: MissionMemory,
    payload: RuntimeResumeRequest,
) -> RuntimeResumeResponse:
    """Convert MissionMemory to the legacy RuntimeResumeResponse format."""
    now = datetime.now(UTC).isoformat()

    artifact_blocks = _build_artifact_blocks(memory, payload.mission_id)
    active_agents = _build_agents_list(memory)
    recent_messages = _build_messages(memory, payload.mission_id, now)

    unanswered = [q for q in memory.questions if q.to == "user" and not q.answered]
    active_question = None
    if unanswered:
        q = unanswered[0]
        active_question = MissionQuestion(
            id=f"{payload.mission_id}:question:{len(memory.questions)}",
            title="Question de cadrage",
            body=q.question,
        )

    status = "waiting_user" if active_question else "completed"

    exec_doc = memory.documents.get("executive_summary")
    dossier_doc = memory.documents.get("dossier_consolide")

    dossier_sections = []
    for doc in memory.documents.values():
        dossier_sections.append(
            DossierSection(
                id=doc.doc_id,
                title=doc.title,
                content=doc.content,
                certainty=doc.certainty,
            )
        )

    return RuntimeResumeResponse(
        summary=exec_doc.content[:300] if exec_doc else "Mission en cours.",
        next_step="Repondez a la question." if active_question else "Le dossier est pret.",
        artifact_blocks=artifact_blocks,
        active_question=active_question,
        certainty_entries=[],
        active_agents=active_agents,
        recent_messages=recent_messages,
        timeline=[
            TimelineItem(id="intake", label="Intake recu", status="completed"),
            TimelineItem(id="agents", label="Agents collaboratifs", status="completed"),
            TimelineItem(id="question", label="Reponse integree", status="completed"),
            TimelineItem(id="dossier", label="Dossier final", status="completed" if not active_question else "in_progress"),
        ],
        status=status,
        dossier_title="Dossier de cadrage",
        dossier_summary=dossier_doc.content[:500] if dossier_doc else None,
        dossier_sections=dossier_sections,
        quality_label="Premier jet" if any(d.certainty != "solid" for d in memory.documents.values()) else "Solide",
    )


def _build_artifact_blocks(memory: MissionMemory, mission_id: str) -> list[ArtifactBlock]:
    """Group documents into artifact blocks by agent domain."""
    blocks = []
    agent_groups = {
        "strategy": ("Bloc Strategie", ["vision_produit", "problem_statement", "icp_personas", "value_proposition"]),
        "product": ("Bloc Produit", ["scope_document", "mvp_definition", "prd", "user_stories", "feature_specs"]),
        "tech": ("Bloc Technique", ["architecture", "tech_stack", "data_model", "api_spec", "nfr_security"]),
        "design": ("Bloc Design", ["ux_principles", "information_architecture", "design_system"]),
        "business": ("Bloc Business", ["business_model", "pricing_strategy", "market_analysis"]),
        "consolidation": ("Bloc Consolidation", ["executive_summary", "dossier_consolide", "implementation_plan", "user_guide"]),
    }

    for agent_code, (title, doc_ids) in agent_groups.items():
        docs = [memory.documents.get(did) for did in doc_ids if did in memory.documents]
        if not docs:
            blocks.append(ArtifactBlock(
                id=f"{mission_id}:artifact:{agent_code}",
                title=title,
                status="not_started",
                certainty="unknown",
                summary="En attente de traitement.",
                content="",
            ))
            continue

        certainties = [d.certainty for d in docs if d is not None]
        if "blocking" in certainties:
            overall_certainty = "blocking"
        elif "unknown" in certainties:
            overall_certainty = "unknown"
        elif "to_confirm" in certainties:
            overall_certainty = "to_confirm"
        else:
            overall_certainty = "solid"

        content_parts = []
        for d in docs:
            if d is not None:
                content_parts.append(f"## {d.title}\n\n{d.content}")

        blocks.append(ArtifactBlock(
            id=f"{mission_id}:artifact:{agent_code}",
            title=title,
            status="complete" if overall_certainty == "solid" else "in_progress",
            certainty=overall_certainty,
            summary=f"{len(docs)} document(s) produit(s).",
            content="\n\n---\n\n".join(content_parts),
        ))

    return blocks


def _build_agents_list(memory: MissionMemory) -> list[MissionAgent]:
    """Build the list of agents with their current status."""
    agents = []
    for spec in AGENT_SPECS:
        docs = memory.get_documents_by_agent(spec.code)
        has_docs = len(docs) > 0
        agents.append(MissionAgent(
            code=spec.code,
            label=spec.label,
            role=spec.role,
            status="done" if has_docs else "waiting",
            prompt_key=spec.prompt_key,
            prompt_version="v1",
            summary=f"{len(docs)} document(s) produit(s)." if has_docs else "En attente.",
        ))
    return agents


def _build_messages(memory: MissionMemory, mission_id: str, now: str) -> list[MissionMessage]:
    """Build recent messages from agent logs."""
    messages = []
    for i, log_entry in enumerate(memory.agent_logs[-10:]):
        agent_code = log_entry.get("agent", "system")
        status = log_entry.get("status", "info")
        docs = log_entry.get("docs_produced", [])

        spec = None
        for s in AGENT_SPECS:
            if s.code == agent_code:
                spec = s
                break

        messages.append(MissionMessage(
            id=f"{mission_id}:{agent_code}:{i}",
            agent_code=agent_code,
            agent_label=spec.label if spec else agent_code,
            stage=f"iteration_{log_entry.get('iteration', 0)}",
            title=f"{spec.label if spec else agent_code} - {'termine' if status == 'completed' else 'erreur'}",
            body=f"Documents produits: {', '.join(docs)}" if docs else log_entry.get("error", "En cours..."),
            created_at=now,
        ))
    return messages
