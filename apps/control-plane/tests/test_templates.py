"""Tests for the dossier-templates router (cov-templates-01)."""
from __future__ import annotations

from uuid import uuid4


def _headers() -> dict[str, str]:
    return {"x-cadris-user-id": f"tpl-{uuid4().hex[:8]}"}


class TestTemplates:
    def test_list_templates_returns_all(self, client):
        resp = client.get("/api/dossier-templates", headers=_headers())
        assert resp.status_code == 200
        ids = {t["id"] for t in resp.json()["templates"]}
        assert {
            "standard",
            "startup_pitch",
            "internal_project",
            "rfp_response",
            "business_plan",
        } <= ids

    def test_get_template_by_id(self, client):
        resp = client.get("/api/dossier-templates/startup_pitch", headers=_headers())
        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == "startup_pitch"
        assert isinstance(body["sections"], list)

    def test_get_nonexistent_template_returns_404(self, client):
        resp = client.get("/api/dossier-templates/does_not_exist", headers=_headers())
        assert resp.status_code == 404

    def test_templates_require_auth(self, client):
        # No x-cadris-user-id header → rejected by require_user.
        resp = client.get("/api/dossier-templates")
        assert resp.status_code == 401
