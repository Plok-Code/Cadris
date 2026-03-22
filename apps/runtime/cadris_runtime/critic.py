"""Critic agent execution — evaluates document quality after each wave.

Extracted from agent_manager.py to keep modules under 400 lines.

Functions:
- run_critic()  → evaluate all docs with the critic agent
"""

from __future__ import annotations

import asyncio
import logging

from .agent_runner import _get_run_config
from .agent_specs import CRITIC_SPEC, CriticOutput
from .error_classification import is_retryable
from .event_emitter import EventEmitter
from .event_types import EventType
from .memory import MissionMemory
from .model_config import get_model_for_agent
from . import training_logger

logger = logging.getLogger(__name__)


async def run_critic(
    wave_num: int,
    memory: MissionMemory,
    event_emitter: EventEmitter,
) -> CriticOutput:
    """Run the critic agent on all documents produced so far.

    The critic sees ALL documents (not filtered by reads_from).
    Returns the structured CriticOutput for the caller to act on.
    """
    from .context_builders import _build_questions_context
    from .prompt_loader import load_prompt

    choice = get_model_for_agent(CRITIC_SPEC.code, memory.plan)

    await event_emitter.emit(EventType.AGENT_STARTED, {
        "agent": CRITIC_SPEC.code,
        "label": CRITIC_SPEC.label,
        "role": CRITIC_SPEC.role,
        "wave": wave_num,
        "model": choice.model,
        "iteration": memory.iteration,
    })

    try:
        # Load critic prompt
        try:
            prompt_template = load_prompt(f"agents/{CRITIC_SPEC.prompt_key}")
            instructions = prompt_template.instructions
        except KeyError:
            instructions = f"Tu es {CRITIC_SPEC.label}. {CRITIC_SPEC.role}"

        # Build context: ALL documents.
        # The critic needs more content per doc than regular agents to evaluate
        # depth and quality properly.  2500 chars ~ 400+ words, matching the
        # critic's 400-word minimum threshold.
        from .config import settings as _settings
        MAX_CHARS_PER_DOC = _settings.critic_max_context_chars
        all_docs = list(memory.documents.values())
        doc_sections = []
        for doc in all_docs:
            content = doc.content
            if len(content) > MAX_CHARS_PER_DOC:
                content = content[:MAX_CHARS_PER_DOC] + "\n\n[... tronque pour concision]"
            doc_sections.append(
                f"### {doc.title} (par {doc.agent_code}, certitude: {doc.certainty})\n{content}"
            )
        docs_context = "\n\n".join(doc_sections) if doc_sections else "Aucun document disponible."

        questions_context = _build_questions_context(memory)

        # Build task
        task_parts = [
            f"## Contexte projet\n{memory.intake_text}",
        ]
        if questions_context:
            task_parts.append(questions_context)
        if memory.user_answers:
            answers_section = "## Reponses precedentes de l'utilisateur\n"
            answers_section += "\n".join(f"- {a}" for a in memory.user_answers)
            task_parts.append(answers_section)
        task_parts.append(f"## Documents produits (vagues 1-{wave_num})\n{docs_context}")
        task_parts.append(
            f"## Ta mission\nEvalue la qualite des documents de la vague {wave_num} "
            f"et genere des questions ciblees pour l'utilisateur."
        )
        task = "\n\n".join(task_parts)

        # Run critic with structured output
        try:
            from agents import Agent, Runner
        except ImportError as exc:
            raise RuntimeError(f"openai-agents import failed: {exc}") from exc

        agent = Agent(
            name=CRITIC_SPEC.label,
            instructions=instructions,
            model=choice.model,
            output_type=CriticOutput,
        )

        run_config = _get_run_config(choice)

        # Retry logic for critic — uses streaming to avoid connection drops
        max_retries = 5
        for attempt in range(1, max_retries + 1):
            try:
                streamed = Runner.run_streamed(agent, task, run_config=run_config)
                async for _event in streamed.stream_events():
                    pass
                break
            except Exception as retry_exc:  # noqa: BLE001 — retry loop uses typed error classification
                if is_retryable(retry_exc) and attempt < max_retries:
                    wait = min(attempt * 30, 120)
                    logger.warning(
                        "critic attempt %d/%d failed (%s), retrying in %ds",
                        attempt, max_retries, type(retry_exc).__name__, wait,
                    )
                    await asyncio.sleep(wait)
                else:
                    raise

        critic_output: CriticOutput = streamed.final_output_as(CriticOutput)

        # Store critic review in memory
        memory.critic_reviews.append({
            "wave": wave_num,
            "iteration": memory.iteration,
            "overall_quality": critic_output.overall_quality,
            "reviews": [r.model_dump() for r in critic_output.reviews],
            "questions": critic_output.questions_for_user,
            "synthesis": critic_output.synthesis,
        })

        # Log critic for training data — key signal for DPO
        training_logger.log_critic(
            mission_id=memory.mission_id,
            wave=wave_num,
            overall_quality=critic_output.overall_quality,
            reviews=[r.model_dump() for r in critic_output.reviews],
            questions_for_user=critic_output.questions_for_user,
            synthesis=critic_output.synthesis,
            plan=memory.plan,
            model=choice.model,
            provider=choice.provider,
        )

        await event_emitter.emit(EventType.AGENT_COMPLETED, {
            "agent": CRITIC_SPEC.code,
            "docs_produced": 0,
            "iteration": memory.iteration,
        })

        # Emit wave review event
        await event_emitter.emit(EventType.WAVE_REVIEW, {
            "wave": wave_num,
            "overall_quality": critic_output.overall_quality,
            "reviews": [r.model_dump() for r in critic_output.reviews],
            "questions_for_user": critic_output.questions_for_user,
            "synthesis": critic_output.synthesis,
        })

        return critic_output

    except Exception as exc:  # noqa: BLE001 — critic failure must not stop the mission
        logger.error("critic agent failed: %s", exc, exc_info=True)
        await event_emitter.emit(EventType.ERROR, {
            "agent": CRITIC_SPEC.code,
            "error": "Une erreur interne est survenue. Veuillez reessayer.",
            "iteration": memory.iteration,
        })
        # Return a safe fallback so the flow doesn't break.
        # Mark as "unavailable" so the UI can distinguish from a real review.
        return CriticOutput(
            overall_quality="unavailable",
            reviews=[],
            questions_for_user=[],
            synthesis="Evaluation du critique non disponible (erreur interne).",
        )
