"""Agent specifications for the collaborative engine.

Each AgentSpec defines:
- identity (code, label, role)
- what documents it produces (doc_specs)
- what documents it reads from other agents (reads_from)
- execution wave (lower waves run first)
- prompt key (maps to packages/prompts/agents/<code>_agent.md)

The roster is intentionally small for v1 (8 agents, ~22 documents).
V2 will add Legal, Execution, GTM, Data agents (~55 documents total).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pydantic import BaseModel, Field


# ── Qualification output (pre-wave phase) ──────────────────


class QualificationQuestion(BaseModel):
    question: str = Field(description="Question ouverte en texte libre pour l'utilisateur.")
    context: str = Field(description="Pourquoi cette question est importante pour le cadrage.")


class QualificationOutput(BaseModel):
    questions: list[QualificationQuestion] = Field(description="2-7 questions selon la richesse de la description.")


# ── Structured output models (one per agent) ───────────────


class StrategyOutput(BaseModel):
    vision_produit: str = Field(description="Vision produit, Markdown structure, 600+ mots.")
    problem_statement: str = Field(description="Probleme utilisateur, Markdown structure, 600+ mots.")
    icp_personas: str = Field(description="ICP et 3 personas detaillees, Markdown structure, 800+ mots.")
    value_proposition: str = Field(description="Proposition de valeur, Markdown structure, 600+ mots.")


class ProductCoreOutput(BaseModel):
    """Output for the product_core agent: scope, MVP, PRD."""

    scope_document: str = Field(description="Perimetre produit V1, Markdown structure, 600+ mots.")
    mvp_definition: str = Field(description="Definition MVP, Markdown structure, 600+ mots.")
    prd: str = Field(description="PRD complet, Markdown structure, 1000+ mots.")


class ProductSpecsOutput(BaseModel):
    """Output for the product_specs agent: user stories and feature specs."""

    user_stories: str = Field(description="User stories 15+, Markdown structure, 800+ mots.")
    feature_specs: str = Field(description="Specs fonctionnelles par feature, Markdown structure, 1000+ mots.")


class TechArchOutput(BaseModel):
    """Output for the tech_arch agent: architecture, stack, NFR."""

    architecture: str = Field(description="Architecture technique, Markdown structure, 800+ mots.")
    tech_stack: str = Field(description="Stack technique justifiee, Markdown structure, 800+ mots.")
    nfr_security: str = Field(description="NFR et securite, Markdown structure, 800+ mots.")


class TechDataOutput(BaseModel):
    """Output for the tech_data agent: data model and API spec."""

    data_model: str = Field(description="Modele de donnees, Markdown structure, 800+ mots.")
    api_spec: str = Field(description="Spec API 8-10 endpoints, Markdown structure, 1000+ mots.")


class DesignOutput(BaseModel):
    ux_principles: str = Field(description="Principes UX 5-7, Markdown structure, 800+ mots.")
    information_architecture: str = Field(description="Architecture info et navigation, Markdown structure, 800+ mots.")
    design_system: str = Field(description="Design system tokens et composants, Markdown structure, 800+ mots.")


class BusinessOutput(BaseModel):
    business_model: str = Field(description="Modele economique, Markdown structure, 800+ mots.")
    pricing_strategy: str = Field(description="Strategie pricing, Markdown structure, 800+ mots.")
    market_analysis: str = Field(description="Analyse de marche, Markdown structure, 800+ mots.")


class ConsolidationOutput(BaseModel):
    executive_summary: str = Field(description="Resume executif, Markdown structure, 800+ mots.")
    dossier_consolide: str = Field(description="Dossier consolide complet, Markdown structure, 2000+ mots.")
    implementation_plan: str = Field(description="Plan implementation step-by-step pour Claude Code, Markdown, 1000+ mots.")
    user_guide: str = Field(description="Guide utilisateur pour piloter la realisation, Markdown, 1000+ mots.")


# ── Critic output (Phase 2) ───────────────────────────────


class CriticReviewItem(BaseModel):
    """Evaluation of a single document by the critic agent."""

    doc_id: str = Field(description="Identifiant du document evalue.")
    quality: str = Field(description="solid | needs_work | insufficient.")
    comment: str = Field(description="Commentaire constructif 3-5 phrases.")


class CriticOutput(BaseModel):
    """Structured output of the critic agent after reviewing a wave."""

    overall_quality: str = Field(description="excellent | good | needs_work | insufficient.")
    reviews: list[CriticReviewItem] = Field(description="Evaluation par document.")
    questions_for_user: list[str] = Field(description="2-5 questions ciblees pour l'utilisateur.")
    synthesis: str = Field(description="Synthese 5-8 phrases sur la qualite de la vague.")


# ── Document spec ──────────────────────────────────────────


@dataclass(frozen=True)
class DocSpec:
    """Definition of a single document an agent must produce."""

    doc_id: str
    title: str


# ── Agent spec ─────────────────────────────────────────────


@dataclass(frozen=True)
class AgentSpec:
    """Full specification of a collaborative agent."""

    code: str
    label: str
    role: str
    wave: int
    prompt_key: str  # maps to packages/prompts/agents/{prompt_key}.md
    doc_specs: tuple[DocSpec, ...] = field(default_factory=tuple)
    reads_from: tuple[str, ...] = field(default_factory=tuple)  # agent codes it reads
    output_model: type[BaseModel] | None = None


# ── Roster v1 ──────────────────────────────────────────────

AGENT_SPECS: list[AgentSpec] = [
    AgentSpec(
        code="strategy",
        label="Agent Strategie",
        role="Clarifie la vision, le probleme, la cible et la proposition de valeur.",
        wave=1,
        prompt_key="strategy_agent",
        doc_specs=(
            DocSpec("vision_produit", "Vision produit"),
            DocSpec("problem_statement", "Probleme utilisateur"),
            DocSpec("icp_personas", "ICP & Personas"),
            DocSpec("value_proposition", "Proposition de valeur"),
        ),
        reads_from=(),  # wave 1 — reads only intake
        output_model=StrategyOutput,
    ),
    AgentSpec(
        code="business",
        label="Agent Business",
        role="Definit le modele economique, le pricing et l'analyse de marche.",
        wave=2,
        prompt_key="business_agent",
        doc_specs=(
            DocSpec("business_model", "Modele economique"),
            DocSpec("pricing_strategy", "Strategie de pricing"),
            DocSpec("market_analysis", "Analyse de marche"),
        ),
        reads_from=("strategy",),
        output_model=BusinessOutput,
    ),
    AgentSpec(
        code="product_core",
        label="Agent Produit (Cadrage)",
        role="Definit le perimetre, le MVP et le PRD du produit.",
        wave=2,
        prompt_key="product_agent",  # same prompt, subset of docs
        doc_specs=(
            DocSpec("scope_document", "Perimetre du produit"),
            DocSpec("mvp_definition", "Definition MVP"),
            DocSpec("prd", "PRD"),
        ),
        reads_from=("strategy",),
        output_model=ProductCoreOutput,
    ),
    AgentSpec(
        code="product_specs",
        label="Agent Produit (Specs)",
        role="Redige les user stories et les specifications fonctionnelles.",
        wave=2,
        prompt_key="product_agent",  # same prompt, subset of docs
        doc_specs=(
            DocSpec("user_stories", "User Stories"),
            DocSpec("feature_specs", "Specifications fonctionnelles"),
        ),
        reads_from=("strategy",),
        output_model=ProductSpecsOutput,
    ),
    AgentSpec(
        code="tech_arch",
        label="Agent Tech (Architecture)",
        role="Definit l'architecture, le stack technique et les exigences non-fonctionnelles.",
        wave=3,
        prompt_key="tech_agent",  # same prompt, subset of docs
        doc_specs=(
            DocSpec("architecture", "Architecture technique"),
            DocSpec("tech_stack", "Stack technique"),
            DocSpec("nfr_security", "Exigences non-fonctionnelles"),
        ),
        reads_from=("strategy", "product_core", "product_specs"),
        output_model=TechArchOutput,
    ),
    AgentSpec(
        code="tech_data",
        label="Agent Tech (Donnees & API)",
        role="Definit le modele de donnees et la specification API.",
        wave=3,
        prompt_key="tech_agent",  # same prompt, subset of docs
        doc_specs=(
            DocSpec("data_model", "Modele de donnees"),
            DocSpec("api_spec", "Specification API"),
        ),
        reads_from=("strategy", "product_core", "product_specs"),
        output_model=TechDataOutput,
    ),
    AgentSpec(
        code="design",
        label="Agent Design",
        role="Definit les principes UX, l'architecture de l'information et le design system.",
        wave=3,
        prompt_key="design_agent",
        doc_specs=(
            DocSpec("ux_principles", "Principes UX"),
            DocSpec("information_architecture", "Architecture de l'information"),
            DocSpec("design_system", "Design System"),
        ),
        reads_from=("strategy", "product_core", "product_specs"),
        output_model=DesignOutput,
    ),
    AgentSpec(
        code="consolidation",
        label="Agent Consolidation",
        role="Synthetise tous les travaux en un dossier final coherent.",
        wave=4,
        prompt_key="consolidation_agent",
        doc_specs=(
            DocSpec("executive_summary", "Resume executif"),
            DocSpec("dossier_consolide", "Dossier consolide"),
            DocSpec("implementation_plan", "Plan d'implementation"),
            DocSpec("user_guide", "Guide utilisateur"),
        ),
        reads_from=("strategy", "business", "product_core", "product_specs", "tech_arch", "tech_data", "design"),
        output_model=ConsolidationOutput,
    ),
]


def get_specs_by_wave() -> dict[int, list[AgentSpec]]:
    """Return agent specs grouped by wave number, ordered."""
    waves: dict[int, list[AgentSpec]] = {}
    for spec in AGENT_SPECS:
        waves.setdefault(spec.wave, []).append(spec)
    return dict(sorted(waves.items()))


def get_spec_by_code(code: str) -> AgentSpec | None:
    """Find an agent spec by its code."""
    for spec in AGENT_SPECS:
        if spec.code == code:
            return spec
    return None


# ── Critic agent (special — not in AGENT_SPECS) ──────────────

CRITIC_SPEC = AgentSpec(
    code="critic",
    label="Agent Critique",
    role="Evalue la qualite des documents produits, identifie les lacunes et genere des questions ciblees.",
    wave=0,  # sentinel: never auto-scheduled in the wave loop
    prompt_key="critic_agent",
    doc_specs=(),  # critic produces no documents
    reads_from=(),  # reads ALL documents (handled specially in agent_manager)
    output_model=CriticOutput,
)
