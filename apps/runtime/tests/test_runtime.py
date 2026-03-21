from __future__ import annotations

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

DEFAULT_MISSION_ID = "test_mission_1"
DEFAULT_PROJECT_NAME = "Test Project"
DEFAULT_INTAKE_TEXT = (
    "Un projet SaaS qui aide les gens a structurer leur cadrage de projet initial."
)
DEFAULT_ANSWER_TEXT = (
    "Le probleme principal est le manque de structure dans le cadrage "
    "de projet pour les solo founders."
)


def _start_payload(*, flow_code: str = "demarrage", **overrides) -> dict:
    payload = {
        "mission_id": DEFAULT_MISSION_ID,
        "project_name": DEFAULT_PROJECT_NAME,
        "intake_text": DEFAULT_INTAKE_TEXT,
        "flow_code": flow_code,
    }
    payload.update(overrides)
    return payload


def _resume_payload(
    *, flow_code: str = "demarrage", cycle_number: int = 1, **overrides
) -> dict:
    payload = {
        "mission_id": DEFAULT_MISSION_ID,
        "project_name": DEFAULT_PROJECT_NAME,
        "intake_text": DEFAULT_INTAKE_TEXT,
        "answer_text": DEFAULT_ANSWER_TEXT,
        "flow_code": flow_code,
        "cycle_number": cycle_number,
        "previous_answers": [],
        "supporting_inputs": [],
    }
    payload.update(overrides)
    return payload


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["ok"] is True
    assert data["provider"] == "local"


# ---------------------------------------------------------------------------
# POST /internal/runtime/start
# ---------------------------------------------------------------------------


def test_start_demarrage(client):
    resp = client.post("/internal/runtime/start", json=_start_payload())
    assert resp.status_code == 200
    data = resp.json()

    assert "summary" in data
    assert data["status"] == "waiting_user"

    # artifact_blocks
    blocks = data["artifact_blocks"]
    assert len(blocks) == 3

    # active_question
    assert data["active_question"] is not None

    # timeline
    assert len(data["timeline"]) == 4


def test_start_projet_flou(client):
    resp = client.post(
        "/internal/runtime/start",
        json=_start_payload(flow_code="projet_flou"),
    )
    assert resp.status_code == 200
    data = resp.json()

    # The question title should differ from the demarrage flow
    demarrage_resp = client.post(
        "/internal/runtime/start", json=_start_payload(flow_code="demarrage")
    )
    demarrage_data = demarrage_resp.json()

    assert (
        data["active_question"]["title"]
        != demarrage_data["active_question"]["title"]
    )


def test_start_pivot(client):
    resp = client.post(
        "/internal/runtime/start",
        json=_start_payload(flow_code="pivot"),
    )
    assert resp.status_code == 200
    data = resp.json()

    title = data["active_question"]["title"].lower()
    assert "pivot" in title or "declencheur" in title


# ---------------------------------------------------------------------------
# POST /internal/runtime/resume
# ---------------------------------------------------------------------------


def test_resume_intermediate(client):
    resp = client.post(
        "/internal/runtime/resume",
        json=_resume_payload(cycle_number=1),
    )
    assert resp.status_code == 200
    data = resp.json()

    assert data["status"] == "waiting_user"
    assert data["active_question"] is not None
    assert len(data["certainty_entries"]) > 0


def test_resume_final(client):
    resp = client.post(
        "/internal/runtime/resume",
        json=_resume_payload(cycle_number=3),
    )
    assert resp.status_code == 200
    data = resp.json()

    assert data["status"] == "completed"
    assert data["dossier_title"] is not None
    assert len(data["dossier_sections"]) > 0
    assert data["quality_label"] is not None


@pytest.mark.parametrize(
    "flow_code, expected_label",
    [
        ("demarrage", "Demarrage"),
        ("projet_flou", "recadrage"),
        ("pivot", "pivot"),
    ],
)
def test_resume_final_dossier_title_matches_flow(
    client, flow_code, expected_label
):
    resp = client.post(
        "/internal/runtime/resume",
        json=_resume_payload(flow_code=flow_code, cycle_number=3),
    )
    assert resp.status_code == 200
    data = resp.json()

    assert data["status"] == "completed"
    assert expected_label.lower() in data["dossier_title"].lower()


# ---------------------------------------------------------------------------
# Artifact section structure
# ---------------------------------------------------------------------------


def test_artifact_sections_present(client):
    resp = client.post("/internal/runtime/start", json=_start_payload())
    assert resp.status_code == 200
    data = resp.json()

    for block in data["artifact_blocks"]:
        assert "sections" in block
        for section in block["sections"]:
            assert "key" in section
            assert "title" in section
            assert "content" in section
            assert "certainty" in section


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def test_start_intake_too_short(client):
    resp = client.post(
        "/internal/runtime/start",
        json=_start_payload(intake_text="trop court"),
    )
    assert resp.status_code == 422


# ---------------------------------------------------------------------------
# POST /internal/runtime/start-stream (SSE fallback in local mode)
# ---------------------------------------------------------------------------


def test_start_stream_returns_sse(client):
    """In local mode, start-stream should return text/event-stream with proper events."""
    resp = client.post("/internal/runtime/start-stream", json=_start_payload())
    assert resp.status_code == 200
    assert "text/event-stream" in resp.headers.get("content-type", "")

    body = resp.text
    assert "event: mission_completed" in body
    # Should contain real data, not just {"ok": true}
    assert "artifact_blocks" in body or "summary" in body


def test_resume_stream_returns_sse(client):
    """In local mode, resume-stream should return text/event-stream."""
    resp = client.post("/internal/runtime/resume-stream", json=_resume_payload())
    assert resp.status_code == 200
    assert "text/event-stream" in resp.headers.get("content-type", "")
    assert "event: mission_completed" in resp.text


# ---------------------------------------------------------------------------
# DELETE /internal/runtime/missions/{mission_id} (cleanup)
# ---------------------------------------------------------------------------


def test_cleanup_mission(client):
    resp = client.delete(f"/internal/runtime/missions/{DEFAULT_MISSION_ID}")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


def test_cleanup_nonexistent_mission(client):
    """Cleanup should succeed even for unknown missions."""
    resp = client.delete("/internal/runtime/missions/nonexistent_123")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True
