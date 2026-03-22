"""Shared test helpers for building mock runtime responses."""
from __future__ import annotations
from uuid import uuid4

from cadris_cp.models import (
    ArtifactBlock,
    DossierSection,
    MissionAgent,
    MissionMessage,
    MissionQuestion,
    RuntimeResumeResponse,
    RuntimeStartResponse,
    TimelineItem,
)


def uid(prefix: str = "") -> str:
    return f"{prefix}{uuid4().hex[:8]}"


INTAKE_TEXT = "Je souhaite creer une plateforme de gestion de projets innovante pour les PME."


def make_start_response(*, status="waiting_user") -> RuntimeStartResponse:
    return RuntimeStartResponse(
        summary="Analyse initiale du projet en cours.",
        next_step="Repondez a la question pour affiner le cadrage.",
        artifact_blocks=[
            ArtifactBlock(
                id=uid("block_"),
                title="Vision",
                status="in_progress",
                certainty="unknown",
                summary="Vision a definir.",
                content="Le projet vise a ...",
                sections=[{"key": "vision", "title": "Vision", "content": "Le projet vise a ...", "certainty": "unknown"}],
            ),
        ],
        active_question=MissionQuestion(
            id=uid("q_"), title="Objectif principal",
            body="Quel est l'objectif principal de votre projet ?", status="waiting",
        ),
        active_agents=[
            MissionAgent(
                code="strategist", label="Strategiste", role="Analyse strategique",
                status="waiting", prompt_key="strategist_v1", prompt_version="1.0",
                summary="En attente de la reponse utilisateur.",
            ),
        ],
        recent_messages=[
            MissionMessage(
                id=uid("msg_"), agent_code="strategist", agent_label="Strategiste",
                stage="intake", title="Analyse recue", body="J'ai bien recu votre brief.",
            ),
        ],
        timeline=[
            TimelineItem(id=uid("tl_"), label="Prise de brief", status="completed"),
            TimelineItem(id=uid("tl_"), label="Analyse", status="in_progress"),
            TimelineItem(id=uid("tl_"), label="Dossier", status="not_started"),
        ],
        status=status,
    )


def make_resume_response(*, completed=False) -> RuntimeResumeResponse:
    status = "completed" if completed else "waiting_user"
    resp = RuntimeResumeResponse(
        summary="Le projet se precise.",
        next_step="Dossier en cours de finalisation." if completed else "Repondez a la prochaine question.",
        artifact_blocks=[
            ArtifactBlock(
                id=uid("block_"), title="Vision",
                status="complete" if completed else "in_progress",
                certainty="solid" if completed else "to_confirm",
                summary="Vision clarifiee.", content="Le projet vise a creer une plateforme.",
                sections=[{"key": "vision", "title": "Vision", "content": "Le projet vise a creer une plateforme.", "certainty": "solid" if completed else "to_confirm"}],
            ),
        ],
        active_question=None if completed else MissionQuestion(
            id=uid("q_"), title="Public cible",
            body="Qui est le public cible de votre projet ?", status="waiting",
        ),
        active_agents=[
            MissionAgent(
                code="strategist", label="Strategiste", role="Analyse strategique",
                status="done" if completed else "waiting", prompt_key="strategist_v1",
                prompt_version="1.0", summary="Analyse terminee." if completed else "En attente.",
            ),
        ],
        recent_messages=[
            MissionMessage(
                id=uid("msg_"), agent_code="strategist", agent_label="Strategiste",
                stage="analysis", title="Mise a jour", body="Merci pour votre reponse.",
            ),
        ],
        timeline=[
            TimelineItem(id=uid("tl_"), label="Prise de brief", status="completed"),
            TimelineItem(id=uid("tl_"), label="Analyse", status="completed" if completed else "in_progress"),
            TimelineItem(id=uid("tl_"), label="Dossier", status="completed" if completed else "not_started"),
        ],
        status=status,
    )
    if completed:
        resp.dossier_title = "Dossier de cadrage"
        resp.dossier_summary = "Synthese du projet."
        resp.dossier_sections = [
            DossierSection(id=uid("sec_"), title="Vision", content="Contenu vision.", certainty="solid"),
        ]
        resp.quality_label = "Bon"
    return resp


def create_project(client, auth_headers, name=None):
    if name is None:
        name = f"Projet {uid()}"
    resp = client.post("/api/projects", json={"name": name}, headers=auth_headers)
    assert resp.status_code == 201
    return resp.json()


async def stream_events(*events):
    for event in events:
        yield event
