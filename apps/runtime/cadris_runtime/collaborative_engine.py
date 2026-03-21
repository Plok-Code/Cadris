"""Collaborative engine — wave-based with critic and user pause points.

Phase 2: The engine runs one wave at a time, pausing after each for
user validation. The start method runs only wave 1. The resume method
handles "refine_wave" (re-run current) or "next_wave" (advance).

Memory is persisted via mission_store between HTTP requests.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime

from .agent_manager import run_consolidation_wave, run_single_wave_cycle, get_specs_by_wave, get_wave_doc_ids
from .agent_specs import AGENT_SPECS
from .event_emitter import EventEmitter
from .event_types import EventType
from .memory import MissionMemory
from . import training_logger
from . import mission_store
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

logger = logging.getLogger(__name__)


class CollaborativeEngine:
    """Runtime engine using wave-based collaborative multi-agent system."""

    provider = "collaborative"

    def health_payload(self) -> dict[str, object]:
        return {
            "provider": self.provider,
            "ready": True,
            "agents": len(AGENT_SPECS),
        }

    # ── Streaming interface (Phase 2) ─────────────────────────

    async def start_mission_stream(
        self,
        payload: RuntimeStartRequest,
        event_emitter: EventEmitter,
    ) -> MissionMemory:
        """Launch a mission: generate qualification questions, then pause.

        The stream closes after questions are emitted. Client must call
        resume_mission_stream with action="answer_qualification" to proceed.
        """
        memory = MissionMemory(mission_id=payload.mission_id, intake_text=payload.intake_text, plan=payload.plan)

        waves = get_specs_by_wave()

        await event_emitter.emit(EventType.MISSION_STARTED, {
            "mission_id": payload.mission_id,
            "total_agents": len(AGENT_SPECS),
            "total_waves": len(waves),
        })

        # Run qualification: generate targeted questions from intake
        await _run_qualification(memory, event_emitter)

        # Persist memory for resume
        mission_store.put(memory)

        return memory

    async def resume_mission_stream(
        self,
        payload: RuntimeResumeRequest,
        event_emitter: EventEmitter,
    ) -> MissionMemory:
        """Resume a mission: refine current wave or advance to next.

        Actions:
        - "refine_wave": inject user answer, re-run current wave + critic
        - "next_wave": validate current wave, run next wave + critic
                       (if last reviewable wave → run consolidation → complete)
        """
        # Load persisted memory
        memory = mission_store.get(payload.mission_id)
        if memory is None:
            logger.warning("No stored memory for %s, creating fresh", payload.mission_id)
            memory = MissionMemory(
                mission_id=payload.mission_id,
                intake_text=payload.intake_text,
                plan=payload.plan,
            )

        action = getattr(payload, "action", "next_wave")

        if action == "answer_qualification":
            # Inject qualification answers and run Wave 1
            import json
            if payload.answer_text and payload.answer_text.strip():
                try:
                    answers = json.loads(payload.answer_text)
                    if isinstance(answers, dict):
                        memory.qualification_answers = {
                            q: a for q, a in answers.items()
                            if a.lower() != "je_sais_pas"
                        }
                except (json.JSONDecodeError, AttributeError):
                    # Fallback: treat as plain text answer
                    memory.user_answers.append(payload.answer_text.strip())

            # Log for training data
            training_logger.log_mission_start(
                mission_id=payload.mission_id,
                intake_text=memory.intake_text,
                qualification_questions=memory.qualification_questions,
                qualification_answers=memory.qualification_answers,
                plan=memory.plan,
            )

            logger.info("mission %s: qualification answered, starting wave 1", payload.mission_id)
            await run_single_wave_cycle(
                wave_num=1,
                memory=memory,
                event_emitter=event_emitter,
            )

            # Persist updated memory
            mission_store.put(memory)
            return memory

        # Inject user answer if provided (for wave actions)
        if payload.answer_text and payload.answer_text.strip():
            memory.user_answers.append(payload.answer_text.strip())

        current_wave = memory.current_wave
        waves = get_specs_by_wave()
        sorted_waves = sorted(waves.keys())
        max_wave = max(sorted_waves)

        # Determine the last "reviewable" wave (all except consolidation)
        # Consolidation is the final wave and runs without review
        last_reviewable_wave = sorted_waves[-2] if len(sorted_waves) > 1 else sorted_waves[0]

        if action == "refine_wave":
            # Re-run the current wave with enriched context (user corrections).
            # All docs from the block are regenerated for coherence.
            logger.info(
                "mission %s: refining wave %d with corrections",
                payload.mission_id, current_wave,
            )
            # Invalidate all docs from this wave so agents regenerate them
            wave_doc_ids = get_wave_doc_ids(current_wave)
            for doc_id in wave_doc_ids:
                if doc_id in memory.documents:
                    logger.info("invalidating doc %s for re-generation", doc_id)
                    memory.documents.pop(doc_id)

            await run_single_wave_cycle(
                wave_num=current_wave,
                memory=memory,
                event_emitter=event_emitter,
            )

        else:
            # action == "next_wave"
            memory.wave_validated.add(current_wave)
            next_wave_num = current_wave + 1

            if next_wave_num > last_reviewable_wave:
                # All reviewable waves done → run consolidation → complete
                logger.info("mission %s: running final consolidation wave", payload.mission_id)
                await run_consolidation_wave(memory, event_emitter)
                # Log completion for training data
                training_logger.log_mission_complete(
                    mission_id=payload.mission_id,
                    total_documents=len(memory.documents),
                    total_errors=sum(1 for log in memory.agent_logs if log.get("status") == "error"),
                    elapsed_seconds=0,  # computed client-side
                    plan=memory.plan,
                )
                # Keep in store for document retrieval (TTL will clean up)
                mission_store.put(memory)
                return memory

            # Run next wave + critic
            logger.info("mission %s: advancing to wave %d", payload.mission_id, next_wave_num)
            await run_single_wave_cycle(
                wave_num=next_wave_num,
                memory=memory,
                event_emitter=event_emitter,
            )

        # Persist updated memory
        mission_store.put(memory)

        return memory

    # ── Synchronous interface (backward compat) ────────────────

    async def start_mission(self, payload: RuntimeStartRequest) -> RuntimeStartResponse:
        """Non-streaming start — runs wave 1 only and returns response."""
        emitter = EventEmitter()

        import asyncio
        memory_task = asyncio.create_task(
            self.start_mission_stream(payload, emitter)
        )
        async for _ in emitter:
            pass
        memory = await memory_task

        return _memory_to_start_response(memory, payload)

    async def resume_mission(self, payload: RuntimeResumeRequest) -> RuntimeResumeResponse:
        """Non-streaming resume — runs one wave cycle and returns response."""
        emitter = EventEmitter()

        import asyncio
        memory_task = asyncio.create_task(
            self.resume_mission_stream(payload, emitter)
        )
        async for _ in emitter:
            pass
        memory = await memory_task

        return _memory_to_resume_response(memory, payload)


# ── Qualification phase ────────────────────────────────────────


async def _run_qualification(
    memory: MissionMemory,
    event_emitter: EventEmitter,
) -> None:
    """Generate qualification questions from the intake text via LLM.

    Uses the qualifier_agent prompt with structured output to produce
    3-5 targeted questions. Emits QUALIFICATION_QUESTIONS event and returns.
    """
    from .agent_specs import QualificationOutput
    from .model_config import get_model_for_agent
    from .prompt_loader import load_prompt

    choice = get_model_for_agent("qualifier", memory.plan)

    try:
        try:
            prompt_template = load_prompt("agents/qualifier_agent")
            instructions = prompt_template.instructions
        except KeyError:
            instructions = (
                "Tu es un expert en cadrage de projets digitaux. "
                "Genere 3 a 5 questions ciblees pour completer la description du projet."
            )

        task = f"## Description du projet\n{memory.intake_text}\n\n## Ta mission\nGenere les questions de qualification."

        try:
            from agents import Agent, Runner
        except ImportError as exc:
            raise RuntimeError(f"openai-agents import failed: {exc}") from exc

        from .agent_runner import _get_run_config

        agent = Agent(
            name="Qualification",
            instructions=instructions,
            model=choice.model,
            output_type=QualificationOutput,
        )

        run_config = _get_run_config(choice)

        streamed = Runner.run_streamed(agent, task, run_config=run_config)
        async for _event in streamed.stream_events():
            pass

        output: QualificationOutput = streamed.final_output_as(QualificationOutput)

        # Store questions in memory
        memory.qualification_questions = [
            {"question": q.question, "context": q.context}
            for q in output.questions
        ]

        # Emit questions for the client
        await event_emitter.emit(EventType.QUALIFICATION_QUESTIONS, {
            "questions": memory.qualification_questions,
        })

        logger.info(
            "qualification generated %d questions for mission %s",
            len(output.questions), memory.mission_id,
        )

    except Exception as exc:  # noqa: BLE001 — qualification failure must not block the mission
        logger.error("qualification failed: %s", exc, exc_info=True)
        await event_emitter.emit(EventType.ERROR, {
            "agent": "qualifier",
            "error": str(exc),
        })
        # Emit empty questions so the client can still proceed
        await event_emitter.emit(EventType.QUALIFICATION_QUESTIONS, {
            "questions": [],
        })


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
