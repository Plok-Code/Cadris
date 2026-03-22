"""Run a single collaborative agent against the shared mission memory.

Uses the OpenAI Agents SDK (openai-agents) with structured outputs.
Supports multiple providers (OpenAI, Together AI) based on the plan.

Each agent:
1. Reads the shared memory (other agents' documents)
2. Receives its prompt + project context
3. Produces structured output (Pydantic model)
4. Returns DocumentDraft objects to be written back to memory
"""

from __future__ import annotations

import asyncio
import logging
import random
import time
from dataclasses import dataclass, field
from typing import TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

from .agent_specs import AgentSpec, DocSpec
from .context_builders import (
    _build_context,
    _build_qualification_context,
    _build_questions_context,
    _build_file_map_context,
    _build_quality_instructions,
    DOC_ID_TO_ZIP_PATH,
)
from .memory import DocumentDraft, MissionMemory
from .model_config import ModelChoice, get_model_for_agent
from .prompt_loader import load_prompt
from .config import settings
from .error_classification import is_json_error, is_retryable
from .web_research import research_for_agent


@dataclass
class AgentResult:
    """Result of run_agent with metadata for training data logging."""
    documents: list[DocumentDraft] = field(default_factory=list)
    model: str = ""
    provider: str = ""
    prompt_sent: str = ""
    attempt: int = 1
    elapsed_ms: int = 0
    is_fallback: bool = False

logger = logging.getLogger(__name__)

try:
    from agents import Agent, ModelSettings, Runner, RunConfig
    from agents.models.openai_provider import OpenAIProvider
    from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
except Exception as exc:  # noqa: BLE001 — import guard for optional agents SDK
    Agent = None  # type: ignore[assignment, misc]
    Runner = None  # type: ignore[assignment, misc]
    RunConfig = None  # type: ignore[assignment, misc]
    OpenAIProvider = None  # type: ignore[assignment, misc]
    OpenAIChatCompletionsModel = None  # type: ignore[assignment, misc]
    _IMPORT_ERROR = exc
else:
    _IMPORT_ERROR = None

T = TypeVar("T", bound=BaseModel)

# ── Provider clients (lazy-initialized singletons) ────────────

_together_client: AsyncOpenAI | None = None
_openai_client: AsyncOpenAI | None = None


def _get_together_client() -> AsyncOpenAI:
    global _together_client
    if _together_client is None:
        api_key = settings.together_api_key
        if not api_key:
            raise RuntimeError("TOGETHER_API_KEY not set — required for free plan")
        _together_client = AsyncOpenAI(
            base_url="https://api.together.xyz/v1",
            api_key=api_key,
        )
    return _together_client


def _get_openai_client() -> AsyncOpenAI:
    global _openai_client
    if _openai_client is None:
        _openai_client = AsyncOpenAI(api_key=settings.openai_api_key)
    return _openai_client


def _get_run_config(choice: ModelChoice) -> RunConfig:
    """Build a RunConfig with the appropriate provider client.

    Together AI doesn't support the /v1/responses endpoint, so we use
    OpenAIChatCompletionsModel (which uses /v1/chat/completions) instead
    of the default OpenAIProvider (which uses /v1/responses).
    """
    if choice.provider == "together":
        client = _get_together_client()
        model = OpenAIChatCompletionsModel(
            model=choice.model,
            openai_client=client,
        )
        # Together AI defaults to ~4096 output tokens which truncates
        # large structured outputs. 10240 tokens gives enough headroom
        # for the consolidation agent (4 docs) on the free plan.
        return RunConfig(
            model=model,
            model_settings=ModelSettings(max_tokens=16384),
        )
    else:
        client = _get_openai_client()
        return RunConfig(model_provider=OpenAIProvider(openai_client=client))


# ── Output parsing ────────────────────────────────────────────


def _parse_output_to_documents(
    output: BaseModel,
    spec: AgentSpec,
) -> list[DocumentDraft]:
    """Convert a structured Pydantic output into DocumentDraft objects."""
    docs: list[DocumentDraft] = []
    output_dict = output.model_dump()

    for doc_spec in spec.doc_specs:
        content = output_dict.get(doc_spec.doc_id, "")
        if not content:
            continue

        certainty = _infer_certainty(content)

        docs.append(
            DocumentDraft(
                doc_id=doc_spec.doc_id,
                title=doc_spec.title,
                agent_code=spec.code,
                content=content,
                certainty=certainty,
                depends_on=[d.doc_id for d in docs],
            )
        )

    return docs


def _infer_certainty(content: str) -> str:
    """Infer certainty level from content markers."""
    lower = content.lower()
    if any(marker in lower for marker in ["bloquant", "blocking", "impossible sans"]):
        return "blocking"
    if any(marker in lower for marker in ["hypothese", "a confirmer", "incertain", "to_confirm"]):
        return "to_confirm"
    if any(marker in lower for marker in ["inconnu", "unknown", "pas assez d'information"]):
        return "unknown"
    return "solid"


# ── Main agent runner ─────────────────────────────────────────


def _ensure_sdk() -> None:
    if _IMPORT_ERROR is not None:
        raise RuntimeError(f"openai-agents import failed: {_IMPORT_ERROR}") from _IMPORT_ERROR


async def run_agent(
    spec: AgentSpec,
    memory: MissionMemory,
) -> AgentResult:
    """Execute a single agent and return its document drafts + metadata.

    The model and provider are resolved from model_config based on
    the agent code and the mission's plan.
    """
    _ensure_sdk()
    t0 = time.monotonic()

    plan = memory.plan
    choice = get_model_for_agent(spec.code, plan)
    logger.info(
        "running agent %s with model %s (provider=%s, plan=%s, wave %d)",
        spec.code, choice.model, choice.provider, plan, spec.wave,
    )

    # 1. Load the agent's prompt
    try:
        prompt_template = load_prompt(f"agents/{spec.prompt_key}")
        instructions = prompt_template.instructions
    except KeyError:
        logger.warning("prompt not found for agents/%s, using role as fallback", spec.prompt_key)
        instructions = f"Tu es {spec.label}. {spec.role}"

    # 2. Build context from shared memory
    other_agents_context = _build_context(spec, memory)
    questions_context = _build_questions_context(memory)

    # 2b. Build qualification context
    qualification_context = _build_qualification_context(memory)

    # 2c. Web research (Pro/Expert plans — Perplexity)
    web_research_context = await research_for_agent(spec.code, memory.intake_text, plan)

    # 3. Compose the task
    task_parts = [
        f"## Contexte projet\n{memory.intake_text}",
    ]
    if qualification_context:
        task_parts.append(qualification_context)
    if questions_context:
        task_parts.append(questions_context)
    if web_research_context:
        task_parts.append(web_research_context)
    task_parts.append(f"## Travail des autres agents\n{other_agents_context}")

    # Inject user corrections/feedback from previous iterations
    if memory.user_answers:
        corrections_section = "## Corrections et retours de l'utilisateur\n"
        corrections_section += "L'utilisateur a demande les modifications suivantes. "
        corrections_section += "Integre ces retours dans tes documents :\n"
        corrections_section += "\n".join(f"- {a}" for a in memory.user_answers)
        task_parts.append(corrections_section)

    task_parts.append(
        f"## Ta mission\nProduis les documents suivants:\n"
        + "\n".join(f"- **{ds.title}** (`{ds.doc_id}`)" for ds in spec.doc_specs)
    )

    # Quality instructions adapted to plan
    task_parts.append(_build_quality_instructions(plan))

    # Inject explicit file path mapping for consolidation agent
    if spec.code == "consolidation":
        task_parts.append(_build_file_map_context())

    task = "\n\n".join(task_parts)

    # 4. Run with structured output (retry on all errors)
    run_config = _get_run_config(choice)

    max_retries = 5
    current_task = task
    output = None

    AGENT_TIMEOUT = 300  # 5 minutes per agent call

    for attempt in range(1, max_retries + 1):
        try:
            agent = Agent(
                name=spec.label,
                instructions=instructions,
                model=choice.model,
                output_type=spec.output_model,
            )
            streamed = Runner.run_streamed(agent, current_task, run_config=run_config)
            async with asyncio.timeout(AGENT_TIMEOUT):
                async for _event in streamed.stream_events():
                    pass  # consume the stream to completion
            output = streamed.final_output_as(spec.output_model)
            break
        except Exception as exc:  # noqa: BLE001 — retry loop uses typed error classification
            if is_retryable(exc) and attempt < max_retries:
                base_wait = min(attempt * 30, 120)

                # On JSON/validation errors: shorten the prompt to avoid truncation
                if is_json_error(exc):
                    current_task = task + (
                        "\n\n## IMPORTANT — CONTRAINTE FORMAT\n"
                        "Ta reponse precedente avait un probleme de format JSON.\n"
                        "Assure-toi que ta reponse est un JSON valide et complet.\n"
                        "- Echappe correctement les guillemets et caracteres speciaux.\n"
                        "- Ne coupe PAS le JSON en plein milieu.\n"
                        "- Si necessaire, reduis legerement la longueur pour que le JSON soit complet.\n"
                    )
                    base_wait = min(base_wait, 10)  # faster retry for JSON errors

                # Add jitter to prevent thundering herd on concurrent retries
                jitter = random.uniform(0, base_wait * 0.3)
                wait = base_wait + jitter

                logger.warning(
                    "agent %s attempt %d/%d failed (%s), retrying in %.1fs",
                    spec.code, attempt, max_retries,
                    type(exc).__name__, wait,
                    exc_info=True,
                )
                await asyncio.sleep(wait)
            else:
                raise

    # 5. Parse into DocumentDraft objects
    documents = _parse_output_to_documents(output, spec)
    elapsed_ms = int((time.monotonic() - t0) * 1000)
    logger.info(
        "agent %s produced %d documents in %dms: %s",
        spec.code,
        len(documents),
        elapsed_ms,
        [d.doc_id for d in documents],
    )

    return AgentResult(
        documents=documents,
        model=choice.model,
        provider=choice.provider,
        prompt_sent=task,
        attempt=attempt,
        elapsed_ms=elapsed_ms,
    )
