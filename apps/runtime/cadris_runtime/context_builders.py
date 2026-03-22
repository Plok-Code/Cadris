"""Context builder helpers for agent prompts.

Pure functions that assemble context strings from MissionMemory
for injection into agent and critic prompts. Extracted from
agent_runner.py to keep each module under 400 lines.
"""

from __future__ import annotations

from .agent_specs import AgentSpec
from .memory import MissionMemory


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


# ── Context builders ──────────────────────────────────────────


def _build_context(spec: AgentSpec, memory: MissionMemory) -> str:
    """Build the context string an agent sees from other agents' work.

    Context chars per doc are aligned with prompt targets:
    - free plan: 1500 chars (~250 words) — prompts target 300-500 words
    - paid plans: 2500 chars (~400 words) — prompts target 600-1200 words
    """
    max_chars = 1500 if memory.plan == "free" else 2500

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


def _build_file_map_context() -> str:
    """Build an explicit file path reference for the consolidation agent.

    This prevents Llama (and any model) from hallucinating file paths
    in implementation_plan and user_guide documents.
    Paths are relative to the project root (after unzipping).
    """
    lines = [
        "## REFERENCE OBLIGATOIRE -- Chemins de fichiers a la racine du projet",
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
    lines.append("NE JAMAIS dire 'dans le zip' -- les fichiers sont a la racine du projet.")
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
            "- **Structure** : Markdown -- titres (##, ###), tableaux, listes.\n"
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
        "- **Structure** : Markdown riche -- titres (##, ###), tableaux, listes. "
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
