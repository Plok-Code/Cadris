"""Model configuration per agent and per pricing plan.

BETA PHASE — UNIFIED MODEL (deliberate product decision):
Every plan currently runs on the FREE model (Llama 3.3 70B via Together AI).
The paid plans keep their richer ORCHESTRATION (critic pass, deeper document
targets, web research) but use the same model as free, so we can measure
whether the orchestration alone moves quality before paying for a stronger
model. Once that comparison is done, restore per-plan models (and wire an
Anthropic/Opus provider for pro/expert) — the original mapping is preserved
in the comments below for a one-line revert.

NOTE: the billing/pricing page advertises stronger models for paid plans; that
promise is intentionally on hold during this beta. Align the copy or restore
the models before charging for "bigger model" tiers.

Dev profile overrides everything to gpt-4.1-nano for fast iteration.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .config import settings

Provider = Literal["openai", "together"]


@dataclass(frozen=True)
class ModelChoice:
    """Model + provider pair resolved for a specific agent call."""
    model: str
    provider: Provider


# ── Plan-based model mapping ──────────────────────────────────

# Key: (plan, agent_code) → ModelChoice
# Falls back to (plan, "default") if agent_code not found.

# The single free model every plan uses during the unified-model beta.
_FREE_MODEL = ModelChoice("meta-llama/Llama-3.3-70B-Instruct-Turbo", "together")

_PLAN_MODELS: dict[str, dict[str, ModelChoice]] = {
    # BETA: all plans share the free model. To restore per-plan models, swap the
    # paid "default" values back to the commented originals below.
    "free": {
        "default": _FREE_MODEL,
    },
    "starter": {
        "default": _FREE_MODEL,  # restore: ModelChoice("gpt-4.1", "openai")
    },
    "pro": {
        "default": _FREE_MODEL,  # restore: ModelChoice("gpt-4.1", "openai")
        # restore: "strategy"/"critic" → Opus when an Anthropic provider exists.
        # "business": Perplexity Sonar — handled at agent level
    },
    "expert": {
        "default": _FREE_MODEL,  # restore: gpt-4.1 / Opus everywhere
        # "business": Perplexity DeepSearch — handled at agent level
    },
}

# Dev override: everything uses nano regardless of plan
_DEV_CHOICE = ModelChoice("gpt-4.1-nano", "openai")


def get_model_for_agent(agent_code: str, plan: str = "free") -> ModelChoice:
    """Return the model+provider for a given agent and plan.

    In dev profile, always returns gpt-4.1-nano on OpenAI.
    """
    if settings.model_profile == "dev":
        return _DEV_CHOICE

    plan_map = _PLAN_MODELS.get(plan, _PLAN_MODELS["free"])
    return plan_map.get(agent_code, plan_map["default"])
