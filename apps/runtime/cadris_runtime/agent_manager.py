"""Wave-based orchestration for the collaborative agent engine.

Phase 2 architecture: each wave runs, then the critic evaluates,
then the system pauses for user validation. The caller (collaborative_engine)
decides whether to resume the same wave or advance to the next.

Functions:
- run_wave()              → execute agents in a single wave
- run_single_wave_cycle() → wave + critic + emit pause events

Critic logic lives in critic.py (extracted for the 400-line rule).
"""

from __future__ import annotations

import asyncio
import logging

from .agent_runner import run_agent, AgentResult
from .agent_specs import AGENT_SPECS, AgentSpec, CriticOutput, get_specs_by_wave
from .critic import run_critic
from .event_emitter import EventEmitter
from .event_types import EventType
from .memory import MissionMemory
from .model_config import get_model_for_agent
from . import training_logger

logger = logging.getLogger(__name__)

# ── Cooldown constants (seconds) ─────────────────────────────
INTER_WAVE_COOLDOWN = 15  # between waves — let TPM rate-limit window reset
INTER_AGENT_COOLDOWN = 10  # between agents within a wave
PRE_CRITIC_COOLDOWN = 5  # before running the critic after a wave


# ── Wave-to-doc mapping (for block coherence re-runs) ─────────

def get_wave_doc_ids(wave_num: int) -> list[str]:
    """Return all doc_ids produced by agents in a given wave.

    Used to determine which docs belong to a block for coherence
    re-verification when the user corrects one document.
    """
    waves = get_specs_by_wave()
    agents = waves.get(wave_num, [])
    doc_ids: list[str] = []
    for spec in agents:
        for ds in spec.doc_specs:
            doc_ids.append(ds.doc_id)
    return doc_ids


def get_wave_for_doc(doc_id: str) -> int | None:
    """Return the wave number that produces a given doc_id."""
    waves = get_specs_by_wave()
    for wave_num, agents in waves.items():
        for spec in agents:
            for ds in spec.doc_specs:
                if ds.doc_id == doc_id:
                    return wave_num
    return None


# ── Wave execution ────────────────────────────────────────────


async def run_wave(
    wave_num: int,
    memory: MissionMemory,
    event_emitter: EventEmitter,
) -> None:
    """Run all agents in a single wave, writing results to memory."""
    waves = get_specs_by_wave()
    wave_agents = waves.get(wave_num, [])

    if not wave_agents:
        logger.warning("No agents found for wave %d", wave_num)
        return

    # Inter-wave cooldown: let the TPM rate-limit window reset before
    # starting a new burst of agent calls.  Wave 1 starts immediately.
    if wave_num > 1:
        logger.info("inter-wave cooldown %ds before wave %d", INTER_WAVE_COOLDOWN, wave_num)
        await asyncio.sleep(INTER_WAVE_COOLDOWN)

    await event_emitter.emit(EventType.WAVE_STARTED, {
        "wave": wave_num,
        "agents": [s.code for s in wave_agents],
        "total_waves": len(waves),
    })

    for i, spec in enumerate(wave_agents):
        if i > 0:
            # Cooldown between agents to avoid rate-limit bursts (TPM)
            logger.info("cooldown %ds before agent %s", INTER_AGENT_COOLDOWN, spec.code)
            await asyncio.sleep(INTER_AGENT_COOLDOWN)
        await _run_single_agent(spec, memory, event_emitter, wave_num)


# ── Combined wave cycle ──────────────────────────────────────


async def run_single_wave_cycle(
    wave_num: int,
    memory: MissionMemory,
    event_emitter: EventEmitter,
) -> CriticOutput:
    """Run one wave + critic review cycle.

    This is the main building block: execute wave agents, then critic,
    then emit WAVE_COMPLETED as a pause point.
    Returns the critic output for the caller to decide next action.
    """
    memory.iteration += 1
    memory.current_wave = wave_num

    # 1. Run wave agents
    await run_wave(wave_num, memory, event_emitter)

    # 2. Skip critic for free plan (saves cost + time)
    if memory.plan == "free":
        logger.info("free plan: skipping critic for wave %d", wave_num)
        critic_output = CriticOutput(
            overall_quality="good",
            reviews=[],
            questions_for_user=[],
            synthesis="Critique non disponible sur le plan gratuit.",
        )
    else:
        # Brief cooldown before critic
        logger.info("cooldown %ds before critic for wave %d", PRE_CRITIC_COOLDOWN, wave_num)
        await asyncio.sleep(PRE_CRITIC_COOLDOWN)

        # Run critic review
        critic_output = await run_critic(wave_num, memory, event_emitter)

    # 3. Emit wave completed (pause point for the client)
    await event_emitter.emit(EventType.WAVE_COMPLETED, {
        "wave": wave_num,
        "total_waves": len(get_specs_by_wave()),
        "overall_quality": critic_output.overall_quality,
        "questions_for_user": critic_output.questions_for_user,
        "documents_so_far": len(memory.documents),
    })

    return critic_output


async def run_consolidation_wave(
    memory: MissionMemory,
    event_emitter: EventEmitter,
) -> None:
    """Run the final consolidation wave without critic review.

    Consolidation just assembles everything — no need for review/pause.
    """
    waves = get_specs_by_wave()
    max_wave = max(waves.keys())

    memory.iteration += 1
    memory.current_wave = max_wave

    await run_wave(max_wave, memory, event_emitter)

    await event_emitter.emit(EventType.MISSION_COMPLETED, {
        "mission_id": memory.mission_id,
        "total_documents": len(memory.documents),
        "iterations": memory.iteration,
    })


# ── Single agent runner (unchanged from Phase 1) ─────────────


async def _run_single_agent(
    spec: AgentSpec,
    memory: MissionMemory,
    event_emitter: EventEmitter,
    wave_num: int,
) -> None:
    """Run one agent and update memory + emit events."""
    choice = get_model_for_agent(spec.code, memory.plan)

    await event_emitter.emit(EventType.AGENT_STARTED, {
        "agent": spec.code,
        "label": spec.label,
        "role": spec.role,
        "wave": wave_num,
        "model": choice.model,
        "iteration": memory.iteration,
    })

    try:
        result: AgentResult = await run_agent(spec, memory)

        for doc in result.documents:
            memory.upsert_document(doc)
            await event_emitter.emit(EventType.DOCUMENT_UPDATED, {
                "doc_id": doc.doc_id,
                "title": doc.title,
                "agent": spec.code,
                "wave": wave_num,
                "certainty": doc.certainty,
                "version": doc.version,
                "content": doc.content or "",
            })
            # Log for training data — full context for fine-tuning
            training_logger.log_document(
                mission_id=memory.mission_id,
                doc_id=doc.doc_id,
                agent=spec.code,
                title=doc.title,
                content=doc.content,
                certainty=doc.certainty,
                wave=wave_num,
                plan=memory.plan,
                model=result.model,
                provider=result.provider,
                prompt_sent=result.prompt_sent,
                attempt=result.attempt,
                elapsed_ms=result.elapsed_ms,
            )

        memory.log({
            "agent": spec.code,
            "wave": wave_num,
            "iteration": memory.iteration,
            "docs_produced": [d.doc_id for d in result.documents],
            "status": "completed",
        })

        await event_emitter.emit(EventType.AGENT_COMPLETED, {
            "agent": spec.code,
            "docs_produced": len(result.documents),
            "iteration": memory.iteration,
        })

    except Exception as exc:  # noqa: BLE001 — fallback produces placeholder docs; mission must not stop
        logger.error("agent %s failed: %s", spec.code, exc, exc_info=True)

        # ── Fallback: produce minimal placeholder documents ──
        # Never leave gaps — downstream agents and consolidation need
        # every doc_id to exist, even if the content is minimal.
        from .memory import DocumentDraft
        fallback_docs = []
        for ds in spec.doc_specs:
            fallback_doc = DocumentDraft(
                doc_id=ds.doc_id,
                title=ds.title,
                agent_code=spec.code,
                content=(
                    f"## {ds.title}\n\n"
                    f"*Ce document n'a pas pu etre genere automatiquement. "
                    f"Il sera complete lors d'une iteration ulterieure ou "
                    f"avec un plan offrant des modeles plus performants.*"
                ),
                certainty="to_confirm",
            )
            memory.upsert_document(fallback_doc)
            fallback_docs.append(fallback_doc)
            await event_emitter.emit(EventType.DOCUMENT_UPDATED, {
                "doc_id": fallback_doc.doc_id,
                "title": fallback_doc.title,
                "agent": spec.code,
                "certainty": fallback_doc.certainty,
                "version": fallback_doc.version,
                "content": fallback_doc.content or "",
            })

        logger.info(
            "agent %s: injected %d fallback documents after failure",
            spec.code, len(fallback_docs),
        )

        memory.log({
            "agent": spec.code,
            "wave": wave_num,
            "iteration": memory.iteration,
            "status": "fallback",
            "error": "agent_execution_failed",
            "docs_produced": [d.doc_id for d in fallback_docs],
        })
        await event_emitter.emit(EventType.AGENT_COMPLETED, {
            "agent": spec.code,
            "docs_produced": len(fallback_docs),
            "iteration": memory.iteration,
            "fallback": True,
        })
