"""Collaborative engine — wave-based with critic and user pause points.

Phase 2: The engine runs one wave at a time, pausing after each for
user validation. The start method runs only wave 1. The resume method
handles "refine_wave" (re-run current) or "next_wave" (advance).

Memory is persisted via mission_store between HTTP requests.
"""

from __future__ import annotations

import asyncio
import logging

from .agent_manager import run_consolidation_wave, run_single_wave_cycle, get_specs_by_wave, get_wave_doc_ids
from .agent_specs import AGENT_SPECS
from .event_emitter import EventEmitter
from .event_types import EventType
from .memory import MissionMemory
from . import training_logger
from . import mission_store
from .models import (
    MissionQuestion,
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
)
from .response_builders import _memory_to_start_response, _memory_to_resume_response

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
        await mission_store.aput(memory)

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
        memory = await mission_store.aget(payload.mission_id)
        if memory is None:
            logger.warning("No stored memory for %s, creating fresh", payload.mission_id)
            memory = MissionMemory(
                mission_id=payload.mission_id,
                intake_text=payload.intake_text,
                plan=payload.plan,
            )

        action = payload.action

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
            await mission_store.aput(memory)
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
                await mission_store.aput(memory)
                return memory

            # Run next wave + critic
            logger.info("mission %s: advancing to wave %d", payload.mission_id, next_wave_num)
            await run_single_wave_cycle(
                wave_num=next_wave_num,
                memory=memory,
                event_emitter=event_emitter,
            )

        # Persist updated memory
        await mission_store.aput(memory)

        return memory

    # ── Synchronous interface (backward compat) ────────────────

    async def start_mission(self, payload: RuntimeStartRequest) -> RuntimeStartResponse:
        """Non-streaming start — runs wave 1 only and returns response."""
        emitter = EventEmitter()

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
        from .error_classification import is_retryable

        agent = Agent(
            name="Qualification",
            instructions=instructions,
            model=choice.model,
            output_type=QualificationOutput,
        )

        run_config = _get_run_config(choice)

        # Retry logic with timeout — qualification is critical for UX
        max_retries = 3
        QUALIFICATION_TIMEOUT = 120  # 2 minutes
        for attempt in range(1, max_retries + 1):
            try:
                async with asyncio.timeout(QUALIFICATION_TIMEOUT):
                    streamed = Runner.run_streamed(agent, task, run_config=run_config)
                    async for _event in streamed.stream_events():
                        pass
                break
            except Exception as retry_exc:  # noqa: BLE001 — retry loop
                if is_retryable(retry_exc) and attempt < max_retries:
                    wait = min(attempt * 10, 30)
                    logger.warning(
                        "qualification attempt %d/%d failed (%s), retrying in %ds",
                        attempt, max_retries, type(retry_exc).__name__, wait,
                    )
                    await asyncio.sleep(wait)
                else:
                    raise

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
            "error": "Une erreur interne est survenue. Veuillez reessayer.",
        })
        # Emit a fallback question so the user can still proceed
        fallback_q = {
            "question": "Décrivez votre projet en quelques phrases",
            "context": "La qualification automatique a échoué. Veuillez décrire votre projet pour que nous puissions continuer.",
        }
        memory.qualification_questions = [fallback_q]
        await event_emitter.emit(EventType.QUALIFICATION_QUESTIONS, {
            "questions": [fallback_q],
        })


