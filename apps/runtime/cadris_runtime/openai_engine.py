from __future__ import annotations

from datetime import UTC, datetime
from typing import TypeVar

from pydantic import BaseModel, Field

from .agents import build_supervisor_agent, summarize_sentence
from .models import (
    ArtifactBlock,
    DossierSection,
    MissionAgent,
    MissionMessage,
    MissionQuestion,
    RuntimeInputItem,
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
    TimelineItem,
)
from .prompt_loader import load_prompt

FLOW_DOSSIER_TITLES = {
    "demarrage": "Dossier d'execution - Demarrage",
    "projet_flou": "Dossier de recadrage",
    "pivot": "Dossier de pivot",
}

try:
    from agents import Agent, Runner
except Exception as exc:  # pragma: no cover - import guard
    Agent = None
    Runner = None
    AGENTS_IMPORT_ERROR = exc
else:
    AGENTS_IMPORT_ERROR = None

T = TypeVar("T", bound=BaseModel)


class StrategyDraft(BaseModel):
    summary: str = Field(description="Lecture courte du probleme, de la cible et de la promesse.")


class ProductDraft(BaseModel):
    summary: str = Field(description="Lecture courte du scope MVP et de ses limites.")


class SupervisorStartDraft(BaseModel):
    mission_summary: str
    next_step: str
    question_title: str
    question_body: str
    strategy_block_summary: str
    strategy_block_content: str
    product_block_summary: str
    product_block_content: str
    requirements_block_summary: str
    requirements_block_content: str


class SupervisorResumeDraft(BaseModel):
    mission_summary: str
    next_step: str
    strategy_block_summary: str
    strategy_block_content: str
    product_block_summary: str
    product_block_content: str
    requirements_block_summary: str
    requirements_block_content: str
    dossier_summary: str
    problem_section: str
    sources_section: str | None = None
    mvp_section: str
    requirements_section: str
    quality_label: str


def supporting_inputs_task_block(inputs: list[RuntimeInputItem]) -> str:
    if not inputs:
        return "Sources jointes: aucune"

    lines = ["Sources jointes :"]
    for item in inputs[:4]:
        label = item.display_name or item.content
        excerpt = summarize_sentence(item.preview_text or item.content)
        lines.append(f"- {label}: {excerpt}")
    if len(inputs) > 4:
        lines.append(f"- +{len(inputs) - 4} autre(s) source(s)")
    return "\n".join(lines)


def supporting_inputs_section_fallback(inputs: list[RuntimeInputItem]) -> str:
    if not inputs:
        return ""
    return supporting_inputs_task_block(inputs).replace("Sources jointes :", "Sources jointes exploitees par la mission :")


class OpenAIRuntimeEngine:
    provider = "openai"

    def __init__(self, *, model: str, api_key: str | None) -> None:
        self.model = model
        self.api_key = api_key

    def health_payload(self) -> dict[str, object]:
        return {
            "provider": self.provider,
            "ready": self.is_ready(),
            "model": self.model,
        }

    def is_ready(self) -> bool:
        return AGENTS_IMPORT_ERROR is None and bool(self.api_key)

    def _ensure_ready(self) -> None:
        if AGENTS_IMPORT_ERROR is not None:
            raise RuntimeError(f"openai_agents_import_failed: {AGENTS_IMPORT_ERROR}") from AGENTS_IMPORT_ERROR
        if not self.api_key:
            raise RuntimeError("missing_openai_api_key")

    async def _run_structured(self, *, name: str, instructions: str, output_type: type[T], task: str) -> T:
        self._ensure_ready()
        agent = Agent(
            name=name,
            instructions=instructions,
            model=self.model,
            output_type=output_type,
        )
        result = await Runner.run(agent, task)
        return result.final_output_as(output_type)

    async def start_mission(self, payload: RuntimeStartRequest) -> RuntimeStartResponse:
        intake = " ".join(payload.intake_text.split())
        sources_block = supporting_inputs_task_block(payload.supporting_inputs)
        strategy_prompt = load_prompt(f"{payload.flow_code}/strategy/core")
        product_prompt = load_prompt(f"{payload.flow_code}/product/core")
        supervisor_prompt = load_prompt(f"{payload.flow_code}/supervisor/start")

        strategy = await self._run_structured(
            name="Cadris Strategy Core",
            instructions=strategy_prompt.instructions,
            output_type=StrategyDraft,
            task=(
                f"Projet: {payload.project_name}\n"
                f"Mission: {payload.mission_id}\n"
                f"Intake: {intake}\n"
                f"{sources_block}\n"
                "Produis une lecture courte, claire et exploitable pour le bloc Strategie."
            ),
        )
        product = await self._run_structured(
            name="Cadris Product Core",
            instructions=product_prompt.instructions,
            output_type=ProductDraft,
            task=(
                f"Projet: {payload.project_name}\n"
                f"Mission: {payload.mission_id}\n"
                f"Intake: {intake}\n"
                f"{sources_block}\n"
                "Reduis le scope vers la tranche verticale Demarrage et explicite les limites du MVP."
            ),
        )
        supervisor = await self._run_structured(
            name="Cadris Supervisor Start",
            instructions=supervisor_prompt.instructions,
            output_type=SupervisorStartDraft,
            task=(
                f"Projet: {payload.project_name}\n"
                f"Mission: {payload.mission_id}\n"
                f"Intake: {intake}\n"
                f"{sources_block}\n"
                f"Note strategie: {strategy.summary}\n"
                f"Note produit: {product.summary}\n"
                "Fusionne ces lectures en une synthese de mission et une seule question utilisateur."
            ),
        )

        return RuntimeStartResponse(
            summary=supervisor.mission_summary,
            next_step=supervisor.next_step,
            artifact_blocks=[
                ArtifactBlock(
                    id=f"{payload.mission_id}:artifact:strategy",
                    title="Bloc Strategie",
                    status="in_progress",
                    certainty="to_confirm",
                    summary=supervisor.strategy_block_summary,
                    content=supervisor.strategy_block_content,
                ),
                ArtifactBlock(
                    id=f"{payload.mission_id}:artifact:product",
                    title="Bloc Produit",
                    status="ready_to_decide",
                    certainty="unknown",
                    summary=supervisor.product_block_summary,
                    content=supervisor.product_block_content,
                ),
                ArtifactBlock(
                    id=f"{payload.mission_id}:artifact:requirements",
                    title="Bloc Exigences",
                    status="not_started",
                    certainty="blocking",
                    summary=supervisor.requirements_block_summary,
                    content=supervisor.requirements_block_content,
                ),
            ],
            active_question=MissionQuestion(
                id=f"{payload.mission_id}:question:1",
                title=supervisor.question_title,
                body=supervisor.question_body,
            ),
            active_agents=[
                build_supervisor_agent(
                    status="waiting",
                    summary="Le supervisor a fusionne les notes OpenAI et ouvert une question utile.",
                    prompt_key=supervisor_prompt.key,
                ),
                self._agent(
                    code="strategy",
                    label="Agent Strategie",
                    role="Clarifie promesse, probleme et cible.",
                    status="active",
                    prompt_key=strategy_prompt.key,
                    prompt_version=strategy_prompt.version,
                    summary=strategy.summary,
                ),
                self._agent(
                    code="product",
                    label="Agent Produit",
                    role="Reduit le scope vers la tranche verticale utile.",
                    status="active",
                    prompt_key=product_prompt.key,
                    prompt_version=product_prompt.version,
                    summary=product.summary,
                ),
            ],
            recent_messages=[
                self._message(payload.mission_id, "strategy", "Agent Strategie", "start", "Lecture strategie initiale", strategy.summary),
                self._message(payload.mission_id, "product", "Agent Produit", "start", "Lecture produit initiale", product.summary),
                self._message(
                    payload.mission_id,
                    "supervisor",
                    "Supervisor",
                    "start",
                    "Synthese supervisor",
                    supervisor.mission_summary,
                ),
            ],
            timeline=[
                TimelineItem(id="intake", label="Intake recu", status="completed"),
                TimelineItem(id="synthese", label="Premiere synthese", status="completed"),
                TimelineItem(id="question", label="Question utile", status="waiting_user"),
                TimelineItem(id="dossier", label="Premier dossier", status="not_started"),
            ],
            status="waiting_user",
        )

    async def resume_mission(self, payload: RuntimeResumeRequest) -> RuntimeResumeResponse:
        from .orchestrator import build_resume_response, MAX_CYCLES

        if payload.cycle_number < MAX_CYCLES:
            return build_resume_response(payload)

        intake = " ".join(payload.intake_text.split())
        answer = " ".join(payload.answer_text.split())
        sources_block = supporting_inputs_task_block(payload.supporting_inputs)
        strategy_prompt = load_prompt(f"{payload.flow_code}/strategy/core")
        product_prompt = load_prompt(f"{payload.flow_code}/product/core")
        supervisor_prompt = load_prompt(f"{payload.flow_code}/supervisor/resume")

        strategy = await self._run_structured(
            name="Cadris Strategy Resume",
            instructions=strategy_prompt.instructions,
            output_type=StrategyDraft,
            task=(
                f"Projet: {payload.project_name}\n"
                f"Mission: {payload.mission_id}\n"
                f"Intake initial: {intake}\n"
                f"Reponse utilisateur: {answer}\n"
                f"{sources_block}\n"
                "Mets a jour la lecture strategie apres arbitrage utilisateur."
            ),
        )
        product = await self._run_structured(
            name="Cadris Product Resume",
            instructions=product_prompt.instructions,
            output_type=ProductDraft,
            task=(
                f"Projet: {payload.project_name}\n"
                f"Mission: {payload.mission_id}\n"
                f"Intake initial: {intake}\n"
                f"Reponse utilisateur: {answer}\n"
                f"{sources_block}\n"
                "Mets a jour la lecture produit apres arbitrage utilisateur."
            ),
        )
        supervisor = await self._run_structured(
            name="Cadris Supervisor Resume",
            instructions=supervisor_prompt.instructions,
            output_type=SupervisorResumeDraft,
            task=(
                f"Projet: {payload.project_name}\n"
                f"Mission: {payload.mission_id}\n"
                f"Intake initial: {intake}\n"
                f"Reponse utilisateur: {answer}\n"
                f"{sources_block}\n"
                f"Note strategie: {strategy.summary}\n"
                f"Note produit: {product.summary}\n"
                "Consolide un premier dossier Cadris lisible et pret a relire."
            ),
        )

        return RuntimeResumeResponse(
            summary=supervisor.mission_summary,
            next_step=supervisor.next_step,
            artifact_blocks=[
                ArtifactBlock(
                    id=f"{payload.mission_id}:artifact:strategy",
                    title="Bloc Strategie",
                    status="complete",
                    certainty="solid",
                    summary=supervisor.strategy_block_summary,
                    content=supervisor.strategy_block_content,
                ),
                ArtifactBlock(
                    id=f"{payload.mission_id}:artifact:product",
                    title="Bloc Produit",
                    status="ready_to_decide",
                    certainty="to_confirm",
                    summary=supervisor.product_block_summary,
                    content=supervisor.product_block_content,
                ),
                ArtifactBlock(
                    id=f"{payload.mission_id}:artifact:requirements",
                    title="Bloc Exigences",
                    status="in_progress",
                    certainty="to_confirm",
                    summary=supervisor.requirements_block_summary,
                    content=supervisor.requirements_block_content,
                ),
            ],
            active_agents=[
                build_supervisor_agent(
                    status="done",
                    summary="Le supervisor a consolide les sorties OpenAI en premier dossier exploitable.",
                    prompt_key=supervisor_prompt.key,
                ),
                self._agent(
                    code="strategy",
                    label="Agent Strategie",
                    role="Clarifie promesse, probleme et cible.",
                    status="done",
                    prompt_key=strategy_prompt.key,
                    prompt_version=strategy_prompt.version,
                    summary=strategy.summary,
                ),
                self._agent(
                    code="product",
                    label="Agent Produit",
                    role="Reduit le scope vers la tranche verticale utile.",
                    status="done",
                    prompt_key=product_prompt.key,
                    prompt_version=product_prompt.version,
                    summary=product.summary,
                ),
            ],
            recent_messages=[
                self._message(payload.mission_id, "strategy", "Agent Strategie", "resume", "Lecture strategie apres reponse", strategy.summary),
                self._message(payload.mission_id, "product", "Agent Produit", "resume", "Lecture produit apres reponse", product.summary),
                self._message(
                    payload.mission_id,
                    "supervisor",
                    "Supervisor",
                    "resume",
                    "Consolidation finale",
                    summarize_sentence(supervisor.dossier_summary),
                ),
            ],
            timeline=[
                TimelineItem(id="intake", label="Intake recu", status="completed"),
                TimelineItem(id="synthese", label="Premiere synthese", status="completed"),
                TimelineItem(id="question", label="Question utile", status="completed"),
                TimelineItem(id="dossier", label="Premier dossier", status="completed"),
            ],
            status="completed",
            dossier_title=FLOW_DOSSIER_TITLES.get(payload.flow_code, f"Dossier - {payload.flow_code}"),
            dossier_summary=supervisor.dossier_summary,
            dossier_sections=[
                DossierSection(
                    id="vision",
                    title="Vision produit",
                    content=(
                        "Cadris doit exister pour donner un cadre de travail serieux aux createurs de projets, "
                        "sans les forcer a porter seuls la charge de cadrage inter-metier."
                    ),
                    certainty="solid",
                ),
                DossierSection(
                    id="problem",
                    title="Probleme utilisateur",
                    content=supervisor.problem_section,
                    certainty="solid",
                ),
                *(
                    [
                        DossierSection(
                            id="sources",
                            title="Sources jointes",
                            content=supervisor.sources_section or supporting_inputs_section_fallback(payload.supporting_inputs),
                            certainty="to_confirm",
                        )
                    ]
                    if payload.supporting_inputs
                    else []
                ),
                DossierSection(
                    id="mvp",
                    title="Boucle MVP retenue",
                    content=supervisor.mvp_section,
                    certainty="to_confirm",
                ),
                DossierSection(
                    id="requirements",
                    title="Exigences V1",
                    content=supervisor.requirements_section,
                    certainty="to_confirm",
                ),
            ],
            quality_label=supervisor.quality_label,
        )

    @staticmethod
    def _agent(
        *,
        code: str,
        label: str,
        role: str,
        status: str,
        prompt_key: str,
        prompt_version: str,
        summary: str,
    ) -> MissionAgent:
        return MissionAgent(
            code=code,
            label=label,
            role=role,
            status=status,
            prompt_key=prompt_key,
            prompt_version=prompt_version,
            summary=summary,
        )

    @staticmethod
    def _message(mission_id: str, agent_code: str, agent_label: str, stage: str, title: str, body: str) -> MissionMessage:
        return MissionMessage(
            id=f"{mission_id}:{agent_code}:{stage}",
            agent_code=agent_code,
            agent_label=agent_label,
            stage=stage,
            title=title,
            body=body,
            created_at=datetime.now(UTC).isoformat(),
        )
