from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from .models import MissionAgent, MissionMessage, RuntimeInputItem
from .prompt_loader import load_prompt


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


def summarize_sentence(text: str) -> str:
    clean = " ".join(text.split())
    if len(clean) <= 240:
        return clean
    return f"{clean[:237].rstrip()}..."


@dataclass(frozen=True)
class RuntimeContext:
    mission_id: str
    project_name: str
    intake_text: str
    answer_text: str | None = None
    supporting_inputs: tuple[RuntimeInputItem, ...] = ()


@dataclass(frozen=True)
class AgentDraft:
    agent: MissionAgent
    message: MissionMessage
    synthesis: str


def supporting_inputs_digest(inputs: tuple[RuntimeInputItem, ...], *, limit: int = 2) -> str:
    if not inputs:
        return ""

    parts: list[str] = []
    for item in inputs[:limit]:
        label = item.display_name or item.content
        excerpt = summarize_sentence(item.preview_text or item.content)
        parts.append(f"{label}: {excerpt}")

    if len(inputs) > limit:
        parts.append(f"+{len(inputs) - limit} autre(s) source(s)")

    return " | ".join(parts)


def supporting_inputs_section(inputs: tuple[RuntimeInputItem, ...], *, limit: int = 4) -> str:
    if not inputs:
        return ""

    lines = ["Sources jointes exploitees par la mission :"]
    for item in inputs[:limit]:
        label = item.display_name or item.content
        excerpt = summarize_sentence(item.preview_text or item.content)
        lines.append(f"- {label}: {excerpt}")

    if len(inputs) > limit:
        lines.append(f"- +{len(inputs) - limit} autre(s) source(s) disponibles dans la mission")

    return "\n".join(lines)


def build_supervisor_agent(status: str, summary: str, prompt_key: str) -> MissionAgent:
    prompt = load_prompt(prompt_key)
    return MissionAgent(
        code="supervisor",
        label="Supervisor",
        role="Coordonne la mission et fusionne les arbitrages.",
        status=status,
        prompt_key=prompt.key,
        prompt_version=prompt.version,
        summary=summary,
    )


def run_strategy_agent(context: RuntimeContext, *, stage: str) -> AgentDraft:
    prompt = load_prompt("demarrage/strategy/core")
    base = summarize_sentence(context.intake_text)
    source_digest = supporting_inputs_digest(context.supporting_inputs)
    if context.answer_text:
        synthesis = (
            "La promesse devient plus credible : "
            f"{summarize_sentence(context.answer_text)} "
            "Le coeur de valeur est relie a un probleme concret, mais quelques preuves restent a confirmer."
        )
        if source_digest:
            synthesis += f" Sources jointes prises en compte : {source_digest}."
        title = "Lecture strategie apres reponse"
    else:
        synthesis = (
            "La mission detecte une promesse encore partiellement floue. "
            f"Point d'appui actuel : {base}"
        )
        if source_digest:
            synthesis += f" Sources deja jointes : {source_digest}."
        title = "Lecture strategie initiale"

    agent = MissionAgent(
        code="strategy",
        label="Agent Strategie",
        role="Clarifie promesse, probleme et cible.",
        status="done" if context.answer_text else "active",
        prompt_key=prompt.key,
        prompt_version=prompt.version,
        summary=synthesis,
    )
    message = MissionMessage(
        id=f"{context.mission_id}:strategy:{stage}",
        agent_code=agent.code,
        agent_label=agent.label,
        stage=stage,
        title=title,
        body=synthesis,
        created_at=utc_now(),
    )
    return AgentDraft(agent=agent, message=message, synthesis=synthesis)


def run_product_agent(context: RuntimeContext, *, stage: str) -> AgentDraft:
    prompt = load_prompt("demarrage/product/core")
    source_digest = supporting_inputs_digest(context.supporting_inputs)
    if context.answer_text:
        synthesis = (
            "La boucle MVP est maintenant plus nette : mission, question, reponse, artefact, dossier. "
            "Les extensions documentaires restent explicitement hors tranche."
        )
        if source_digest:
            synthesis += f" Les sources jointes nourrissent le dossier via apercu local : {source_digest}."
        title = "Lecture produit apres reponse"
    else:
        synthesis = (
            "Le scope doit rester serre sur Demarrage. "
            "Le MVP ne doit pas depasser la boucle mission -> question -> reponse -> dossier."
        )
        if source_digest:
            synthesis += " Les sources jointes doivent rester exploitees via ingestion locale simple, sans ouvrir File Search."
        title = "Lecture produit initiale"

    agent = MissionAgent(
        code="product",
        label="Agent Produit",
        role="Reduit le scope vers la tranche verticale utile.",
        status="done" if context.answer_text else "active",
        prompt_key=prompt.key,
        prompt_version=prompt.version,
        summary=synthesis,
    )
    message = MissionMessage(
        id=f"{context.mission_id}:product:{stage}",
        agent_code=agent.code,
        agent_label=agent.label,
        stage=stage,
        title=title,
        body=synthesis,
        created_at=utc_now(),
    )
    return AgentDraft(agent=agent, message=message, synthesis=synthesis)
