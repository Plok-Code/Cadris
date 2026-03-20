"""Integration tests for mission lifecycle and export/share endpoints.

Mocks RuntimeClient and RendererClient to avoid real HTTP calls.
"""
from __future__ import annotations

from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.models import (
    ArtifactBlock,
    DossierSection,
    MissionAgent,
    MissionMessage,
    MissionQuestion,
    RuntimeResumeResponse,
    RuntimeStartResponse,
    TimelineItem,
)


# ---------------------------------------------------------------------------
# Helpers: build realistic mock responses with unique IDs
# ---------------------------------------------------------------------------

def _uid(prefix: str = "") -> str:
    return f"{prefix}{uuid4().hex[:8]}"


def _make_start_response(*, status="waiting_user") -> RuntimeStartResponse:
    return RuntimeStartResponse(
        summary="Analyse initiale du projet en cours.",
        next_step="Repondez a la question pour affiner le cadrage.",
        artifact_blocks=[
            ArtifactBlock(
                id=_uid("block_"),
                title="Vision",
                status="in_progress",
                certainty="unknown",
                summary="Vision a definir.",
                content="Le projet vise a ...",
            ),
        ],
        active_question=MissionQuestion(
            id=_uid("q_"),
            title="Objectif principal",
            body="Quel est l'objectif principal de votre projet ?",
            status="waiting",
        ),
        active_agents=[
            MissionAgent(
                code="strategist",
                label="Strategiste",
                role="Analyse strategique",
                status="waiting",
                prompt_key="strategist_v1",
                prompt_version="1.0",
                summary="En attente de la reponse utilisateur.",
            ),
        ],
        recent_messages=[
            MissionMessage(
                id=_uid("msg_"),
                agent_code="strategist",
                agent_label="Strategiste",
                stage="intake",
                title="Analyse recue",
                body="J'ai bien recu votre brief.",
            ),
        ],
        timeline=[
            TimelineItem(id=_uid("tl_"), label="Prise de brief", status="completed"),
            TimelineItem(id=_uid("tl_"), label="Analyse", status="in_progress"),
            TimelineItem(id=_uid("tl_"), label="Dossier", status="not_started"),
        ],
        status=status,
    )


def _make_resume_response(*, completed=False) -> RuntimeResumeResponse:
    status = "completed" if completed else "waiting_user"
    resp = RuntimeResumeResponse(
        summary="Le projet se precise.",
        next_step="Dossier en cours de finalisation." if completed else "Repondez a la prochaine question.",
        artifact_blocks=[
            ArtifactBlock(
                id=_uid("block_"),
                title="Vision",
                status="complete" if completed else "in_progress",
                certainty="solid" if completed else "to_confirm",
                summary="Vision clarifiee.",
                content="Le projet vise a creer une plateforme.",
            ),
        ],
        active_question=None if completed else MissionQuestion(
            id=_uid("q_"),
            title="Public cible",
            body="Qui est le public cible de votre projet ?",
            status="waiting",
        ),
        active_agents=[
            MissionAgent(
                code="strategist",
                label="Strategiste",
                role="Analyse strategique",
                status="done" if completed else "waiting",
                prompt_key="strategist_v1",
                prompt_version="1.0",
                summary="Analyse terminee." if completed else "En attente.",
            ),
        ],
        recent_messages=[
            MissionMessage(
                id=_uid("msg_"),
                agent_code="strategist",
                agent_label="Strategiste",
                stage="analysis",
                title="Mise a jour",
                body="Merci pour votre reponse.",
            ),
        ],
        timeline=[
            TimelineItem(id=_uid("tl_"), label="Prise de brief", status="completed"),
            TimelineItem(id=_uid("tl_"), label="Analyse", status="completed" if completed else "in_progress"),
            TimelineItem(id=_uid("tl_"), label="Dossier", status="completed" if completed else "not_started"),
        ],
        status=status,
    )
    if completed:
        resp.dossier_title = "Dossier de cadrage"
        resp.dossier_summary = "Synthese du projet."
        resp.dossier_sections = [
            DossierSection(id=_uid("sec_"), title="Vision", content="Contenu vision.", certainty="solid"),
        ]
        resp.quality_label = "Bon"
    return resp


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def mock_runtime():
    with patch("app.main.runtime_client") as mock:
        mock.start_mission = AsyncMock()
        mock.resume_mission = AsyncMock()
        yield mock


@pytest.fixture()
def mock_renderer():
    with patch("app.main.renderer_client") as mock:
        mock.render_markdown = AsyncMock()
        mock.render_pdf = AsyncMock()
        yield mock


def _create_project(client, auth_headers, name=None):
    if name is None:
        name = f"Projet {_uid()}"
    resp = client.post("/api/projects", json={"name": name}, headers=auth_headers)
    assert resp.status_code == 201
    return resp.json()


INTAKE_TEXT = "Je souhaite creer une plateforme de gestion de projets innovante pour les PME."


# ---------------------------------------------------------------------------
# Mission lifecycle tests
# ---------------------------------------------------------------------------


class TestCreateMission:
    def test_create_mission_demarrage_waiting_user(self, client, auth_headers, mock_runtime):
        start_resp = _make_start_response(status="waiting_user")
        mock_runtime.start_mission.return_value = start_resp
        project = _create_project(client, auth_headers)

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
        mock_runtime.start_mission.return_value = _make_start_response()
        project = _create_project(client, auth_headers)

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
        project = _create_project(client, auth_headers)
        resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": "Too short"},
            headers=auth_headers,
        )
        assert resp.status_code == 422


class TestAnswerQuestion:
    def _setup_mission(self, client, auth_headers, mock_runtime):
        """Create a project and mission, return mission data."""
        mock_runtime.start_mission.return_value = _make_start_response(status="waiting_user")
        project = _create_project(client, auth_headers)
        resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT, "flowCode": "demarrage"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        return resp.json()["mission"]

    def test_answer_question_continues_mission(self, client, auth_headers, mock_runtime, mock_renderer):
        mission = self._setup_mission(client, auth_headers, mock_runtime)
        resume_resp = _make_resume_response(completed=False)
        mock_runtime.resume_mission.return_value = resume_resp

        resp = client.post(
            f"/api/missions/{mission['id']}/answers",
            json={"answerText": "Notre public cible sont les PME de 10 a 50 employes."},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["mission"]["status"] == "waiting_user"
        assert data["mission"]["activeQuestion"] is not None
        assert data["mission"]["activeQuestion"]["id"] == resume_resp.active_question.id
        assert data["dossier"] is None

        mock_runtime.resume_mission.assert_awaited_once()
        mock_renderer.render_markdown.assert_not_awaited()

    def test_answer_question_completes_mission_with_dossier(self, client, auth_headers, mock_runtime, mock_renderer):
        mission = self._setup_mission(client, auth_headers, mock_runtime)
        mock_runtime.resume_mission.return_value = _make_resume_response(completed=True)

        from app.models import RendererResponse
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
        assert data["dossier"] is not None
        assert data["dossier"]["title"] == "Dossier de cadrage"
        assert "Vision" in data["dossier"]["markdown"]

        mock_renderer.render_markdown.assert_awaited_once()

    def test_answer_question_mission_not_found(self, client, auth_headers, mock_runtime):
        resp = client.post(
            "/api/missions/nonexistent/answers",
            json={"answerText": "Some answer that is long enough to pass validation rules."},
            headers=auth_headers,
        )
        assert resp.status_code == 404

    def test_answer_too_short(self, client, auth_headers, mock_runtime):
        mission = self._setup_mission(client, auth_headers, mock_runtime)
        mock_runtime.resume_mission.return_value = _make_resume_response()
        resp = client.post(
            f"/api/missions/{mission['id']}/answers",
            json={"answerText": "Short"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["mission"]["status"] == "waiting_user"


class TestGetMission:
    def test_get_mission_after_creation(self, client, auth_headers, mock_runtime):
        mock_runtime.start_mission.return_value = _make_start_response()
        project = _create_project(client, auth_headers)
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
        assert len(mission["timeline"]) >= 1


# ---------------------------------------------------------------------------
# Export / share endpoint tests
# ---------------------------------------------------------------------------


class TestDossierMarkdownExport:
    def test_markdown_404_when_no_dossier(self, client, auth_headers, mock_runtime):
        """GET /api/missions/{id}/dossier/markdown returns 404 when no dossier exists."""
        mock_runtime.start_mission.return_value = _make_start_response()
        project = _create_project(client, auth_headers)
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
        """POST /api/missions/{id}/dossier/share returns 404 when no dossier exists."""
        mock_runtime.start_mission.return_value = _make_start_response()
        project = _create_project(client, auth_headers)
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


class TestSharedDossierAccess:
    def test_invalid_share_token_404(self, client):
        """GET /api/shared/invalid_token returns 404."""
        resp = client.get("/api/shared/invalid_token_abc123")
        assert resp.status_code == 404

    def test_shared_dossier_sanitizes_embedded_html(self, client, auth_headers, mock_runtime, mock_renderer):
        project = _create_project(client, auth_headers)
        mock_runtime.start_mission.return_value = _make_start_response(status="waiting_user")
        create_resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT},
            headers=auth_headers,
        )
        mission_id = create_resp.json()["mission"]["id"]

        completed = _make_resume_response(completed=True)
        completed.dossier_sections[0].content = (
            "<script>alert('xss')</script>\n\n**Contenu legitime**\n\n[Lien](javascript:alert(1))"
        )
        mock_runtime.resume_mission.return_value = completed

        from app.models import RendererResponse
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
        token = share_resp.json()["export"]["token"]

        resp = client.get(f"/api/shared/{token}")
        assert resp.status_code == 200
        assert "<script" not in resp.text.lower()
        assert "javascript:alert" not in resp.text.lower()
        assert "Contenu legitime" in resp.text


class TestRevokeExport:
    def test_revoke_nonexistent_export_404(self, client, auth_headers):
        """DELETE /api/exports/nonexistent returns 404."""
        resp = client.delete("/api/exports/nonexistent", headers=auth_headers)
        assert resp.status_code == 404


class TestDossierEndpoints:
    def test_get_dossier_404_when_no_dossier(self, client, auth_headers, mock_runtime):
        """GET /api/missions/{id}/dossier returns 404 when mission exists but has no dossier."""
        mock_runtime.start_mission.return_value = _make_start_response()
        project = _create_project(client, auth_headers)
        create_resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT},
            headers=auth_headers,
        )
        mission_id = create_resp.json()["mission"]["id"]

        resp = client.get(f"/api/missions/{mission_id}/dossier", headers=auth_headers)
        assert resp.status_code == 404

    def test_get_dossier_pdf_404_when_no_dossier(self, client, auth_headers, mock_runtime):
        """GET /api/missions/{id}/dossier/pdf returns 404 when mission exists but has no dossier."""
        mock_runtime.start_mission.return_value = _make_start_response()
        project = _create_project(client, auth_headers)
        create_resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT},
            headers=auth_headers,
        )
        mission_id = create_resp.json()["mission"]["id"]

        resp = client.get(f"/api/missions/{mission_id}/dossier/pdf", headers=auth_headers)
        assert resp.status_code == 404


class TestFullLifecycle:
    """End-to-end: create project -> create mission -> answer -> complete -> export."""

    def test_full_lifecycle_with_dossier_and_exports(self, client, auth_headers, mock_runtime, mock_renderer):
        # 1. Create project
        project = _create_project(client, auth_headers, name="Lifecycle Test")

        # 2. Create mission
        mock_runtime.start_mission.return_value = _make_start_response(status="waiting_user")
        resp = client.post(
            f"/api/projects/{project['id']}/missions",
            json={"intakeText": INTAKE_TEXT, "flowCode": "demarrage"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        mission_id = resp.json()["mission"]["id"]

        # 3. Answer question -> complete
        mock_runtime.resume_mission.return_value = _make_resume_response(completed=True)
        from app.models import RendererResponse
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

        # 4. Get dossier
        resp = client.get(f"/api/missions/{mission_id}/dossier", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["title"] == "Dossier de cadrage"

        # 5. Export markdown
        resp = client.get(f"/api/missions/{mission_id}/dossier/markdown", headers=auth_headers)
        assert resp.status_code == 200
        assert "application/zip" in resp.headers["content-type"]

        # 6. Create share link
        resp = client.post(f"/api/missions/{mission_id}/dossier/share", headers=auth_headers)
        assert resp.status_code == 200
        share_data = resp.json()
        assert "shareUrl" in share_data
        assert "export" in share_data
        token = share_data["export"]["token"]
        export_id = share_data["export"]["id"]

        # 7. List exports
        resp = client.get(f"/api/missions/{mission_id}/exports", headers=auth_headers)
        assert resp.status_code == 200
        exports = resp.json()
        assert len(exports) >= 2  # markdown export + share link

        # 8. Access shared dossier (public, no auth)
        resp = client.get(f"/api/shared/{token}")
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]
        assert "Dossier de cadrage" in resp.text

        # 9. Revoke share link
        resp = client.delete(f"/api/exports/{export_id}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["revoked"] is True

        # 10. Shared link no longer works after revocation
        resp = client.get(f"/api/shared/{token}")
        assert resp.status_code == 404
