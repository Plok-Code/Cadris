"""Model configuration per agent and per pricing plan.

Each plan maps to a set of models and a provider:
- free    : Llama 3.3 70B via Together AI (cheap, no OpenAI dependency)
- starter : GPT-4.1 via OpenAI
- pro     : Claude Opus (strategy+critic) + GPT-4.1 (others) + Perplexity Sonar (business)
- expert  : Claude Opus everywhere + Perplexity DeepSearch

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

_PLAN_MODELS: dict[str, dict[str, ModelChoice]] = {
    "free": {
        "default": ModelChoice("meta-llama/Llama-3.3-70B-Instruct-Turbo", "together"),
    },
    "starter": {
        "default": ModelChoice("gpt-4.1", "openai"),
    },
    "pro": {
        "default": ModelChoice("gpt-4.1", "openai"),
        "strategy": ModelChoice("gpt-4.1", "openai"),  # Opus when available
        "critic": ModelChoice("gpt-4.1", "openai"),     # Opus when available
        # "business": Perplexity Sonar — handled at agent level
    },
    "expert": {
        "default": ModelChoice("gpt-4.1", "openai"),  # Opus when available
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
