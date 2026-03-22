"""Tests for model_config.py — plan-based model selection."""
from __future__ import annotations

import pytest
from unittest.mock import patch

from cadris_runtime.model_config import ModelChoice, get_model_for_agent


@pytest.fixture(autouse=True)
def _prod_profile():
    """Force prod profile so plan-based routing is tested (dev overrides all)."""
    with patch("cadris_runtime.model_config.settings") as mock_settings:
        mock_settings.model_profile = "prod"
        yield mock_settings


class TestGetModelForAgent:
    """Verify plan→model routing produces correct choices."""

    def test_free_plan_uses_together(self):
        choice = get_model_for_agent("strategy", "free")
        assert choice.provider == "together"
        assert "Llama" in choice.model or "llama" in choice.model

    def test_starter_plan_uses_openai(self):
        choice = get_model_for_agent("strategy", "starter")
        assert choice.provider == "openai"

    def test_unknown_plan_falls_back_to_free(self):
        choice = get_model_for_agent("strategy", "nonexistent_plan")
        assert choice.provider == "together"

    def test_unknown_agent_uses_plan_default(self):
        choice = get_model_for_agent("nonexistent_agent", "starter")
        default = get_model_for_agent("default", "starter")
        assert choice.model == default.model

    def test_dev_profile_overrides_everything(self, _prod_profile):
        _prod_profile.model_profile = "dev"
        choice = get_model_for_agent("strategy", "expert")
        assert choice.model == "gpt-4.1-nano"
        assert choice.provider == "openai"

    def test_all_plans_return_model_choice(self):
        """Every valid plan must return a ModelChoice, never raise."""
        for plan in ("free", "starter", "pro", "expert"):
            for agent in ("strategy", "business", "product_core", "tech_arch", "consolidation", "critic"):
                choice = get_model_for_agent(agent, plan)
                assert isinstance(choice, ModelChoice)
                assert choice.model
                assert choice.provider in ("openai", "together")
