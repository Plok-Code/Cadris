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
import time
from dataclasses import dataclass, field
from typing import TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

from .agent_specs import AgentSpec, DocSpec
from .memory import DocumentDraft, MissionMemory
from .model_config import ModelChoice, get_model_for_agent
from .prompt_loader import load_prompt
from .config import settings


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
except Exception as exc:
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


# ── Context builders ──────────────────────────────────────────


def _build_context(spec: AgentSpec, memory: MissionMemory) -> str:
    """Build the context string an agent sees from other agents' work.

    MAX_CHARS_PER_DOC controls context window usage per doc.
    """
    max_chars = 1200

    other_docs = memory.get_documents_for_agent(spec.code)
    if not other_docs:
        return "Aucun document d'autres agents n'est encore disponible."

    if spec.reads_from:
        other_docs = [d for d in other_docs if d.agent_code in spec.reads_from]

    if not other_docs:
        return "Aucun document pertinent d'autres agents n'est encore disponible."

    sections: list[str] = []
    for doc in other_docs:
        content = doc.content
        if len(content) > max_chars:
            content = content[:max_chars] + "\n\n[... tronque pour concision]"
        sections.append(
            f"### {doc.title} (par {doc.agent_code}, certitude: {doc.certainty})\n{content}"
        )
    return "\n\n".join(sections)


def _build_qualification_context(memory: MissionMemory) -> str:
    """Build context from qualification answers (pre-wave user responses)."""
    if not memory.qualification_answers:
        return ""
    lines = ["## Informations complementaires (qualification utilisateur)"]
    for question, answer in memory.qualification_answers.items():
        lines.append(f"**Q:** {question}\n**R:** {answer}")
    return "\n\n".join(lines)


def _build_questions_context(memory: MissionMemory) -> str:
    """Build context about user answers to previous questions."""
    answered = [q for q in memory.questions if q.answered and q.answer]
    if not answered:
        return ""
    lines = ["## Reponses de l'utilisateur"]
    for q in answered:
        lines.append(f"**Q:** {q.question}\n**R:** {q.answer}")
    return "\n\n".join(lines)


# ── Document path mapping (mirrors control-plane DOC_ID_TO_ZIP_PATH) ─────

DOC_ID_TO_ZIP_PATH = {
    "implementation_plan": "CLAUDE.md",
    "user_guide": "user_guide.md",
    "executive_summary": "executive_summary.md",
    "vision_produit": "01-strategy/vision_produit.md",
    "problem_statement": "01-strategy/problem_statement.md",
    "icp_personas": "01-strategy/icp_personas.md",
    "value_proposition": "01-strategy/value_proposition.md",
    "business_model": "02-business/business_model.md",
    "pricing_strategy": "02-business/pricing_strategy.md",
    "market_analysis": "02-business/market_analysis.md",
    "scope_document": "03-product/scope_document.md",
    "mvp_definition": "03-product/mvp_definition.md",
    "prd": "03-product/prd.md",
    "user_stories": "03-product/user_stories.md",
    "feature_specs": "03-product/feature_specs.md",
    "architecture": "04-technical/architecture.md",
    "tech_stack": "04-technical/tech_stack.md",
    "data_model": "04-technical/data_model.md",
    "api_spec": "04-technical/api_spec.md",
    "nfr_security": "04-technical/nfr_security.md",
    "ux_principles": "05-design/ux_principles.md",
    "information_architecture": "05-design/information_architecture.md",
    "design_system": "05-design/design_system.md",
    "dossier_consolide": "06-synthesis/dossier_consolide.md",
}


def _build_file_map_context() -> str:
    """Build an explicit file path reference for the consolidation agent.

    This prevents Llama (and any model) from hallucinating file paths
    in implementation_plan and user_guide documents.
    Paths are relative to the project root (after unzipping).
    """
    lines = [
        "## REFERENCE OBLIGATOIRE — Chemins de fichiers a la racine du projet",
        "",
        "Apres avoir dezippe le dossier Cadris a la RACINE du projet,",
        "voici la carte EXACTE des fichiers. Utilise UNIQUEMENT ces chemins :",
        "",
    ]
    for doc_id, path in DOC_ID_TO_ZIP_PATH.items():
        if doc_id in ("implementation_plan", "user_guide", "executive_summary", "dossier_consolide"):
            continue  # Skip consolidation's own docs
        lines.append(f"- `{path}` ({doc_id})")
    lines.append("")
    lines.append("NE JAMAIS inventer de chemins. NE JAMAIS utiliser 06-ux/, 07-synthesis/ ou autre.")
    lines.append("NE JAMAIS dire 'dans le zip' — les fichiers sont a la racine du projet.")
    lines.append("Le implementation_plan sera sauvegarde en tant que `CLAUDE.md` a la racine du projet.")
    return "\n".join(lines)


def _build_quality_instructions(plan: str) -> str:
    """Build quality instructions tailored to the plan."""
    if plan == "free":
        return (
            "## Consignes qualite\n"
            "Produis des documents professionnels qui vont a l'essentiel.\n\n"
            "- **Synthese** : resume les points cles de facon claire et actionable. "
            "Pas de remplissage, chaque phrase doit apporter de la valeur.\n"
            "- **Structure** : Markdown — titres (##, ###), tableaux, listes.\n"
            "- **Specificite** : adapte chaque element au projet concret. "
            "Pas de formulations generiques.\n"
            "- **Actionabilite** : chaque section permet de passer a l'action.\n"
            "- **Format** : Markdown pur.\n"
        )
    return (
        "## Consignes qualite\n"
        "Tu produis des livrables de qualite entreprise, dignes d'un cabinet de conseil.\n\n"
        "- **Profondeur** : chaque document doit etre substantiel. Pas de paragraphes de 2 phrases. "
        "Developpe chaque point avec contexte, justification et implications.\n"
        "- **Structure** : Markdown riche — titres (##, ###), tableaux, listes. "
        "Chaque document a des sections clairement delimitees.\n"
        "- **Specificite** : evite les formulations generiques. "
        "Adapte chaque element au projet concret decrit dans le contexte. "
        "Des exemples concrets, des chiffres, des scenarios d'usage.\n"
        "- **Actionabilite** : chaque section permet de passer a l'action. "
        "Criteres mesurables, decisions explicites.\n"
        "- **Longueur** : vise 800-1500 mots par document (2000+ pour le dossier consolide). "
        "Un document de 200 mots est INSUFFISANT et sera rejete par le critique.\n"
        "- **Format** : Markdown pur. Tableaux pour les comparaisons, "
        "listes pour les enumerations, paragraphes denses pour les analyses.\n"
    )


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

    # 3. Compose the task
    task_parts = [
        f"## Contexte projet\n{memory.intake_text}",
    ]
    if qualification_context:
        task_parts.append(qualification_context)
    if questions_context:
        task_parts.append(questions_context)
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

    for attempt in range(1, max_retries + 1):
        try:
            agent = Agent(
                name=spec.label,
                instructions=instructions,
                model=choice.model,
                output_type=spec.output_model,
            )
            streamed = Runner.run_streamed(agent, current_task, run_config=run_config)
            async for _event in streamed.stream_events():
                pass  # consume the stream to completion
            output = streamed.final_output_as(spec.output_model)
            break
        except Exception as exc:
            err_msg = str(exc).lower()
            is_permanent = any(k in err_msg for k in (
                "insufficient_quota", "invalid_api_key",
            ))
            is_json_error = any(k in err_msg for k in (
                "invalid json", "json_invalid", "eof while parsing",
                "validation error", "expected value",
            ))
            is_retryable = not is_permanent and (is_json_error or any(k in err_msg for k in (
                "connection", "disconnected", "rate", "limit", "timeout",
                "overloaded", "server_error", "502", "503", "529",
            )))

            if is_retryable and attempt < max_retries:
                wait = min(attempt * 30, 120)

                # On JSON/validation errors: shorten the prompt to avoid truncation
                if is_json_error:
                    current_task = task + (
                        "\n\n## IMPORTANT — CONTRAINTE FORMAT\n"
                        "Ta reponse precedente avait un probleme de format JSON.\n"
                        "Assure-toi que ta reponse est un JSON valide et complet.\n"
                        "- Echappe correctement les guillemets et caracteres speciaux.\n"
                        "- Ne coupe PAS le JSON en plein milieu.\n"
                        "- Si necessaire, reduis legerement la longueur pour que le JSON soit complet.\n"
                    )
                    wait = min(wait, 10)  # faster retry for JSON errors

                logger.warning(
                    "agent %s attempt %d/%d failed (%s: %s), retrying in %ds",
                    spec.code, attempt, max_retries,
                    type(exc).__name__, str(exc)[:200], wait,
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
