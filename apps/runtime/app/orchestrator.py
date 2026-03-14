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
    DossierSection,
    MissionQuestion,
    RuntimeResumeRequest,
    RuntimeResumeResponse,
    RuntimeStartRequest,
    RuntimeStartResponse,
    TimelineItem,
)
from .prompt_loader import load_prompt


def build_start_response(payload: RuntimeStartRequest) -> RuntimeStartResponse:
    intake = normalize_text(payload.intake_text)
    project_name = payload.project_name.strip()
    context = RuntimeContext(
        mission_id=payload.mission_id,
        project_name=project_name,
        intake_text=intake,
        supporting_inputs=tuple(payload.supporting_inputs),
    )
    strategy = run_strategy_agent(context, stage="start")
    product = run_product_agent(context, stage="start")
    supervisor_prompt = load_prompt("demarrage/supervisor/start")
    source_digest = supporting_inputs_digest(context.supporting_inputs)
    summary = (
        f"Cadris a ouvert une mission Demarrage pour {project_name}. "
        f"Le projet est encore partiellement flou, mais une premiere structure utile existe deja."
    )
    if source_digest:
        summary += f" Des sources jointes sont deja disponibles : {source_digest}."
    next_step = "Une reponse utilisateur structurante est requise pour stabiliser la cible et produire un premier dossier."
    if source_digest:
        next_step += " La reponse doit tenir compte des documents deja attaches."
    artifact_blocks = [
        ArtifactBlock(
            id=f"{payload.mission_id}:artifact:strategy",
            title="Bloc Strategie",
            status="in_progress",
            certainty="to_confirm",
            summary="Premier cadrage de la promesse et du probleme.",
            content=(
                "Vision provisoire : "
                f"{summarize_sentence(intake)} "
                "Le probleme, la cible et la preuve de valeur doivent etre clarifies."
                + (f" Sources jointes : {source_digest}." if source_digest else "")
            ),
        ),
        ArtifactBlock(
            id=f"{payload.mission_id}:artifact:product",
            title="Bloc Produit",
            status="ready_to_decide",
            certainty="unknown",
            summary="Premiere lecture du scope MVP et des dependances critiques.",
            content=(
                "Le systeme a detecte un besoin de cadrage prioritaire sur l'utilisateur cible, "
                "le probleme principal et la boucle de valeur minimale."
                + (
                    " Des sources sont deja presentes dans la mission et doivent seulement enrichir le cadrage local."
                    if source_digest
                    else ""
                )
            ),
        ),
        ArtifactBlock(
            id=f"{payload.mission_id}:artifact:requirements",
            title="Bloc Exigences",
            status="not_started",
            certainty="blocking",
            summary="Les exigences V1 critiques doivent encore etre fermees.",
            content=(
                "Les exigences minimales sont seulement esquissees. "
                "Il faut encore confirmer les attentes non fonctionnelles, les contraintes de build "
                "et les points vraiment bloquants pour la V1."
                + (
                    " L'ingestion V1 doit rester simple : upload, apercu local, usage dans la mission."
                    if source_digest
                    else ""
                )
            ),
        ),
    ]
    question = MissionQuestion(
        id=f"{payload.mission_id}:question:1",
        title="Clarifier le coeur du projet",
        body=(
            "Quel probleme principal resolvez-vous, pour qui exactement, "
            "et quel resultat concret doit exister des la V1 ?"
            + (" Appuie-toi aussi sur les sources jointes si elles apportent des preuves utiles." if source_digest else "")
        ),
    )
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
    source_section = supporting_inputs_section(context.supporting_inputs)
    supervisor = build_supervisor_agent(
        status="done",
        summary="Le supervisor a fusionne la reponse utilisateur et produit un premier dossier exploitable.",
        prompt_key="demarrage/supervisor/resume",
    )
    summary = (
        "La mission a integre la reponse utilisateur. "
        "Le projet est maintenant assez structure pour produire un premier dossier lisible."
    )
    if source_digest:
        summary += f" Les sources jointes ont aussi ete integrees : {source_digest}."
    next_step = "Relire le dossier, verifier ce qui reste a confirmer, puis lancer la prochaine mission si necessaire."
    artifact_blocks = [
        ArtifactBlock(
            id=f"{payload.mission_id}:artifact:strategy",
            title="Bloc Strategie",
            status="complete",
            certainty="solid",
            summary="Vision, probleme et cible sont explicitement relies.",
            content=(
                f"Contexte initial : {summarize_sentence(intake)} "
                f"Arbitrage utilisateur : {summarize_sentence(answer)} "
                "Le produit doit exister pour transformer un projet flou en dossier d'execution exploitable."
                + (f" Sources jointes integrees : {source_digest}." if source_digest else "")
            ),
        ),
        ArtifactBlock(
            id=f"{payload.mission_id}:artifact:product",
            title="Bloc Produit",
            status="ready_to_decide",
            certainty="to_confirm",
            summary="Le MVP de demarrage devient concret et demonstratif.",
            content=(
                "La boucle prioritaire retenue est mission -> question -> reponse -> artefact -> dossier. "
                "Les extensions comme PDF, partage et retrieval documentaire restent hors tranche."
                + (
                    " Les documents joints nourrissent seulement le cadrage local et le premier dossier."
                    if source_digest
                    else ""
                )
            ),
        ),
        ArtifactBlock(
            id=f"{payload.mission_id}:artifact:requirements",
            title="Bloc Exigences",
            status="in_progress",
            certainty="to_confirm",
            summary="Les exigences V1 deviennent plus concretes, mais pas encore totalement fermees.",
            content=(
                "Les exigences de base convergent vers une auth serveur credible, "
                "un runtime reprenable, une persistence canonique et un dossier markdown lisible. "
                "Le detail des integrations et des garanties post-lancement reste a confirmer."
                + (
                    " L'ingestion V1 reste volontairement simple : attacher, apercevoir, reutiliser dans la mission."
                    if source_digest
                    else ""
                )
            ),
        ),
    ]
    timeline = [
        TimelineItem(id="intake", label="Intake recu", status="completed"),
        TimelineItem(id="synthese", label="Premiere synthese", status="completed"),
        TimelineItem(id="question", label="Question utile", status="completed"),
        TimelineItem(id="dossier", label="Premier dossier", status="completed"),
    ]
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
            content=summarize_sentence(answer),
            certainty="solid",
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
    sections.extend(
        [
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
        ]
    )
    return RuntimeResumeResponse(
        summary=summary,
        next_step=next_step,
        artifact_blocks=artifact_blocks,
        active_agents=[supervisor, strategy.agent, product.agent],
        recent_messages=[
            strategy.message,
            product.message,
            strategy.message.model_copy(
                update={
                    "id": f"{payload.mission_id}:supervisor:resume",
                    "agent_code": "supervisor",
                    "agent_label": "Supervisor",
                    "title": "Consolidation finale",
                    "body": (
                        "La reponse utilisateur ferme assez d'inconnus pour livrer un premier dossier. "
                        "Les points encore a confirmer restent visibles dans le bloc produit."
                    ),
                }
            ),
        ],
        timeline=timeline,
        status="completed",
        dossier_title="Dossier d'execution - Demarrage",
        dossier_summary=(
            "Premier dossier produit depuis la base canonique de la mission. "
            "Il est suffisant pour une premiere relecture et une prochaine decision."
        ),
        dossier_sections=sections,
        quality_label="Pret a decider",
    )


def summarize_sentence(text: str) -> str:
    clean = normalize_text(text)
    if len(clean) <= 240:
        return clean
    return f"{clean[:237].rstrip()}..."


def normalize_text(text: str) -> str:
    return " ".join(text.split())
