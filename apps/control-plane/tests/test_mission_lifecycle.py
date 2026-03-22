"""Integration tests for mission lifecycle.

Fixtures (client, auth_headers, mock_runtime, mock_renderer) from conftest.py.
Response builders from helpers.py.
"""
from __future__ import annotations

from .helpers import (
    INTAKE_TEXT,
    create_project,
    make_resume_response,
    make_start_response,
    stream_events,
)


# ---------------------------------------------------------------------------
# Mission creation
# ---------------------------------------------------------------------------


class TestCreateMission:
    def test_create_mission_demarrage_waiting_user(self, client, auth_headers, mock_runtime):
        start_resp = make_start_response(status="waiting_user")
        mock_runtime.start_mission.return_value = start_resp
        project = create_project(client, auth_headers)

        resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT, "flowCode": "demarrage"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()

        assert "mission" in data
        assert "project" in data
        mission = data["mission"]
        assert mission["status"] == "waiting_user"
        assert mission["flowCode"] == "demarrage"
        assert mission["flowLabel"] == "Nouveau projet"
        assert mission["activeQuestion"] is not None
        assert mission["activeQuestion"]["id"] == start_resp.active_question.id
        assert mission["dossierReady"] is False

        mock_runtime.start_mission.assert_awaited_once()

    def test_create_mission_projet_flou_label(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission.return_value = make_start_response()
        project = create_project(client, auth_headers)

        resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT, "flowCode": "projet_flou"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        mission = resp.json()["mission"]
        assert mission["flowCode"] == "projet_flou"
        assert mission["flowLabel"] == "Projet a recadrer"

    def test_create_mission_project_not_found(self, client, auth_headers, mock_runtime):
        resp = client.post(
            "/api/projects/nonexistent_project/missions",
            json={"intakeText": INTAKE_TEXT},
            headers=auth_headers,
        )
        assert resp.status_code == 404

    def test_create_mission_requires_auth(self, client, mock_runtime):
        resp = client.post(
            "/api/projects/some_project/missions",
            json={"intakeText": INTAKE_TEXT},
        )
        assert resp.status_code == 401

    def test_create_mission_intake_too_short(self, client, auth_headers, mock_runtime):
        project = create_project(client, auth_headers)
        resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": "Too short"},
            headers=auth_headers,
        )
        assert resp.status_code == 422

    def test_create_mission_increments_free_plan_counter(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission.return_value = make_start_response(status="waiting_user")
        project = create_project(client, auth_headers)

        resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT, "flowCode": "demarrage"},
            headers=auth_headers,
        )
        assert resp.status_code == 201

        plans = client.get("/api/billing/plans", headers=auth_headers)
        assert plans.status_code == 200
        assert plans.json()["missions_this_month"] == 1


# ---------------------------------------------------------------------------
# SSE streaming
# ---------------------------------------------------------------------------


class TestMissionStreaming:
    def test_run_stream_increments_free_plan_counter_only_after_start(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission_stream.return_value = stream_events(
            {"event": "qualification_questions", "data": {"questions": []}},
            {"event": "mission_completed", "data": {"ok": True}},
        )

        resp = client.post(
            "/api/missions/run",
            json={"intakeText": INTAKE_TEXT, "flowCode": "demarrage"},
            headers=auth_headers,
        )

        assert resp.status_code == 200
        assert "event: mission_created" in resp.text

        plans = client.get("/api/billing/plans", headers=auth_headers)
        assert plans.status_code == 200
        assert plans.json()["missions_this_month"] == 1

    def test_run_stream_does_not_burn_quota_on_start_failure(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission_stream.return_value = stream_events(
            {"event": "error", "data": {"error": "runtime boom"}},
        )

        resp = client.post(
            "/api/missions/run",
            json={"intakeText": INTAKE_TEXT, "flowCode": "demarrage"},
            headers=auth_headers,
        )

        assert resp.status_code == 502

        projects = client.get("/api/projects", headers=auth_headers)
        assert projects.status_code == 200
        assert projects.json() == []

        plans = client.get("/api/billing/plans", headers=auth_headers)
        assert plans.status_code == 200
        assert plans.json()["missions_this_month"] == 0

    def test_resume_wave_running_replays_current_wave(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission_stream.return_value = stream_events(
            {"event": "wave_started", "data": {"wave": 2}},
        )

        start_resp = client.post(
            "/api/missions/run",
            json={"intakeText": INTAKE_TEXT, "flowCode": "demarrage"},
            headers=auth_headers,
        )
        assert start_resp.status_code == 200

        mission_id = client.get("/api/missions", headers=auth_headers).json()[0]["id"]

        mock_runtime.resume_mission_stream.return_value = stream_events()
        resume_resp = client.post(
            f"/api/missions/{mission_id}/resume",
            json={"answerText": "", "action": "next_wave"},
            headers=auth_headers,
        )

        assert resume_resp.status_code == 200
        payload = mock_runtime.resume_mission_stream.call_args.args[0]
        assert payload.action == "refine_wave"


# ---------------------------------------------------------------------------
# Answer question
# ---------------------------------------------------------------------------


class TestAnswerQuestion:
    def _setup_mission(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission.return_value = make_start_response(status="waiting_user")
        project = create_project(client, auth_headers)
        resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT, "flowCode": "demarrage"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        return resp.json()["mission"]

    def test_answer_question_continues_mission(self, client, auth_headers, mock_runtime, mock_renderer):
        mission = self._setup_mission(client, auth_headers, mock_runtime)
        resume_resp = make_resume_response(completed=False)
        mock_runtime.resume_mission.return_value = resume_resp

        resp = client.post(
            f"/api/missions/{mission['id']}/answers",
            json={"answerText": "Notre public cible sont les PME de 10 a 50 employes."},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["mission"]["status"] == "waiting_user"
        assert data["mission"]["activeQuestion"]["id"] == resume_resp.active_question.id
        assert data["dossier"] is None

    def test_answer_question_completes_mission_with_dossier(self, client, auth_headers, mock_runtime, mock_renderer):
        mission = self._setup_mission(client, auth_headers, mock_runtime)
        mock_runtime.resume_mission.return_value = make_resume_response(completed=True)

        from cadris_cp.models import RendererResponse
        mock_renderer.render_markdown.return_value = RendererResponse(
            markdown="# Dossier de cadrage\n\nSynthese du projet.\n\n## Vision\n\nContenu vision."
        )

        resp = client.post(
            f"/api/missions/{mission['id']}/answers",
            json={"answerText": "Notre public cible sont les PME de 10 a 50 employes."},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["mission"]["status"] == "completed"
        assert data["mission"]["dossierReady"] is True
        assert data["dossier"]["title"] == "Dossier de cadrage"

    def test_answer_question_mission_not_found(self, client, auth_headers, mock_runtime):
        resp = client.post(
            "/api/missions/nonexistent/answers",
            json={"answerText": "Some answer that is long enough to pass validation rules."},
            headers=auth_headers,
        )
        assert resp.status_code == 404

    def test_answer_too_short(self, client, auth_headers, mock_runtime):
        mission = self._setup_mission(client, auth_headers, mock_runtime)
        mock_runtime.resume_mission.return_value = make_resume_response()
        resp = client.post(
            f"/api/missions/{mission['id']}/answers",
            json={"answerText": "Short"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["mission"]["status"] == "waiting_user"


# ---------------------------------------------------------------------------
# Get mission + logo
# ---------------------------------------------------------------------------


class TestGetMission:
    def test_get_mission_after_creation(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission.return_value = make_start_response()
        project = create_project(client, auth_headers)
        create_resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT},
            headers=auth_headers,
        )
        mission_id = create_resp.json()["mission"]["id"]

        resp = client.get(f"/api/missions/{mission_id}", headers=auth_headers)
        assert resp.status_code == 200
        mission = resp.json()
        assert mission["id"] == mission_id
        assert mission["status"] == "waiting_user"
        assert len(mission["artifactBlocks"]) >= 1
        assert mission["artifactBlocks"][0]["sections"][0]["key"] == "vision"
        assert len(mission["timeline"]) >= 1


class TestLogoEndpoint:
    def test_logo_requires_expert_plan(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission.return_value = make_start_response()
        project = create_project(client, auth_headers)
        create_resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT},
            headers=auth_headers,
        )
        mission_id = create_resp.json()["mission"]["id"]

        resp = client.post(
            f"/api/missions/{mission_id}/logo",
            json={
                "projectName": "Cadris",
                "projectBrief": "Un outil pour structurer le cadrage produit.",
                "numVariants": 2,
            },
            headers=auth_headers,
        )

        assert resp.status_code == 403
        assert resp.json()["code"] == "forbidden"


# Export/share/dossier tests → test_dossier_exports.py
