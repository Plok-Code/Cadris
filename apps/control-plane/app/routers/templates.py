"""Dossier templates router."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from ..auth import AuthenticatedUser, require_user
from ..errors import AppError

router = APIRouter(prefix="/api/dossier-templates", tags=["templates"])

DOSSIER_TEMPLATES = {
    "standard": {
        "id": "standard",
        "name": "Standard",
        "description": "Cadrage complet avec les 22 sections par defaut.",
        "sections": None,
    },
    "startup_pitch": {
        "id": "startup_pitch",
        "name": "Startup Pitch",
        "description": "Deck oriente investisseurs : vision, marche, business model, MVP.",
        "sections": [
            "vision_produit", "problem_statement", "icp_personas", "value_proposition",
            "market_analysis", "business_model", "pricing_strategy",
            "mvp_definition", "architecture", "executive_summary",
        ],
    },
    "internal_project": {
        "id": "internal_project",
        "name": "Projet interne",
        "description": "Dossier pour un projet interne d'entreprise : specs, tech, planning.",
        "sections": [
            "vision_produit", "problem_statement", "scope_document",
            "prd", "user_stories", "feature_specs",
            "architecture", "tech_stack", "data_model", "api_spec",
            "implementation_plan", "executive_summary",
        ],
    },
    "rfp_response": {
        "id": "rfp_response",
        "name": "Appel d'offres",
        "description": "Reponse structuree a un appel d'offres ou cahier des charges.",
        "sections": [
            "vision_produit", "problem_statement", "value_proposition",
            "scope_document", "mvp_definition", "prd",
            "architecture", "tech_stack", "nfr_security",
            "ux_principles", "design_system",
            "dossier_consolide", "executive_summary",
        ],
    },
    "business_plan": {
        "id": "business_plan",
        "name": "Business Plan",
        "description": "Plan d'affaires complet : marche, financier, strategie, operations.",
        "sections": [
            "vision_produit", "problem_statement", "icp_personas", "value_proposition",
            "market_analysis", "business_model", "pricing_strategy",
            "scope_document", "mvp_definition",
            "architecture", "tech_stack",
            "implementation_plan", "executive_summary", "dossier_consolide",
        ],
    },
}


@router.get("")
async def list_dossier_templates(user: AuthenticatedUser = Depends(require_user)):
    """List available dossier templates."""
    return {"templates": list(DOSSIER_TEMPLATES.values())}


@router.get("/{template_id}")
async def get_dossier_template(
    template_id: str,
    user: AuthenticatedUser = Depends(require_user),
):
    """Get a specific dossier template."""
    template = DOSSIER_TEMPLATES.get(template_id)
    if not template:
        raise AppError.not_found("template_not_found", "Template non trouve.")
    return template
