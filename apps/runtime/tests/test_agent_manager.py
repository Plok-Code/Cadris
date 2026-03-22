"""Tests for agent_manager.py — wave orchestration, fallback, events.

These tests mock the LLM calls (run_agent) to test the orchestration
logic independently of any external API. This is the core mission
execution engine and must be tested thoroughly.
"""
from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cadris_runtime.agent_manager import (
    get_wave_doc_ids,
    get_wave_for_doc,
    run_wave,
    run_single_wave_cycle,
    run_consolidation_wave,
)
from cadris_runtime.agent_runner import AgentResult
from cadris_runtime.agent_specs import AGENT_SPECS, CriticOutput, get_specs_by_wave
from cadris_runtime.event_emitter import EventEmitter
from cadris_runtime.memory import DocumentDraft, MissionMemory


# ── Helpers ───────────────────────────────────────────────


def _make_memory(plan: str = "free") -> MissionMemory:
    return MissionMemory(
        mission_id="test_mission",
        intake_text="Build a SaaS for project management",
        plan=plan,
    )


def _make_agent_result(spec) -> AgentResult:
    """Build a successful AgentResult with placeholder docs for a spec."""
    docs = [
        DocumentDraft(
            doc_id=ds.doc_id,
            title=ds.title,
            agent_code=spec.code,
            content=f"# {ds.title}\n\nContent for {ds.doc_id}.",
            certainty="solid",
        )
        for ds in spec.doc_specs
    ]
    return AgentResult(
        documents=docs,
        model="test-model",
        provider="test",
        prompt_sent="test prompt",
        attempt=1,
        elapsed_ms=100,
    )


def _make_critic_output() -> CriticOutput:
    return CriticOutput(
        overall_quality="good",
        reviews=[],
        questions_for_user=["Quelle est votre cible principale ?"],
        synthesis="Documents de bonne qualite.",
    )


# ── Wave doc mapping ──────────────────────────────────────


class TestWaveDocMapping:
    def test_get_wave_doc_ids_wave1(self):
        doc_ids = get_wave_doc_ids(1)
        assert "vision_produit" in doc_ids
        assert "problem_statement" in doc_ids
        assert len(doc_ids) == 4  # strategy agent produces 4 docs

    def test_get_wave_doc_ids_wave2(self):
        doc_ids = get_wave_doc_ids(2)
        # Wave 2: business(3) + product_core(3) + product_specs(2) = 8 docs
        assert "business_model" in doc_ids
        assert "scope_document" in doc_ids
        assert "user_stories" in doc_ids
        assert len(doc_ids) == 8

    def test_get_wave_doc_ids_empty_wave(self):
        doc_ids = get_wave_doc_ids(99)
        assert doc_ids == []

    def test_get_wave_for_doc_known(self):
        assert get_wave_for_doc("vision_produit") == 1
        assert get_wave_for_doc("business_model") == 2
        assert get_wave_for_doc("architecture") == 3
        assert get_wave_for_doc("executive_summary") == 4

    def test_get_wave_for_doc_unknown(self):
        assert get_wave_for_doc("nonexistent_doc") is None


# ── Wave execution ────────────────────────────────────────


@pytest.mark.asyncio
class TestRunWave:
    @patch("cadris_runtime.agent_manager.run_agent")
    @patch("cadris_runtime.agent_manager.asyncio.sleep", new_callable=AsyncMock)
    async def test_wave1_runs_strategy_agent(self, mock_sleep, mock_run_agent):
        """Wave 1 should run the strategy agent and produce 4 docs."""
        memory = _make_memory()
        emitter = EventEmitter()

        waves = get_specs_by_wave()
        strategy_spec = waves[1][0]
        mock_run_agent.return_value = _make_agent_result(strategy_spec)

        # Consume events in background
        events = []
        async def consume():
            async for e in emitter:
                events.append(e)

        task = asyncio.create_task(consume())
        await run_wave(1, memory, emitter)
        await emitter.close()
        await task

        assert mock_run_agent.call_count == 1
        assert len(memory.documents) == 4
        assert "vision_produit" in memory.documents
        # Wave 1 starts immediately (no inter-wave cooldown)
        mock_sleep.assert_not_called()

    @patch("cadris_runtime.agent_manager.run_agent")
    @patch("cadris_runtime.agent_manager.asyncio.sleep", new_callable=AsyncMock)
    async def test_wave2_has_inter_wave_cooldown(self, mock_sleep, mock_run_agent):
        """Waves > 1 should have inter-wave cooldown."""
        memory = _make_memory()
        emitter = EventEmitter()

        waves = get_specs_by_wave()
        for spec in waves[2]:
            mock_run_agent.return_value = _make_agent_result(spec)

        task = asyncio.create_task(self._consume(emitter))
        await run_wave(2, memory, emitter)
        await emitter.close()
        await task

        # Inter-wave cooldown before wave 2
        assert any(call.args[0] >= 10 for call in mock_sleep.call_args_list)

    @patch("cadris_runtime.agent_manager.run_agent")
    @patch("cadris_runtime.agent_manager.asyncio.sleep", new_callable=AsyncMock)
    async def test_agent_failure_injects_fallback_docs(self, mock_sleep, mock_run_agent):
        """If run_agent raises, fallback placeholder docs must be injected."""
        memory = _make_memory()
        emitter = EventEmitter()

        mock_run_agent.side_effect = RuntimeError("LLM provider down")

        task = asyncio.create_task(self._consume(emitter))
        await run_wave(1, memory, emitter)
        await emitter.close()
        await task

        # Fallback docs should exist for all 4 strategy docs
        assert len(memory.documents) == 4
        for doc in memory.documents.values():
            assert doc.certainty == "to_confirm"
            assert "pas pu etre genere" in doc.content

    @patch("cadris_runtime.agent_manager.run_agent")
    @patch("cadris_runtime.agent_manager.asyncio.sleep", new_callable=AsyncMock)
    async def test_empty_wave_is_noop(self, mock_sleep, mock_run_agent):
        """Running a non-existent wave should do nothing."""
        memory = _make_memory()
        emitter = EventEmitter()

        task = asyncio.create_task(self._consume(emitter))
        await run_wave(99, memory, emitter)
        await emitter.close()
        await task

        mock_run_agent.assert_not_called()
        assert len(memory.documents) == 0

    @staticmethod
    async def _consume(emitter):
        async for _ in emitter:
            pass


# ── Wave cycle (wave + critic) ────────────────────────────


@pytest.mark.asyncio
class TestRunSingleWaveCycle:
    @patch("cadris_runtime.agent_manager.run_critic")
    @patch("cadris_runtime.agent_manager.run_agent")
    @patch("cadris_runtime.agent_manager.asyncio.sleep", new_callable=AsyncMock)
    async def test_free_plan_skips_critic(self, mock_sleep, mock_run_agent, mock_critic):
        """Free plan should skip critic to save cost."""
        memory = _make_memory("free")
        emitter = EventEmitter()

        waves = get_specs_by_wave()
        strategy_spec = waves[1][0]
        mock_run_agent.return_value = _make_agent_result(strategy_spec)

        task = asyncio.create_task(self._consume(emitter))
        critic_output = await run_single_wave_cycle(1, memory, emitter)
        await emitter.close()
        await task

        mock_critic.assert_not_called()
        assert critic_output.overall_quality == "good"
        assert memory.iteration == 1
        assert memory.current_wave == 1

    @patch("cadris_runtime.agent_manager.run_critic")
    @patch("cadris_runtime.agent_manager.run_agent")
    @patch("cadris_runtime.agent_manager.asyncio.sleep", new_callable=AsyncMock)
    async def test_paid_plan_runs_critic(self, mock_sleep, mock_run_agent, mock_critic):
        """Paid plans should run the critic after wave agents."""
        memory = _make_memory("pro")
        emitter = EventEmitter()

        waves = get_specs_by_wave()
        strategy_spec = waves[1][0]
        mock_run_agent.return_value = _make_agent_result(strategy_spec)
        mock_critic.return_value = _make_critic_output()

        task = asyncio.create_task(self._consume(emitter))
        critic_output = await run_single_wave_cycle(1, memory, emitter)
        await emitter.close()
        await task

        mock_critic.assert_called_once()
        assert critic_output.overall_quality == "good"

    @staticmethod
    async def _consume(emitter):
        async for _ in emitter:
            pass


# ── Consolidation wave ────────────────────────────────────


@pytest.mark.asyncio
class TestRunConsolidationWave:
    @patch("cadris_runtime.agent_manager.run_agent")
    @patch("cadris_runtime.agent_manager.asyncio.sleep", new_callable=AsyncMock)
    async def test_consolidation_produces_4_docs(self, mock_sleep, mock_run_agent):
        """Consolidation wave should produce executive_summary, dossier_consolide, implementation_plan, user_guide."""
        memory = _make_memory()
        emitter = EventEmitter()

        waves = get_specs_by_wave()
        consolidation_spec = waves[max(waves.keys())][0]
        mock_run_agent.return_value = _make_agent_result(consolidation_spec)

        events = []
        async def consume():
            async for e in emitter:
                events.append(e)

        task = asyncio.create_task(consume())
        await run_consolidation_wave(memory, emitter)
        await emitter.close()
        await task

        assert "executive_summary" in memory.documents
        assert "implementation_plan" in memory.documents
        assert "user_guide" in memory.documents

        # Should emit MISSION_COMPLETED event
        event_types = [e.type.value for e in events]
        assert "mission_completed" in event_types

    @staticmethod
    async def _consume(emitter):
        async for _ in emitter:
            pass
