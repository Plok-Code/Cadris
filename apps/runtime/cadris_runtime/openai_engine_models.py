"""Draft output models and input helpers for the legacy OpenAI engine.

Extracted from openai_engine.py to keep that module under the 400-line
project limit. These are the structured-output schemas the legacy single-pass
OpenAI engine asks the model to fill, plus the helpers that fold mission
supporting inputs into a prompt block.
"""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from .agents import summarize_sentence
from .models import MissionAgent, MissionMessage, RuntimeInputItem

FLOW_DOSSIER_TITLES = {
    "demarrage": "Dossier d'execution - Demarrage",
    "projet_flou": "Dossier de recadrage",
    "pivot": "Dossier de pivot",
}


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
    return supporting_inputs_task_block(inputs).replace(
        "Sources jointes :", "Sources jointes exploitees par la mission :"
    )


def build_mission_agent(
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


def build_mission_message(
    mission_id: str,
    agent_code: str,
    agent_label: str,
    stage: str,
    title: str,
    body: str,
) -> MissionMessage:
    return MissionMessage(
        id=f"{mission_id}:{agent_code}:{stage}",
        agent_code=agent_code,
        agent_label=agent_label,
        stage=stage,
        title=title,
        body=body,
        created_at=datetime.now(UTC).isoformat(),
    )
