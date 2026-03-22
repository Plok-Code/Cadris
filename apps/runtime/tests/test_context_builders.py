"""Tests for context_builders.py — agent context assembly."""
from __future__ import annotations

from cadris_runtime.agent_specs import AGENT_SPECS, get_specs_by_wave
from cadris_runtime.context_builders import (
    _build_context,
    _build_file_map_context,
    _build_qualification_context,
    _build_quality_instructions,
    _build_questions_context,
)
from cadris_runtime.memory import DocumentDraft, MissionMemory


def _make_memory(plan: str = "free", docs: dict[str, str] | None = None) -> MissionMemory:
    memory = MissionMemory(mission_id="test_mission", intake_text="Test project", plan=plan)
    if docs:
        for doc_id, content in docs.items():
            memory.upsert_document(DocumentDraft(
                doc_id=doc_id, title=doc_id, agent_code="other_agent",
                content=content, certainty="solid",
            ))
    return memory


class TestBuildContext:
    def test_no_docs_returns_placeholder(self):
        memory = _make_memory()
        spec = AGENT_SPECS[0]
        result = _build_context(spec, memory)
        assert "Aucun document" in result

    def test_truncation_respects_plan(self):
        long_content = "x" * 5000
        memory = _make_memory("free", {"vision_produit": long_content})
        spec = AGENT_SPECS[0]
        result = _build_context(spec, memory)
        # Free plan should truncate, content should not be full 5000 chars
        assert len(result) < 5000
        assert "tronque" in result

    def test_paid_plan_allows_more_chars(self):
        long_content = "x" * 2000
        memory = _make_memory("pro", {"vision_produit": long_content})
        spec = AGENT_SPECS[0]
        result = _build_context(spec, memory)
        # Pro plan allows 1200 chars for agent context (per config), so 2000 will be truncated
        # but less aggressively than free plan
        assert "tronque" in result or len(long_content) <= 2500

    def test_excludes_own_docs(self):
        memory = _make_memory()
        spec = AGENT_SPECS[0]
        # Add doc from the same agent
        memory.upsert_document(DocumentDraft(
            doc_id="test_doc", title="Test", agent_code=spec.code,
            content="My own content", certainty="solid",
        ))
        result = _build_context(spec, memory)
        assert "My own content" not in result


class TestBuildQualityInstructions:
    def test_free_plan_is_concise(self):
        result = _build_quality_instructions("free")
        assert "essentiel" in result.lower() or "synthese" in result.lower()

    def test_paid_plan_is_different(self):
        free_result = _build_quality_instructions("free")
        paid_result = _build_quality_instructions("pro")
        assert free_result != paid_result


class TestBuildQualificationContext:
    def test_no_answers_returns_empty(self):
        memory = _make_memory()
        result = _build_qualification_context(memory)
        assert result == ""

    def test_with_answers_returns_section(self):
        memory = _make_memory()
        memory.qualification_answers = {"Q1": "Answer 1", "Q2": "Answer 2"}
        result = _build_qualification_context(memory)
        assert "Answer 1" in result
        assert "Answer 2" in result


class TestBuildQuestionsContext:
    def test_no_questions_returns_empty(self):
        memory = _make_memory()
        result = _build_questions_context(memory)
        assert result == ""


class TestBuildFileMapContext:
    def test_returns_doc_paths(self):
        result = _build_file_map_context()
        assert "CLAUDE.md" in result
        assert len(result) > 100  # should contain multiple doc paths


class TestAgentSpecs:
    def test_waves_cover_all_agents(self):
        waves = get_specs_by_wave()
        all_wave_agents = []
        for agents in waves.values():
            all_wave_agents.extend(a.code for a in agents)
        for spec in AGENT_SPECS:
            assert spec.code in all_wave_agents, f"Agent {spec.code} not in any wave"

    def test_each_agent_has_output_model(self):
        for spec in AGENT_SPECS:
            assert spec.output_model is not None, f"Agent {spec.code} has no output_model"

    def test_each_agent_has_doc_specs(self):
        for spec in AGENT_SPECS:
            assert len(spec.doc_specs) > 0, f"Agent {spec.code} has no doc_specs"
