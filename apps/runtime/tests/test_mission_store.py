from __future__ import annotations

from app import mission_store
from app.memory import AgentQuestion, DocumentDraft, MissionMemory


def _sample_memory() -> MissionMemory:
    memory = MissionMemory(
        mission_id="mission-persisted",
        intake_text="Plateforme SaaS pour piloter les operations RH.",
        plan="free",
        current_wave=2,
        user_answers=["Hypotheses raisonnables", "Continuer"],
        qualification_questions=[{"question": "Quel est le besoin principal ?", "context": "Qualification"}],
        qualification_answers={"Quel est le besoin principal ?": "Automatiser les workflows RH"},
    )
    memory.upsert_document(
        DocumentDraft(
            doc_id="vision_produit",
            title="Vision produit",
            agent_code="strategy",
            content="Vision structuree du produit.",
            certainty="solid",
        )
    )
    memory.questions.append(
        AgentQuestion(
            from_agent="critic",
            to="user",
            question="Validez-vous cette direction ?",
            context="Review wave 2",
        )
    )
    return memory


def test_mission_store_restores_snapshot_after_cache_loss(tmp_path, monkeypatch):
    monkeypatch.setattr(mission_store, "_engine", None)
    monkeypatch.setattr(mission_store, "_snapshot_dir", tmp_path)
    mission_store._store.clear()

    memory = _sample_memory()
    mission_store.put(memory)
    mission_store._store.clear()

    restored = mission_store.get(memory.mission_id)

    assert restored is not None
    assert restored.current_wave == 2
    assert restored.documents["vision_produit"].content == "Vision structuree du produit."
    assert restored.qualification_answers["Quel est le besoin principal ?"] == "Automatiser les workflows RH"


def test_mission_store_remove_deletes_persisted_snapshot(tmp_path, monkeypatch):
    monkeypatch.setattr(mission_store, "_engine", None)
    monkeypatch.setattr(mission_store, "_snapshot_dir", tmp_path)
    mission_store._store.clear()

    memory = _sample_memory()
    mission_store.put(memory)

    mission_store.remove(memory.mission_id)
    mission_store._store.clear()

    assert mission_store.get(memory.mission_id) is None
    assert not (tmp_path / f"{memory.mission_id}.json").exists()
