"""Artifact block builders, first-question helper, and text utilities."""

from __future__ import annotations

from ..models import (
    ArtifactBlock,
    ArtifactSection,
    MissionQuestion,
)

__all__ = [
    "normalize_text",
    "summarize_sentence",
    "_first_question",
    "_build_start_artifacts",
    "_build_intermediate_artifacts",
    "_build_final_artifacts",
]


# -- Text helpers -----------------------------------------------------------

def normalize_text(text: str) -> str:
    return " ".join(text.split())


def summarize_sentence(text: str) -> str:
    clean = normalize_text(text)
    return clean if len(clean) <= 240 else f"{clean[:237].rstrip()}..."


# -- First question ---------------------------------------------------------

def _first_question(mission_id: str, flow_code: str, source_digest: str) -> MissionQuestion:
    hint = " Appuie-toi aussi sur les sources jointes si elles apportent des preuves utiles." if source_digest else ""
    questions: dict[str, tuple[str, str]] = {
        "demarrage": ("Clarifier le coeur du projet",
                      f"Quel probleme principal resolvez-vous, pour qui exactement, et quel resultat concret doit exister des la V1 ?{hint}"),
        "projet_flou": ("Identifier l'incoherence principale",
                        f"Qu'est-ce qui ne colle plus dans le projet tel qu'il existe aujourd'hui ? Ou sentez-vous que les decisions se contredisent ?{hint}"),
        "pivot": ("Definir le declencheur du pivot",
                  f"Quel evenement ou constat a declenche ce changement de direction ? Qu'est-ce qui doit absolument changer, et qu'est-ce qui peut rester ?{hint}"),
    }
    title, body = questions.get(flow_code, questions["demarrage"])
    return MissionQuestion(id=f"{mission_id}:question:1", title=title, body=body)


# -- Shared section factories -----------------------------------------------

def _strategy_sections(intake_short, context_short=None, cert="unknown"):
    if context_short is None:
        return [
            ArtifactSection(key="promise", title="Promesse", content=f"A preciser a partir de l'intake : {intake_short}", certainty="unknown"),
            ArtifactSection(key="problem", title="Probleme principal", content="Le probleme principal n'est pas encore formule.", certainty="unknown"),
            ArtifactSection(key="target", title="Cible", content="L'utilisateur cible n'est pas encore identifie.", certainty="unknown"),
        ]
    return [
        ArtifactSection(key="promise", title="Promesse", content=f"En cours de formulation : {intake_short}", certainty=cert),
        ArtifactSection(key="problem", title="Probleme principal", content=f"Precisions utilisateur : {context_short}", certainty=cert),
        ArtifactSection(key="target", title="Cible", content="La cible se precise au fil des reponses.", certainty=cert),
    ]


def _src(source_digest, prefix=" "):
    return f"{prefix}{source_digest}." if source_digest else ""


# -- Start artifacts --------------------------------------------------------

def _build_start_artifacts(mission_id, intake, source_digest):
    s = summarize_sentence(intake)
    return [
        ArtifactBlock(
            id=f"{mission_id}:artifact:strategy", title="Bloc Strategie", status="in_progress", certainty="to_confirm",
            summary="Premier cadrage de la promesse et du probleme.",
            content=f"Vision provisoire : {s} Le probleme, la cible et la preuve de valeur doivent etre clarifies.{_src(source_digest, ' Sources jointes : ')}",
            sections=_strategy_sections(s),
        ),
        ArtifactBlock(
            id=f"{mission_id}:artifact:product", title="Bloc Produit", status="ready_to_decide", certainty="unknown",
            summary="Premiere lecture du scope MVP et des dependances critiques.",
            content="Le systeme a detecte un besoin de cadrage prioritaire sur l'utilisateur cible, le probleme principal et la boucle de valeur minimale."
                    + (" Des sources sont deja presentes dans la mission." if source_digest else ""),
            sections=[
                ArtifactSection(key="scope", title="Scope MVP", content="Le perimetre V1 n'est pas encore defini.", certainty="unknown"),
                ArtifactSection(key="features", title="Fonctionnalites cles", content="Les fonctionnalites prioritaires restent a identifier.", certainty="unknown"),
                ArtifactSection(key="out_of_scope", title="Hors tranche", content="Les exclusions ne sont pas encore formulees.", certainty="unknown"),
            ],
        ),
        ArtifactBlock(
            id=f"{mission_id}:artifact:requirements", title="Bloc Exigences", status="not_started", certainty="blocking",
            summary="Les exigences V1 critiques doivent encore etre fermees.",
            content="Les exigences minimales sont seulement esquissees. Il faut encore confirmer les attentes non fonctionnelles et les contraintes de build.",
            sections=[
                ArtifactSection(key="functional", title="Exigences fonctionnelles", content="A definir apres cadrage.", certainty="blocking"),
                ArtifactSection(key="non_functional", title="Exigences non fonctionnelles", content="A definir apres cadrage.", certainty="blocking"),
                ArtifactSection(key="risks", title="Risques identifies", content="Aucun risque formule pour le moment.", certainty="unknown"),
            ],
        ),
    ]


# -- Intermediate artifacts -------------------------------------------------

def _build_intermediate_artifacts(mission_id, intake, accumulated_context, source_digest, cycle):
    s, c = summarize_sentence(intake), summarize_sentence(accumulated_context)
    cert = "to_confirm" if cycle >= 2 else "unknown"
    return [
        ArtifactBlock(
            id=f"{mission_id}:artifact:strategy", title="Bloc Strategie", status="in_progress", certainty="to_confirm",
            summary=f"Cadrage strategique enrichi apres {cycle} cycle(s).",
            content=f"Vision en cours : {s} Clarifications utilisateur : {c} Le probleme et la cible se precisent mais restent a consolider.{_src(source_digest, ' Sources integrees : ')}",
            sections=_strategy_sections(s, c, cert),
        ),
        ArtifactBlock(
            id=f"{mission_id}:artifact:product", title="Bloc Produit", status="in_progress", certainty="to_confirm",
            summary=f"Scope produit en cours de convergence (cycle {cycle}).",
            content=f"La boucle produit se precise grace aux reponses utilisateur. Contexte accumule : {c}"
                    + (" Les documents joints enrichissent le cadrage." if source_digest else ""),
            sections=[
                ArtifactSection(key="scope", title="Scope MVP", content=f"Convergence en cours : {c}", certainty=cert),
                ArtifactSection(key="features", title="Fonctionnalites cles", content="Les fonctionnalites prioritaires commencent a emerger.", certainty="unknown"),
                ArtifactSection(key="out_of_scope", title="Hors tranche", content="Les exclusions se clarifient progressivement.", certainty="unknown"),
            ],
        ),
        ArtifactBlock(
            id=f"{mission_id}:artifact:requirements", title="Bloc Exigences", status="in_progress", certainty="unknown",
            summary="Les exigences convergent mais ne sont pas encore fermees.",
            content="Les exigences V1 commencent a se structurer. Certains points non fonctionnels et contraintes de build restent a confirmer.",
            sections=[
                ArtifactSection(key="functional", title="Exigences fonctionnelles", content="En cours de definition.", certainty="unknown"),
                ArtifactSection(key="non_functional", title="Exigences non fonctionnelles", content="Contraintes techniques a confirmer.", certainty="blocking"),
                ArtifactSection(key="risks", title="Risques identifies", content="Les risques commencent a se dessiner.", certainty="unknown"),
            ],
        ),
    ]


# -- Final artifacts --------------------------------------------------------

def _build_final_artifacts(mission_id, intake, accumulated_context, source_digest):
    s, c = summarize_sentence(intake), summarize_sentence(accumulated_context)
    return [
        ArtifactBlock(
            id=f"{mission_id}:artifact:strategy", title="Bloc Strategie", status="complete", certainty="solid",
            summary="Vision, probleme et cible sont explicitement relies.",
            content=f"Contexte initial : {s} Arbitrages utilisateur : {c} Le produit doit exister pour transformer un projet flou en dossier d'execution exploitable.{_src(source_digest, ' Sources jointes integrees : ')}",
            sections=[
                ArtifactSection(key="promise", title="Promesse", content="Donner un cadre de travail serieux aux createurs de projets, sans les forcer a porter seuls la charge de cadrage.", certainty="solid"),
                ArtifactSection(key="problem", title="Probleme principal", content=f"Le probleme retenu apres arbitrage : {c}", certainty="solid"),
                ArtifactSection(key="target", title="Cible", content="Solo founders et petites equipes early-stage avec un projet SaaS ou digital a cadrer.", certainty="to_confirm"),
            ],
        ),
        ArtifactBlock(
            id=f"{mission_id}:artifact:product", title="Bloc Produit", status="ready_to_decide", certainty="to_confirm",
            summary="Le MVP de demarrage devient concret et demonstratif.",
            content="La boucle prioritaire retenue est mission -> question -> reponse -> artefact -> dossier. Les extensions comme PDF, partage et retrieval documentaire restent hors tranche.",
            sections=[
                ArtifactSection(key="scope", title="Scope MVP", content="Flow Demarrage resserre : intake libre, question utile, reprise, dossier markdown.", certainty="to_confirm"),
                ArtifactSection(key="features", title="Fonctionnalites cles", content="Projet, mission, question, artefacts, dossier. Upload fichier en V1 simple.", certainty="to_confirm"),
                ArtifactSection(key="out_of_scope", title="Hors tranche", content="PDF, share links, retrieval documentaire, multi-flow, auth production.", certainty="solid"),
            ],
        ),
        ArtifactBlock(
            id=f"{mission_id}:artifact:requirements", title="Bloc Exigences", status="in_progress", certainty="to_confirm",
            summary="Les exigences V1 deviennent plus concretes, mais pas encore totalement fermees.",
            content="Les exigences de base convergent vers une auth serveur credible, un runtime reprenable, une persistence canonique et un dossier markdown lisible.",
            sections=[
                ArtifactSection(key="functional", title="Exigences fonctionnelles", content="Auth serveur minimale, cycle waiting_user -> resume stable, persistence canonique, dossier markdown.", certainty="to_confirm"),
                ArtifactSection(key="non_functional", title="Exigences non fonctionnelles", content="Latence acceptable, runtime reprenable, donnees exportables, pas de lock-in.", certainty="to_confirm"),
                ArtifactSection(key="risks", title="Risques identifies", content="Qualite du cadrage si peu de contexte, contenu generique des agents, adoption utilisateur.", certainty="unknown"),
            ],
        ),
    ]
