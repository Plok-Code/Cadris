"""Certainty-entry and dossier-section builders (used by resume responses)."""

from __future__ import annotations

from ..models import CertaintyEntry, DossierSection
from .artifacts import summarize_sentence

__all__ = ["_build_certainty_entries", "_build_dossier_sections"]


def _build_certainty_entries(mission_id, cycle, source_digest, final=False):
    entries = [
        CertaintyEntry(
            id=f"{mission_id}:cert:problem", title="Probleme principal",
            status="solid" if final else ("to_confirm" if cycle >= 2 else "unknown"),
            impact="Definit la raison d'etre du produit", source_label="Reponses utilisateur",
        ),
        CertaintyEntry(
            id=f"{mission_id}:cert:target", title="Utilisateur cible",
            status="solid" if final else ("to_confirm" if cycle >= 2 else "unknown"),
            impact="Determine le cadrage produit et UX", source_label="Reponses utilisateur",
        ),
        CertaintyEntry(
            id=f"{mission_id}:cert:mvp_scope", title="Scope MVP",
            status="to_confirm" if final else "unknown",
            impact="Fixe le perimetre de la V1", source_label="Agent produit",
        ),
        CertaintyEntry(
            id=f"{mission_id}:cert:value_loop", title="Boucle de valeur",
            status="to_confirm" if final else ("unknown" if cycle < 2 else "to_confirm"),
            impact="Determine la preuve de valeur minimale", source_label="Agent strategie",
        ),
        CertaintyEntry(
            id=f"{mission_id}:cert:nfr", title="Exigences non fonctionnelles",
            status="to_confirm" if final else "blocking",
            impact="Contraintes techniques et qualite", source_label="Agent exigences",
        ),
    ]
    if source_digest:
        entries.append(CertaintyEntry(
            id=f"{mission_id}:cert:sources", title="Sources jointes",
            status="to_confirm", impact="Enrichissent le cadrage avec des preuves externes",
            source_label="Documents utilisateur",
        ))
    return entries


def _build_dossier_sections(context, accumulated_context, source_section, source_digest):
    sections = [
        DossierSection(
            id="vision", title="Vision produit", certainty="solid",
            content="Cadris doit exister pour donner un cadre de travail serieux aux createurs de projets, sans les forcer a porter seuls la charge de cadrage inter-metier.",
        ),
        DossierSection(
            id="problem", title="Probleme utilisateur", certainty="solid",
            content=summarize_sentence(accumulated_context),
        ),
        DossierSection(
            id="target", title="Utilisateur cible", certainty="to_confirm",
            content="Solo founders et petites equipes early-stage avec un projet SaaS ou digital a cadrer. Capables de travailler avec l'IA mais soucieux de ne pas laisser les modeles improviser la logique projet.",
        ),
    ]
    if source_section:
        sections.append(DossierSection(
            id="sources", title="Sources jointes", content=source_section, certainty="to_confirm",
        ))
    sections.extend([
        DossierSection(
            id="mvp", title="Boucle MVP retenue", certainty="to_confirm",
            content="La V1 doit prouver la valeur sur le flow Demarrage resserre, avec mission durable, question utile, reprise et dossier markdown.",
        ),
        DossierSection(
            id="requirements", title="Exigences V1", certainty="to_confirm",
            content="La V1 doit garantir une auth serveur minimale, un cycle waiting_user -> resume stable, une persistence canonique lisible et un dossier markdown transmissible.",
        ),
        DossierSection(
            id="risks", title="Risques identifies", certainty="unknown",
            content="Les principaux risques portent sur la qualite du cadrage si l'utilisateur fournit peu de contexte, et sur la capacite des agents a produire du contenu non generique.",
        ),
    ])
    return sections
