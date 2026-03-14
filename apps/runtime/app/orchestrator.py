from __future__ import annotations

from .agents import (
    RuntimeContext,
    build_supervisor_agent,
    run_product_agent,
    run_strategy_agent,
    supporting_inputs_digest,
    supporting_inputs_section,
)
from .models import (
    ArtifactBlock,
    ArtifactSection,
    CertaintyEntry,
    DossierSection,
    MissionQuestion,
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
    TimelineItem,
)
from .prompt_loader import load_prompt

MAX_CYCLES = 3

FLOW_LABELS: dict[str, str] = {
    "demarrage": "Demarrage",
    "projet_flou": "Recadrage",
    "pivot": "Pivot",
}

FLOW_DOSSIER_TITLES: dict[str, str] = {
    "demarrage": "Dossier d'execution - Demarrage",
    "projet_flou": "Dossier de recadrage",
    "pivot": "Dossier de pivot",
}


def _prompt_key(flow_code: str, role: str, stage: str) -> str:
    return f"{flow_code}/{role}/{stage}"


def build_start_response(payload: RuntimeStartRequest) -> RuntimeStartResponse:
    intake = normalize_text(payload.intake_text)
    project_name = payload.project_name.strip()
    context = RuntimeContext(
        mission_id=payload.mission_id,
        project_name=project_name,
        intake_text=intake,
        supporting_inputs=tuple(payload.supporting_inputs),
    )
    flow_code = payload.flow_code
    flow_label = FLOW_LABELS.get(flow_code, flow_code)
    strategy = run_strategy_agent(context, stage="start")
    product = run_product_agent(context, stage="start")
    supervisor_prompt = load_prompt(_prompt_key(flow_code, "supervisor", "start"))
    source_digest = supporting_inputs_digest(context.supporting_inputs)
    summary = (
        f"Cadris a ouvert une mission {flow_label} pour {project_name}. "
        f"Le projet est encore partiellement flou, mais une premiere structure utile existe deja."
    )
    if source_digest:
        summary += f" Des sources jointes sont deja disponibles : {source_digest}."
    next_step = "Une reponse utilisateur structurante est requise pour stabiliser la cible et produire un premier dossier."
    if source_digest:
        next_step += " La reponse doit tenir compte des documents deja attaches."
    artifact_blocks = _build_start_artifacts(payload.mission_id, intake, source_digest)
    question = _first_question(payload.mission_id, flow_code, source_digest)
    timeline = [
        TimelineItem(id="intake", label="Intake recu", status="completed"),
        TimelineItem(id="synthese", label="Premiere synthese", status="completed"),
        TimelineItem(id="question", label="Question utile", status="waiting_user"),
        TimelineItem(id="dossier", label="Premier dossier", status="not_started"),
    ]
    supervisor = build_supervisor_agent(
        status="waiting",
        summary=(
            "Le supervisor a fusionne les lectures strategie et produit, puis a ouvert une unique question utile "
            "avant ecriture du premier dossier."
        ),
        prompt_key=supervisor_prompt.key,
    )
    messages = [
        strategy.message,
        product.message,
        strategy.message.model_copy(
            update={
                "id": f"{payload.mission_id}:supervisor:start",
                "agent_code": "supervisor",
                "agent_label": "Supervisor",
                "title": "Synthese supervisor",
                "body": (
                    "Le supervisor retient une mission encore partiellement floue. "
                    "La question prioritaire doit lier probleme, cible et resultat V1."
                ),
            }
        ),
    ]
    return RuntimeStartResponse(
        summary=summary,
        next_step=next_step,
        artifact_blocks=artifact_blocks,
        active_question=question,
        active_agents=[supervisor, strategy.agent, product.agent],
        recent_messages=messages,
        timeline=timeline,
        status="waiting_user",
    )


def build_resume_response(payload: RuntimeResumeRequest) -> RuntimeResumeResponse:
    intake = normalize_text(payload.intake_text)
    answer = normalize_text(payload.answer_text)
    cycle = payload.cycle_number
    is_final = cycle >= MAX_CYCLES
    context = RuntimeContext(
        mission_id=payload.mission_id,
        project_name=payload.project_name.strip(),
        intake_text=intake,
        answer_text=answer,
        supporting_inputs=tuple(payload.supporting_inputs),
    )
    strategy = run_strategy_agent(context, stage="resume")
    product = run_product_agent(context, stage="resume")
    source_digest = supporting_inputs_digest(context.supporting_inputs)

    flow_code = payload.flow_code
    if is_final:
        return _build_final_response(payload, context, strategy, product, source_digest, cycle, flow_code)
    else:
        return _build_intermediate_response(payload, context, strategy, product, source_digest, cycle, flow_code)


def _build_intermediate_response(payload, context, strategy, product, source_digest, cycle, flow_code="demarrage"):
    supervisor = build_supervisor_agent(
        status="waiting",
        summary=f"Le supervisor a integre la reponse du cycle {cycle} et approfondit le cadrage.",
        prompt_key=_prompt_key(flow_code, "supervisor", "resume"),
    )
    all_answers = list(payload.previous_answers) + [normalize_text(payload.answer_text)]
    accumulated_context = " | ".join(all_answers)

    artifact_blocks = _build_intermediate_artifacts(
        payload.mission_id, context.intake_text, accumulated_context, source_digest, cycle
    )
    certainty_entries = _build_certainty_entries(payload.mission_id, cycle, source_digest)

    question_map = {
        2: MissionQuestion(
            id=f"{payload.mission_id}:question:2",
            title="Preciser le scope MVP",
            body=(
                "Quelles fonctionnalites sont absolument necessaires pour la V1, "
                "et lesquelles peuvent attendre ? "
                "Y a-t-il des contraintes techniques ou de delai non encore mentionnees ?"
            ),
        ),
        3: MissionQuestion(
            id=f"{payload.mission_id}:question:3",
            title="Confirmer les priorites et risques",
            body=(
                "Parmi les hypotheses retenues, lesquelles considerez-vous comme les plus risquees ? "
                "Y a-t-il des points bloquants que vous n'avez pas encore mentionnes ?"
            ),
        ),
    }
    next_question = question_map.get(cycle + 1, MissionQuestion(
        id=f"{payload.mission_id}:question:{cycle + 1}",
        title=f"Approfondissement cycle {cycle + 1}",
        body="Pouvez-vous preciser les points encore flous identifies dans le dernier cycle ?",
    ))

    timeline = [
        TimelineItem(id="intake", label="Intake recu", status="completed"),
        TimelineItem(id="synthese", label="Premiere synthese", status="completed"),
        TimelineItem(id="question", label=f"Question {cycle}", status="completed"),
        TimelineItem(id=f"question_{cycle + 1}", label=f"Question {cycle + 1}", status="waiting_user"),
        TimelineItem(id="dossier", label="Premier dossier", status="not_started"),
    ]

    return RuntimeResumeResponse(
        summary=(
            f"La reponse du cycle {cycle} a ete integree. "
            f"Le cadrage avance mais des points meritent encore une clarification."
        ),
        next_step=f"Repondez a la question suivante pour approfondir le cadrage (cycle {cycle + 1}/{MAX_CYCLES}).",
        artifact_blocks=artifact_blocks,
        active_question=next_question,
        certainty_entries=certainty_entries,
        active_agents=[supervisor, strategy.agent, product.agent],
        recent_messages=[
            strategy.message,
            product.message,
            strategy.message.model_copy(
                update={
                    "id": f"{payload.mission_id}:supervisor:cycle{cycle}",
                    "agent_code": "supervisor",
                    "agent_label": "Supervisor",
                    "title": f"Synthese cycle {cycle}",
                    "body": (
                        f"Le supervisor a integre la reponse du cycle {cycle}. "
                        "Des points restent a approfondir avant le dossier final."
                    ),
                }
            ),
        ],
        timeline=timeline,
        status="waiting_user",
    )


def _build_final_response(payload, context, strategy, product, source_digest, cycle, flow_code="demarrage"):
    source_section = supporting_inputs_section(context.supporting_inputs)
    supervisor = build_supervisor_agent(
        status="done",
        summary="Le supervisor a fusionne toutes les reponses et produit un dossier exploitable.",
        prompt_key=_prompt_key(flow_code, "supervisor", "resume"),
    )
    all_answers = list(payload.previous_answers) + [normalize_text(payload.answer_text)]
    accumulated_context = " | ".join(all_answers)

    summary = (
        f"La mission a integre {cycle} cycles de clarification. "
        "Le projet est maintenant assez structure pour produire un dossier lisible."
    )
    if source_digest:
        summary += f" Les sources jointes ont aussi ete integrees : {source_digest}."

    artifact_blocks = _build_final_artifacts(payload.mission_id, context.intake_text, accumulated_context, source_digest)
    certainty_entries = _build_certainty_entries(payload.mission_id, cycle, source_digest, final=True)

    timeline = [
        TimelineItem(id="intake", label="Intake recu", status="completed"),
        TimelineItem(id="synthese", label="Premiere synthese", status="completed"),
    ]
    for i in range(1, cycle + 1):
        timeline.append(TimelineItem(id=f"question_{i}", label=f"Question {i}", status="completed"))
    timeline.append(TimelineItem(id="dossier", label="Premier dossier", status="completed"))

    sections = _build_dossier_sections(context, accumulated_context, source_section, source_digest)

    return RuntimeResumeResponse(
        summary=summary,
        next_step="Relire le dossier, verifier ce qui reste a confirmer, puis lancer la prochaine mission si necessaire.",
        artifact_blocks=artifact_blocks,
        certainty_entries=certainty_entries,
        active_agents=[supervisor, strategy.agent, product.agent],
        recent_messages=[
            strategy.message,
            product.message,
            strategy.message.model_copy(
                update={
                    "id": f"{payload.mission_id}:supervisor:final",
                    "agent_code": "supervisor",
                    "agent_label": "Supervisor",
                    "title": "Consolidation finale",
                    "body": (
                        f"Le supervisor a consolide {cycle} cycles de clarification. "
                        "Le dossier est pret pour relecture."
                    ),
                }
            ),
        ],
        timeline=timeline,
        status="completed",
        dossier_title=FLOW_DOSSIER_TITLES.get(flow_code, f"Dossier - {flow_code}"),
        dossier_summary=(
            f"Dossier produit apres {cycle} cycles de clarification. "
            "Il est suffisant pour une premiere relecture et une prochaine decision."
        ),
        dossier_sections=sections,
        quality_label="Pret a decider",
    )


# ---------------------------------------------------------------------------
# Flow-specific first questions
# ---------------------------------------------------------------------------

def _first_question(mission_id: str, flow_code: str, source_digest: str) -> MissionQuestion:
    source_hint = " Appuie-toi aussi sur les sources jointes si elles apportent des preuves utiles." if source_digest else ""
    questions: dict[str, tuple[str, str]] = {
        "demarrage": (
            "Clarifier le coeur du projet",
            f"Quel probleme principal resolvez-vous, pour qui exactement, et quel resultat concret doit exister des la V1 ?{source_hint}",
        ),
        "projet_flou": (
            "Identifier l'incoherence principale",
            f"Qu'est-ce qui ne colle plus dans le projet tel qu'il existe aujourd'hui ? Ou sentez-vous que les decisions se contredisent ?{source_hint}",
        ),
        "pivot": (
            "Definir le declencheur du pivot",
            f"Quel evenement ou constat a declenche ce changement de direction ? Qu'est-ce qui doit absolument changer, et qu'est-ce qui peut rester ?{source_hint}",
        ),
    }
    title, body = questions.get(flow_code, questions["demarrage"])
    return MissionQuestion(
        id=f"{mission_id}:question:1",
        title=title,
        body=body,
    )


# ---------------------------------------------------------------------------
# Artifact builders
# ---------------------------------------------------------------------------

def _build_start_artifacts(mission_id, intake, source_digest):
    intake_short = summarize_sentence(intake)
    return [
        ArtifactBlock(
            id=f"{mission_id}:artifact:strategy",
            title="Bloc Strategie",
            status="in_progress",
            certainty="to_confirm",
            summary="Premier cadrage de la promesse et du probleme.",
            content=(
                f"Vision provisoire : {intake_short} "
                "Le probleme, la cible et la preuve de valeur doivent etre clarifies."
                + (f" Sources jointes : {source_digest}." if source_digest else "")
            ),
            sections=[
                ArtifactSection(key="promise", title="Promesse", content=f"A preciser a partir de l'intake : {intake_short}", certainty="unknown"),
                ArtifactSection(key="problem", title="Probleme principal", content="Le probleme principal n'est pas encore formule.", certainty="unknown"),
                ArtifactSection(key="target", title="Cible", content="L'utilisateur cible n'est pas encore identifie.", certainty="unknown"),
            ],
        ),
        ArtifactBlock(
            id=f"{mission_id}:artifact:product",
            title="Bloc Produit",
            status="ready_to_decide",
            certainty="unknown",
            summary="Premiere lecture du scope MVP et des dependances critiques.",
            content=(
                "Le systeme a detecte un besoin de cadrage prioritaire sur l'utilisateur cible, "
                "le probleme principal et la boucle de valeur minimale."
                + (" Des sources sont deja presentes dans la mission." if source_digest else "")
            ),
            sections=[
                ArtifactSection(key="scope", title="Scope MVP", content="Le perimetre V1 n'est pas encore defini.", certainty="unknown"),
                ArtifactSection(key="features", title="Fonctionnalites cles", content="Les fonctionnalites prioritaires restent a identifier.", certainty="unknown"),
                ArtifactSection(key="out_of_scope", title="Hors tranche", content="Les exclusions ne sont pas encore formulees.", certainty="unknown"),
            ],
        ),
        ArtifactBlock(
            id=f"{mission_id}:artifact:requirements",
            title="Bloc Exigences",
            status="not_started",
            certainty="blocking",
            summary="Les exigences V1 critiques doivent encore etre fermees.",
            content=(
                "Les exigences minimales sont seulement esquissees. "
                "Il faut encore confirmer les attentes non fonctionnelles et les contraintes de build."
            ),
            sections=[
                ArtifactSection(key="functional", title="Exigences fonctionnelles", content="A definir apres cadrage.", certainty="blocking"),
                ArtifactSection(key="non_functional", title="Exigences non fonctionnelles", content="A definir apres cadrage.", certainty="blocking"),
                ArtifactSection(key="risks", title="Risques identifies", content="Aucun risque formule pour le moment.", certainty="unknown"),
            ],
        ),
    ]


def _build_intermediate_artifacts(mission_id, intake, accumulated_context, source_digest, cycle):
    intake_short = summarize_sentence(intake)
    context_short = summarize_sentence(accumulated_context)
    cert = "to_confirm" if cycle >= 2 else "unknown"
    return [
        ArtifactBlock(
            id=f"{mission_id}:artifact:strategy",
            title="Bloc Strategie",
            status="in_progress",
            certainty="to_confirm",
            summary=f"Cadrage strategique enrichi apres {cycle} cycle(s).",
            content=(
                f"Vision en cours : {intake_short} "
                f"Clarifications utilisateur : {context_short} "
                "Le probleme et la cible se precisent mais restent a consolider."
                + (f" Sources integrees : {source_digest}." if source_digest else "")
            ),
            sections=[
                ArtifactSection(key="promise", title="Promesse", content=f"En cours de formulation : {intake_short}", certainty=cert),
                ArtifactSection(key="problem", title="Probleme principal", content=f"Precisions utilisateur : {context_short}", certainty=cert),
                ArtifactSection(key="target", title="Cible", content="La cible se precise au fil des reponses.", certainty=cert),
            ],
        ),
        ArtifactBlock(
            id=f"{mission_id}:artifact:product",
            title="Bloc Produit",
            status="in_progress",
            certainty="to_confirm",
            summary=f"Scope produit en cours de convergence (cycle {cycle}).",
            content=(
                "La boucle produit se precise grace aux reponses utilisateur. "
                f"Contexte accumule : {context_short}"
                + (" Les documents joints enrichissent le cadrage." if source_digest else "")
            ),
            sections=[
                ArtifactSection(key="scope", title="Scope MVP", content=f"Convergence en cours : {context_short}", certainty=cert),
                ArtifactSection(key="features", title="Fonctionnalites cles", content="Les fonctionnalites prioritaires commencent a emerger.", certainty="unknown"),
                ArtifactSection(key="out_of_scope", title="Hors tranche", content="Les exclusions se clarifient progressivement.", certainty="unknown"),
            ],
        ),
        ArtifactBlock(
            id=f"{mission_id}:artifact:requirements",
            title="Bloc Exigences",
            status="in_progress",
            certainty="unknown",
            summary="Les exigences convergent mais ne sont pas encore fermees.",
            content=(
                "Les exigences V1 commencent a se structurer. "
                "Certains points non fonctionnels et contraintes de build restent a confirmer."
            ),
            sections=[
                ArtifactSection(key="functional", title="Exigences fonctionnelles", content="En cours de definition.", certainty="unknown"),
                ArtifactSection(key="non_functional", title="Exigences non fonctionnelles", content="Contraintes techniques a confirmer.", certainty="blocking"),
                ArtifactSection(key="risks", title="Risques identifies", content="Les risques commencent a se dessiner.", certainty="unknown"),
            ],
        ),
    ]


def _build_final_artifacts(mission_id, intake, accumulated_context, source_digest):
    intake_short = summarize_sentence(intake)
    context_short = summarize_sentence(accumulated_context)
    return [
        ArtifactBlock(
            id=f"{mission_id}:artifact:strategy",
            title="Bloc Strategie",
            status="complete",
            certainty="solid",
            summary="Vision, probleme et cible sont explicitement relies.",
            content=(
                f"Contexte initial : {intake_short} "
                f"Arbitrages utilisateur : {context_short} "
                "Le produit doit exister pour transformer un projet flou en dossier d'execution exploitable."
                + (f" Sources jointes integrees : {source_digest}." if source_digest else "")
            ),
            sections=[
                ArtifactSection(
                    key="promise", title="Promesse",
                    content="Donner un cadre de travail serieux aux createurs de projets, sans les forcer a porter seuls la charge de cadrage.",
                    certainty="solid",
                ),
                ArtifactSection(
                    key="problem", title="Probleme principal",
                    content=f"Le probleme retenu apres arbitrage : {context_short}",
                    certainty="solid",
                ),
                ArtifactSection(
                    key="target", title="Cible",
                    content="Solo founders et petites equipes early-stage avec un projet SaaS ou digital a cadrer.",
                    certainty="to_confirm",
                ),
            ],
        ),
        ArtifactBlock(
            id=f"{mission_id}:artifact:product",
            title="Bloc Produit",
            status="ready_to_decide",
            certainty="to_confirm",
            summary="Le MVP de demarrage devient concret et demonstratif.",
            content=(
                "La boucle prioritaire retenue est mission -> question -> reponse -> artefact -> dossier. "
                "Les extensions comme PDF, partage et retrieval documentaire restent hors tranche."
            ),
            sections=[
                ArtifactSection(
                    key="scope", title="Scope MVP",
                    content="Flow Demarrage resserre : intake libre, question utile, reprise, dossier markdown.",
                    certainty="to_confirm",
                ),
                ArtifactSection(
                    key="features", title="Fonctionnalites cles",
                    content="Projet, mission, question, artefacts, dossier. Upload fichier en V1 simple.",
                    certainty="to_confirm",
                ),
                ArtifactSection(
                    key="out_of_scope", title="Hors tranche",
                    content="PDF, share links, retrieval documentaire, multi-flow, auth production.",
                    certainty="solid",
                ),
            ],
        ),
        ArtifactBlock(
            id=f"{mission_id}:artifact:requirements",
            title="Bloc Exigences",
            status="in_progress",
            certainty="to_confirm",
            summary="Les exigences V1 deviennent plus concretes, mais pas encore totalement fermees.",
            content=(
                "Les exigences de base convergent vers une auth serveur credible, "
                "un runtime reprenable, une persistence canonique et un dossier markdown lisible."
            ),
            sections=[
                ArtifactSection(
                    key="functional", title="Exigences fonctionnelles",
                    content="Auth serveur minimale, cycle waiting_user -> resume stable, persistence canonique, dossier markdown.",
                    certainty="to_confirm",
                ),
                ArtifactSection(
                    key="non_functional", title="Exigences non fonctionnelles",
                    content="Latence acceptable, runtime reprenable, donnees exportables, pas de lock-in.",
                    certainty="to_confirm",
                ),
                ArtifactSection(
                    key="risks", title="Risques identifies",
                    content="Qualite du cadrage si peu de contexte, contenu generique des agents, adoption utilisateur.",
                    certainty="unknown",
                ),
            ],
        ),
    ]


# ---------------------------------------------------------------------------
# Certainty entries
# ---------------------------------------------------------------------------

def _build_certainty_entries(mission_id, cycle, source_digest, final=False):
    entries = [
        CertaintyEntry(
            id=f"{mission_id}:cert:problem",
            title="Probleme principal",
            status="solid" if final else ("to_confirm" if cycle >= 2 else "unknown"),
            impact="Definit la raison d'etre du produit",
            source_label="Reponses utilisateur",
        ),
        CertaintyEntry(
            id=f"{mission_id}:cert:target",
            title="Utilisateur cible",
            status="solid" if final else ("to_confirm" if cycle >= 2 else "unknown"),
            impact="Determine le cadrage produit et UX",
            source_label="Reponses utilisateur",
        ),
        CertaintyEntry(
            id=f"{mission_id}:cert:mvp_scope",
            title="Scope MVP",
            status="to_confirm" if final else "unknown",
            impact="Fixe le perimetre de la V1",
            source_label="Agent produit",
        ),
        CertaintyEntry(
            id=f"{mission_id}:cert:value_loop",
            title="Boucle de valeur",
            status="to_confirm" if final else ("unknown" if cycle < 2 else "to_confirm"),
            impact="Determine la preuve de valeur minimale",
            source_label="Agent strategie",
        ),
        CertaintyEntry(
            id=f"{mission_id}:cert:nfr",
            title="Exigences non fonctionnelles",
            status="to_confirm" if final else "blocking",
            impact="Contraintes techniques et qualite",
            source_label="Agent exigences",
        ),
    ]
    if source_digest:
        entries.append(
            CertaintyEntry(
                id=f"{mission_id}:cert:sources",
                title="Sources jointes",
                status="to_confirm",
                impact="Enrichissent le cadrage avec des preuves externes",
                source_label="Documents utilisateur",
            )
        )
    return entries


# ---------------------------------------------------------------------------
# Dossier sections
# ---------------------------------------------------------------------------

def _build_dossier_sections(context, accumulated_context, source_section, source_digest):
    sections = [
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
            content=summarize_sentence(accumulated_context),
            certainty="solid",
        ),
        DossierSection(
            id="target",
            title="Utilisateur cible",
            content=(
                "Solo founders et petites equipes early-stage avec un projet SaaS ou digital a cadrer. "
                "Capables de travailler avec l'IA mais soucieux de ne pas laisser les modeles improviser la logique projet."
            ),
            certainty="to_confirm",
        ),
    ]
    if source_section:
        sections.append(
            DossierSection(
                id="sources",
                title="Sources jointes",
                content=source_section,
                certainty="to_confirm",
            )
        )
    sections.extend([
        DossierSection(
            id="mvp",
            title="Boucle MVP retenue",
            content=(
                "La V1 doit prouver la valeur sur le flow Demarrage resserre, "
                "avec mission durable, question utile, reprise et dossier markdown."
            ),
            certainty="to_confirm",
        ),
        DossierSection(
            id="requirements",
            title="Exigences V1",
            content=(
                "La V1 doit garantir une auth serveur minimale, un cycle waiting_user -> resume stable, "
                "une persistence canonique lisible et un dossier markdown transmissible."
            ),
            certainty="to_confirm",
        ),
        DossierSection(
            id="risks",
            title="Risques identifies",
            content=(
                "Les principaux risques portent sur la qualite du cadrage si l'utilisateur fournit peu de contexte, "
                "et sur la capacite des agents a produire du contenu non generique."
            ),
            certainty="unknown",
        ),
    ])
    return sections


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def summarize_sentence(text: str) -> str:
    clean = normalize_text(text)
    if len(clean) <= 240:
        return clean
    return f"{clean[:237].rstrip()}..."


def normalize_text(text: str) -> str:
    return " ".join(text.split())
