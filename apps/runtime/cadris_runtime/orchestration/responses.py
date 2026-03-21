"""Main response builders: build_start_response and build_resume_response."""

from __future__ import annotations

from ..models import (
    MissionQuestion,
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
    TimelineItem,
)
from .agents import (
    RuntimeContext,
    build_supervisor_agent,
    run_product_agent,
    run_strategy_agent,
    supporting_inputs_digest,
    supporting_inputs_section,
)
from .artifacts import normalize_text, _build_start_artifacts, _build_intermediate_artifacts, _build_final_artifacts, _first_question
from .dossier import _build_certainty_entries, _build_dossier_sections
from .prompts import FLOW_DOSSIER_TITLES, FLOW_LABELS, MAX_CYCLES, _prompt_key, load_prompt

__all__ = ["build_start_response", "build_resume_response"]


def build_start_response(payload: RuntimeStartRequest) -> RuntimeStartResponse:
    intake = normalize_text(payload.intake_text)
    project_name = payload.project_name.strip()
    ctx = RuntimeContext(mission_id=payload.mission_id, project_name=project_name,
                         intake_text=intake, supporting_inputs=tuple(payload.supporting_inputs))
    flow_code = payload.flow_code
    flow_label = FLOW_LABELS.get(flow_code, flow_code)
    strategy = run_strategy_agent(ctx, stage="start")
    product = run_product_agent(ctx, stage="start")
    sup_prompt = load_prompt(_prompt_key(flow_code, "supervisor", "start"))
    sd = supporting_inputs_digest(ctx.supporting_inputs)

    summary = (f"Cadris a ouvert une mission {flow_label} pour {project_name}. "
               "Le projet est encore partiellement flou, mais une premiere structure utile existe deja.")
    if sd:
        summary += f" Des sources jointes sont deja disponibles : {sd}."
    next_step = "Une reponse utilisateur structurante est requise pour stabiliser la cible et produire un premier dossier."
    if sd:
        next_step += " La reponse doit tenir compte des documents deja attaches."

    supervisor = build_supervisor_agent(
        status="waiting",
        summary="Le supervisor a fusionne les lectures strategie et produit, puis a ouvert une unique question utile avant ecriture du premier dossier.",
        prompt_key=sup_prompt.key,
    )
    sup_msg = strategy.message.model_copy(update={
        "id": f"{payload.mission_id}:supervisor:start", "agent_code": "supervisor",
        "agent_label": "Supervisor", "title": "Synthese supervisor",
        "body": "Le supervisor retient une mission encore partiellement floue. La question prioritaire doit lier probleme, cible et resultat V1.",
    })
    return RuntimeStartResponse(
        summary=summary, next_step=next_step,
        artifact_blocks=_build_start_artifacts(payload.mission_id, intake, sd),
        active_question=_first_question(payload.mission_id, flow_code, sd),
        active_agents=[supervisor, strategy.agent, product.agent],
        recent_messages=[strategy.message, product.message, sup_msg],
        timeline=[
            TimelineItem(id="intake", label="Intake recu", status="completed"),
            TimelineItem(id="synthese", label="Premiere synthese", status="completed"),
            TimelineItem(id="question", label="Question utile", status="waiting_user"),
            TimelineItem(id="dossier", label="Premier dossier", status="not_started"),
        ],
        status="waiting_user",
    )


def build_resume_response(payload: RuntimeResumeRequest) -> RuntimeResumeResponse:
    intake = normalize_text(payload.intake_text)
    answer = normalize_text(payload.answer_text)
    cycle = payload.cycle_number
    ctx = RuntimeContext(mission_id=payload.mission_id, project_name=payload.project_name.strip(),
                         intake_text=intake, answer_text=answer,
                         supporting_inputs=tuple(payload.supporting_inputs))
    strategy = run_strategy_agent(ctx, stage="resume")
    product = run_product_agent(ctx, stage="resume")
    sd = supporting_inputs_digest(ctx.supporting_inputs)
    fc = payload.flow_code
    if cycle >= MAX_CYCLES:
        return _build_final_response(payload, ctx, strategy, product, sd, cycle, fc)
    return _build_intermediate_response(payload, ctx, strategy, product, sd, cycle, fc)


def _build_intermediate_response(payload, ctx, strategy, product, sd, cycle, fc="demarrage"):
    supervisor = build_supervisor_agent(
        status="waiting", summary=f"Le supervisor a integre la reponse du cycle {cycle} et approfondit le cadrage.",
        prompt_key=_prompt_key(fc, "supervisor", "resume"),
    )
    all_answers = list(payload.previous_answers) + [normalize_text(payload.answer_text)]
    acc = " | ".join(all_answers)
    qmap = {
        2: MissionQuestion(id=f"{payload.mission_id}:question:2", title="Preciser le scope MVP",
                           body="Quelles fonctionnalites sont absolument necessaires pour la V1, et lesquelles peuvent attendre ? Y a-t-il des contraintes techniques ou de delai non encore mentionnees ?"),
        3: MissionQuestion(id=f"{payload.mission_id}:question:3", title="Confirmer les priorites et risques",
                           body="Parmi les hypotheses retenues, lesquelles considerez-vous comme les plus risquees ? Y a-t-il des points bloquants que vous n'avez pas encore mentionnes ?"),
    }
    nq = qmap.get(cycle + 1, MissionQuestion(
        id=f"{payload.mission_id}:question:{cycle + 1}", title=f"Approfondissement cycle {cycle + 1}",
        body="Pouvez-vous preciser les points encore flous identifies dans le dernier cycle ?",
    ))
    sup_msg = strategy.message.model_copy(update={
        "id": f"{payload.mission_id}:supervisor:cycle{cycle}", "agent_code": "supervisor",
        "agent_label": "Supervisor", "title": f"Synthese cycle {cycle}",
        "body": f"Le supervisor a integre la reponse du cycle {cycle}. Des points restent a approfondir avant le dossier final.",
    })
    return RuntimeResumeResponse(
        summary=f"La reponse du cycle {cycle} a ete integree. Le cadrage avance mais des points meritent encore une clarification.",
        next_step=f"Repondez a la question suivante pour approfondir le cadrage (cycle {cycle + 1}/{MAX_CYCLES}).",
        artifact_blocks=_build_intermediate_artifacts(payload.mission_id, ctx.intake_text, acc, sd, cycle),
        active_question=nq, certainty_entries=_build_certainty_entries(payload.mission_id, cycle, sd),
        active_agents=[supervisor, strategy.agent, product.agent],
        recent_messages=[strategy.message, product.message, sup_msg],
        timeline=[
            TimelineItem(id="intake", label="Intake recu", status="completed"),
            TimelineItem(id="synthese", label="Premiere synthese", status="completed"),
            TimelineItem(id="question", label=f"Question {cycle}", status="completed"),
            TimelineItem(id=f"question_{cycle + 1}", label=f"Question {cycle + 1}", status="waiting_user"),
            TimelineItem(id="dossier", label="Premier dossier", status="not_started"),
        ],
        status="waiting_user",
    )


def _build_final_response(payload, ctx, strategy, product, sd, cycle, fc="demarrage"):
    src_section = supporting_inputs_section(ctx.supporting_inputs)
    supervisor = build_supervisor_agent(
        status="done", summary="Le supervisor a fusionne toutes les reponses et produit un dossier exploitable.",
        prompt_key=_prompt_key(fc, "supervisor", "resume"),
    )
    all_answers = list(payload.previous_answers) + [normalize_text(payload.answer_text)]
    acc = " | ".join(all_answers)
    summary = f"La mission a integre {cycle} cycles de clarification. Le projet est maintenant assez structure pour produire un dossier lisible."
    if sd:
        summary += f" Les sources jointes ont aussi ete integrees : {sd}."
    timeline = [
        TimelineItem(id="intake", label="Intake recu", status="completed"),
        TimelineItem(id="synthese", label="Premiere synthese", status="completed"),
    ]
    for i in range(1, cycle + 1):
        timeline.append(TimelineItem(id=f"question_{i}", label=f"Question {i}", status="completed"))
    timeline.append(TimelineItem(id="dossier", label="Premier dossier", status="completed"))
    sup_msg = strategy.message.model_copy(update={
        "id": f"{payload.mission_id}:supervisor:final", "agent_code": "supervisor",
        "agent_label": "Supervisor", "title": "Consolidation finale",
        "body": f"Le supervisor a consolide {cycle} cycles de clarification. Le dossier est pret pour relecture.",
    })
    return RuntimeResumeResponse(
        summary=summary,
        next_step="Relire le dossier, verifier ce qui reste a confirmer, puis lancer la prochaine mission si necessaire.",
        artifact_blocks=_build_final_artifacts(payload.mission_id, ctx.intake_text, acc, sd),
        certainty_entries=_build_certainty_entries(payload.mission_id, cycle, sd, final=True),
        active_agents=[supervisor, strategy.agent, product.agent],
        recent_messages=[strategy.message, product.message, sup_msg],
        timeline=timeline, status="completed",
        dossier_title=FLOW_DOSSIER_TITLES.get(fc, f"Dossier - {fc}"),
        dossier_summary=f"Dossier produit apres {cycle} cycles de clarification. Il est suffisant pour une premiere relecture et une prochaine decision.",
        dossier_sections=_build_dossier_sections(ctx, acc, src_section, sd),
        quality_label="Pret a decider",
    )
