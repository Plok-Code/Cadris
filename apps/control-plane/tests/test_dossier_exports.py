"""Integration tests for dossier export and share endpoints.

Split from test_mission_lifecycle.py to stay under 400-line policy.
Fixtures from conftest.py, helpers from helpers.py.
"""
from __future__ import annotations

from cadris_cp.models import RendererResponse

from .helpers import (
    INTAKE_TEXT,
    create_project,
    make_resume_response,
    make_start_response,
)


class TestDossierMarkdownExport:
    def test_markdown_404_when_no_dossier(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission.return_value = make_start_response()
        project = create_project(client, auth_headers)
        create_resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT},
            headers=auth_headers,
        )
        mission_id = create_resp.json()["mission"]["id"]
        resp = client.get(f"/api/missions/{mission_id}/dossier/markdown", headers=auth_headers)
        assert resp.status_code == 404

    def test_markdown_404_nonexistent_mission(self, client, auth_headers):
        resp = client.get("/api/missions/nonexistent/dossier/markdown", headers=auth_headers)
        assert resp.status_code == 404


class TestDossierShare:
    def test_share_404_when_no_dossier(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission.return_value = make_start_response()
        project = create_project(client, auth_headers)
        create_resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT},
            headers=auth_headers,
        )
        mission_id = create_resp.json()["mission"]["id"]
        resp = client.post(f"/api/missions/{mission_id}/dossier/share", headers=auth_headers)
        assert resp.status_code == 404

    def test_share_404_nonexistent_mission(self, client, auth_headers):
        resp = client.post("/api/missions/nonexistent/dossier/share", headers=auth_headers)
        assert resp.status_code == 404

    def test_share_link_prefers_allowed_origin_header(self, client, auth_headers, mock_runtime, mock_renderer):
        project = create_project(client, auth_headers)
        mock_runtime.start_mission.return_value = make_start_response(status="waiting_user")
        create_resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT},
            headers=auth_headers,
        )
        mission_id = create_resp.json()["mission"]["id"]

        mock_runtime.resume_mission.return_value = make_resume_response(completed=True)
        mock_renderer.render_markdown.return_value = RendererResponse(
            markdown="# Dossier de cadrage\n\nContenu complet."
        )

        answer_resp = client.post(
            f"/api/missions/{mission_id}/answers",
            json={"answerText": "Notre objectif est de digitaliser les processus RH des PME."},
            headers=auth_headers,
        )
        assert answer_resp.status_code == 200

        share_resp = client.post(
            f"/api/missions/{mission_id}/dossier/share",
            headers={**auth_headers, "origin": "http://localhost:3001"},
        )
        assert share_resp.status_code == 200
        assert share_resp.json()["shareUrl"].startswith("http://localhost:3001/api/shared/")


class TestSharedDossierAccess:
    def test_invalid_share_token_404(self, client):
        resp = client.get("/api/shared/invalid_token_abc123")
        assert resp.status_code == 404

    def test_shared_dossier_sanitizes_embedded_html(self, client, auth_headers, mock_runtime, mock_renderer):
        project = create_project(client, auth_headers)
        mock_runtime.start_mission.return_value = make_start_response(status="waiting_user")
        create_resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT},
            headers=auth_headers,
        )
        mission_id = create_resp.json()["mission"]["id"]

        completed = make_resume_response(completed=True)
        completed.dossier_sections[0].content = (
            "<script>alert('xss')</script>\n\n**Contenu legitime**\n\n[Lien](javascript:alert(1))"
        )
        mock_runtime.resume_mission.return_value = completed
        mock_renderer.render_markdown.return_value = RendererResponse(
            markdown="# Dossier de cadrage\n\nContenu legitime"
        )

        answer_resp = client.post(
            f"/api/missions/{mission_id}/answers",
            json={"answerText": "Notre objectif est de digitaliser les processus RH des PME."},
            headers=auth_headers,
        )
        assert answer_resp.status_code == 200

        share_resp = client.post(f"/api/missions/{mission_id}/dossier/share", headers=auth_headers)
        assert share_resp.status_code == 200
        share_url = share_resp.json()["shareUrl"]
        token = share_url.rsplit("/", 1)[-1]

        resp = client.get(f"/api/shared/{token}")
        assert resp.status_code == 200
        assert "<script" not in resp.text.lower()
        assert "javascript:alert" not in resp.text.lower()
        assert "Contenu legitime" in resp.text


class TestRevokeExport:
    def test_revoke_nonexistent_export_404(self, client, auth_headers):
        resp = client.delete("/api/exports/nonexistent", headers=auth_headers)
        assert resp.status_code == 404


class TestDossierEndpoints:
    def test_get_dossier_404_when_no_dossier(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission.return_value = make_start_response()
        project = create_project(client, auth_headers)
        create_resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT},
            headers=auth_headers,
        )
        mission_id = create_resp.json()["mission"]["id"]
        resp = client.get(f"/api/missions/{mission_id}/dossier", headers=auth_headers)
        assert resp.status_code == 404

    def test_get_dossier_pdf_404_when_no_dossier(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission.return_value = make_start_response()
        project = create_project(client, auth_headers)
        create_resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT},
            headers=auth_headers,
        )
        mission_id = create_resp.json()["mission"]["id"]
        resp = client.get(f"/api/missions/{mission_id}/dossier/pdf", headers=auth_headers)
        assert resp.status_code == 404


class TestFullLifecycle:
    def test_full_lifecycle_with_dossier_and_exports(self, client, auth_headers, mock_runtime, mock_renderer):
        project = create_project(client, auth_headers, name="Lifecycle Test")

        mock_runtime.start_mission.return_value = make_start_response(status="waiting_user")
        resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT, "flowCode": "demarrage"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        mission_id = resp.json()["mission"]["id"]

        mock_runtime.resume_mission.return_value = make_resume_response(completed=True)
        mock_renderer.render_markdown.return_value = RendererResponse(
            markdown="# Dossier Final\n\nContenu complet."
        )

        resp = client.post(
            f"/api/missions/{mission_id}/answers",
            json={"answerText": "Notre objectif est de digitaliser les processus RH des PME."},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["mission"]["status"] == "completed"
        assert resp.json()["dossier"] is not None

        resp = client.get(f"/api/missions/{mission_id}/dossier", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["title"] == "Dossier de cadrage"

        resp = client.get(f"/api/missions/{mission_id}/dossier/markdown", headers=auth_headers)
        assert resp.status_code == 200
        assert "application/zip" in resp.headers["content-type"]

        resp = client.post(f"/api/missions/{mission_id}/dossier/share", headers=auth_headers)
        assert resp.status_code == 200
        share_data = resp.json()
        assert "shareUrl" in share_data
        token = share_data["shareUrl"].rsplit("/", 1)[-1]
        export_id = share_data["export"]["id"]

        resp = client.get(f"/api/missions/{mission_id}/exports", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) >= 2

        resp = client.get(f"/api/shared/{token}")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]

        resp = client.delete(f"/api/exports/{export_id}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["revoked"] is True

        resp = client.get(f"/api/shared/{token}")
        assert resp.status_code == 404
