"""Tests for collaborative_engine.py — mission state machine.

Tests the full mission lifecycle: start → qualification → wave cycles → consolidation.
All LLM calls are mocked; we test the orchestration logic, state transitions,
and memory persistence.
"""
from __future__ import annotations

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from cadris_runtime.agent_specs import CriticOutput, QualificationOutput, QualificationQuestion
from cadris_runtime.collaborative_engine import CollaborativeEngine, _run_qualification
from cadris_runtime.event_emitter import EventEmitter
from cadris_runtime.event_types import EventType
from cadris_runtime.memory import DocumentDraft, MissionMemory
from cadris_runtime.models import RuntimeResumeRequest, RuntimeStartRequest


# ── Helpers ───────────────────────────────────────────────


def _start_payload(mission_id: str = "test_m1", plan: str = "free") -> RuntimeStartRequest:
    return RuntimeStartRequest(
        mission_id=mission_id,
        project_name="Test Project",
        intake_text="Build a SaaS for project management with AI features",
        flow_code="demarrage",
        plan=plan,
        supporting_inputs=[],
    )


def _resume_payload(
    mission_id: str = "test_m1",
    action: str = "next_wave",
    answer_text: str = "",
    plan: str = "free",
) -> RuntimeResumeRequest:
    return RuntimeResumeRequest(
        mission_id=mission_id,
        project_name="Test Project",
        intake_text="Build a SaaS for project management with AI features",
        answer_text=answer_text,
        flow_code="demarrage",
        plan=plan,
        action=action,
    )


def _mock_qualification_output() -> QualificationOutput:
    return QualificationOutput(
        questions=[
            QualificationQuestion(question="Qui est votre cible ?", context="Pour le persona"),
            QualificationQuestion(question="Quel est le budget ?", context="Pour le pricing"),
        ]
    )


async def _collect_events(emitter: EventEmitter) -> list:
    events = []
    async for e in emitter:
        events.append(e)
    return events


# ── Qualification phase ───────────────────────────────────


@pytest.mark.asyncio
class TestQualification:
    @patch("cadris_runtime.agent_runner._get_run_config")
    @patch("agents.Runner")
    @patch("agents.Agent")
    async def test_qualification_emits_questions(self, mock_agent_cls, mock_runner, mock_config):
        """Qualification phase should emit QUALIFICATION_QUESTIONS event."""
        memory = MissionMemory(mission_id="q_test", intake_text="SaaS project", plan="free")
        emitter = EventEmitter()

        # Mock the streamed runner
        mock_streamed = MagicMock()
        mock_streamed.stream_events = MagicMock(return_value=AsyncIteratorMock([]))
        mock_streamed.final_output_as = MagicMock(return_value=_mock_qualification_output())
        mock_runner.run_streamed = MagicMock(return_value=mock_streamed)

        task = asyncio.create_task(_collect_events(emitter))
        await _run_qualification(memory, emitter)
        await emitter.close()
        events = await task

        assert len(memory.qualification_questions) == 2
        event_types = [e.type for e in events]
        assert EventType.QUALIFICATION_QUESTIONS in event_types

    @patch("cadris_runtime.agent_runner._get_run_config")
    @patch("agents.Runner")
    @patch("agents.Agent")
    async def test_qualification_failure_emits_fallback(self, mock_agent_cls, mock_runner, mock_config):
        """If qualification LLM fails, a fallback question must be emitted."""
        memory = MissionMemory(mission_id="q_fail", intake_text="SaaS", plan="free")
        emitter = EventEmitter()

        mock_runner.run_streamed = MagicMock(side_effect=RuntimeError("LLM down"))

        task = asyncio.create_task(_collect_events(emitter))
        await _run_qualification(memory, emitter)
        await emitter.close()
        events = await task

        # Should still have a fallback question
        assert len(memory.qualification_questions) == 1
        assert "projet" in memory.qualification_questions[0]["question"].lower()

        # Should emit ERROR + fallback QUALIFICATION_QUESTIONS
        event_types = [e.type for e in events]
        assert EventType.ERROR in event_types
        assert EventType.QUALIFICATION_QUESTIONS in event_types


# ── Engine start ──────────────────────────────────────────


@pytest.mark.asyncio
class TestEngineStart:
    @patch("cadris_runtime.collaborative_engine.mission_store")
    @patch("cadris_runtime.collaborative_engine._run_qualification")
    async def test_start_creates_memory_and_persists(self, mock_qual, mock_store):
        """start_mission_stream should create memory and persist it."""
        engine = CollaborativeEngine()
        emitter = EventEmitter()
        payload = _start_payload()

        mock_qual.return_value = None
        mock_store.aput = AsyncMock()

        task = asyncio.create_task(_collect_events(emitter))
        memory = await engine.start_mission_stream(payload, emitter)
        await emitter.close()
        await task

        assert memory.mission_id == "test_m1"
        assert memory.plan == "free"
        mock_store.aput.assert_called_once()
        mock_qual.assert_called_once()


# ── Engine resume ─────────────────────────────────────────


@pytest.mark.asyncio
class TestEngineResume:
    @patch("cadris_runtime.collaborative_engine.mission_store")
    @patch("cadris_runtime.collaborative_engine.run_single_wave_cycle")
    async def test_answer_qualification_starts_wave1(self, mock_wave_cycle, mock_store):
        """Answering qualification should trigger wave 1."""
        engine = CollaborativeEngine()
        emitter = EventEmitter()

        # Pre-populate memory in store
        memory = MissionMemory(mission_id="test_m1", intake_text="SaaS", plan="free")
        mock_store.aget = AsyncMock(return_value=memory)
        mock_store.aput = AsyncMock()
        mock_wave_cycle.return_value = CriticOutput(
            overall_quality="good", reviews=[], questions_for_user=[], synthesis="OK"
        )

        payload = _resume_payload(
            action="answer_qualification",
            answer_text=json.dumps({"Q1": "Startups"}),
        )

        task = asyncio.create_task(_collect_events(emitter))
        result = await engine.resume_mission_stream(payload, emitter)
        await emitter.close()
        await task

        mock_wave_cycle.assert_called_once_with(wave_num=1, memory=memory, event_emitter=emitter)
        assert memory.qualification_answers == {"Q1": "Startups"}

    @patch("cadris_runtime.collaborative_engine.mission_store")
    @patch("cadris_runtime.collaborative_engine.run_single_wave_cycle")
    async def test_next_wave_advances(self, mock_wave_cycle, mock_store):
        """action=next_wave should advance to the next wave."""
        engine = CollaborativeEngine()
        emitter = EventEmitter()

        memory = MissionMemory(mission_id="test_m1", intake_text="SaaS", plan="free")
        memory.current_wave = 1
        mock_store.aget = AsyncMock(return_value=memory)
        mock_store.aput = AsyncMock()
        mock_wave_cycle.return_value = CriticOutput(
            overall_quality="good", reviews=[], questions_for_user=[], synthesis="OK"
        )

        payload = _resume_payload(action="next_wave")

        task = asyncio.create_task(_collect_events(emitter))
        await engine.resume_mission_stream(payload, emitter)
        await emitter.close()
        await task

        # Wave 1 validated, should run wave 2
        assert 1 in memory.wave_validated
        mock_wave_cycle.assert_called_once_with(wave_num=2, memory=memory, event_emitter=emitter)

    @patch("cadris_runtime.collaborative_engine.mission_store")
    @patch("cadris_runtime.collaborative_engine.run_single_wave_cycle")
    async def test_refine_wave_reruns_current(self, mock_wave_cycle, mock_store):
        """action=refine_wave should re-run the current wave, clearing its docs."""
        engine = CollaborativeEngine()
        emitter = EventEmitter()

        memory = MissionMemory(mission_id="test_m1", intake_text="SaaS", plan="free")
        memory.current_wave = 1
        # Add a doc from wave 1 that should be invalidated
        memory.upsert_document(DocumentDraft(
            doc_id="vision_produit", title="Vision", agent_code="strategy",
            content="Old vision", certainty="solid",
        ))
        mock_store.aget = AsyncMock(return_value=memory)
        mock_store.aput = AsyncMock()
        mock_wave_cycle.return_value = CriticOutput(
            overall_quality="good", reviews=[], questions_for_user=[], synthesis="OK"
        )

        payload = _resume_payload(action="refine_wave", answer_text="Focus on B2B")

        task = asyncio.create_task(_collect_events(emitter))
        await engine.resume_mission_stream(payload, emitter)
        await emitter.close()
        await task

        # Doc should have been invalidated before re-run
        mock_wave_cycle.assert_called_once_with(wave_num=1, memory=memory, event_emitter=emitter)
        assert "Focus on B2B" in memory.user_answers

    @patch("cadris_runtime.collaborative_engine.mission_store")
    @patch("cadris_runtime.collaborative_engine.run_consolidation_wave")
    @patch("cadris_runtime.collaborative_engine.run_single_wave_cycle")
    async def test_last_wave_triggers_consolidation(self, mock_wave_cycle, mock_consolidation, mock_store):
        """When all reviewable waves are done, consolidation should run."""
        engine = CollaborativeEngine()
        emitter = EventEmitter()

        memory = MissionMemory(mission_id="test_m1", intake_text="SaaS", plan="free")
        # Wave 3 is the last reviewable wave (wave 4 = consolidation)
        memory.current_wave = 3
        mock_store.aget = AsyncMock(return_value=memory)
        mock_store.aput = AsyncMock()
        mock_consolidation.return_value = None

        payload = _resume_payload(action="next_wave")

        task = asyncio.create_task(_collect_events(emitter))
        await engine.resume_mission_stream(payload, emitter)
        await emitter.close()
        await task

        mock_consolidation.assert_called_once()
        mock_wave_cycle.assert_not_called()

    @patch("cadris_runtime.collaborative_engine.mission_store")
    @patch("cadris_runtime.collaborative_engine.run_single_wave_cycle")
    async def test_missing_memory_creates_fresh(self, mock_wave_cycle, mock_store):
        """If memory is not found in store, a fresh one should be created."""
        engine = CollaborativeEngine()
        emitter = EventEmitter()

        mock_store.aget = AsyncMock(return_value=None)
        mock_store.aput = AsyncMock()
        mock_wave_cycle.return_value = CriticOutput(
            overall_quality="good", reviews=[], questions_for_user=[], synthesis="OK"
        )

        payload = _resume_payload(
            action="answer_qualification",
            answer_text=json.dumps({"Q1": "Startups"}),
        )

        task = asyncio.create_task(_collect_events(emitter))
        result = await engine.resume_mission_stream(payload, emitter)
        await emitter.close()
        await task

        # Should have created fresh memory and proceeded
        assert result.mission_id == "test_m1"
        mock_wave_cycle.assert_called_once()

    @patch("cadris_runtime.collaborative_engine.mission_store")
    @patch("cadris_runtime.collaborative_engine.run_single_wave_cycle")
    async def test_je_sais_pas_answers_filtered(self, mock_wave_cycle, mock_store):
        """Answers with 'je_sais_pas' should be filtered out."""
        engine = CollaborativeEngine()
        emitter = EventEmitter()

        memory = MissionMemory(mission_id="test_m1", intake_text="SaaS", plan="free")
        mock_store.aget = AsyncMock(return_value=memory)
        mock_store.aput = AsyncMock()
        mock_wave_cycle.return_value = CriticOutput(
            overall_quality="good", reviews=[], questions_for_user=[], synthesis="OK"
        )

        payload = _resume_payload(
            action="answer_qualification",
            answer_text=json.dumps({"Q1": "Startups", "Q2": "je_sais_pas"}),
        )

        task = asyncio.create_task(_collect_events(emitter))
        await engine.resume_mission_stream(payload, emitter)
        await emitter.close()
        await task

        assert memory.qualification_answers == {"Q1": "Startups"}
        assert "Q2" not in memory.qualification_answers


# ── Async iterator mock helper ────────────────────────────


class AsyncIteratorMock:
    """Mock async iterator for Runner.run_streamed().stream_events()."""

    def __init__(self, items):
        self._items = iter(items)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self._items)
        except StopIteration:
            raise StopAsyncIteration
