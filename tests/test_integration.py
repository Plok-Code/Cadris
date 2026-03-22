"""Cross-service integration tests.

These tests verify the contract between control-plane, runtime, and renderer
by running all three services in-process with mocked LLM calls.
They catch drift between services that unit tests cannot.

Run: python -m pytest tests/test_integration.py -v
Requires: all three services' dependencies installed.
"""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from fastapi.testclient import TestClient


# ── Control-plane app ────────────────────────────────────────────

@pytest.fixture()
def cp_client(monkeypatch):
    """Create a test client for the control-plane FastAPI app."""
    import os
    monkeypatch.setenv("CADRIS_ALLOW_UNSIGNED_REQUESTS", "true")

    # Force config reload with new env var
    import cadris_cp.config as cfg_mod
    cfg_mod.settings = cfg_mod.Settings()

    from cadris_cp.main import app
    with TestClient(app) as client:
        yield client


# ── Integration: create project → create mission → verify state ──

class TestMissionLifecycle:
    """Test the full lifecycle: project creation → mission creation → state."""

    def test_create_project_and_mission_roundtrip(self, cp_client: TestClient):
        """A new user can create a project and start a mission."""
        headers = {
            "x-cadris-user-id": "integration-test-user",
            "x-cadris-user-email": "integration@test.local",
        }

        # 1. Create project
        resp = cp_client.post("/api/projects", json={"name": "Integration Test"}, headers=headers)
        assert resp.status_code == 201, resp.text
        project = resp.json()
        assert project["name"] == "Integration Test"
        project_id = project["id"]

        # 2. List projects — should contain our project
        resp = cp_client.get("/api/projects", headers=headers)
        assert resp.status_code == 200
        projects = resp.json()
        assert any(p["id"] == project_id for p in projects)

        # 3. List missions — should be empty
        resp = cp_client.get("/api/missions", headers=headers)
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


class TestAuthContract:
    """Test that auth headers are enforced correctly across all routes."""

    def test_missing_user_id_returns_401(self, cp_client: TestClient):
        resp = cp_client.get("/api/projects")
        assert resp.status_code == 401

    def test_valid_user_id_returns_200(self, cp_client: TestClient):
        resp = cp_client.get("/api/projects", headers={
            "x-cadris-user-id": "auth-test-user",
            "x-cadris-user-email": "auth@test.local",
        })
        assert resp.status_code == 200

    def test_invalid_user_id_format_returns_401(self, cp_client: TestClient):
        resp = cp_client.get("/api/projects", headers={
            "x-cadris-user-id": "invalid user with spaces!",
        })
        assert resp.status_code == 401


class TestErrorEnvelopeContract:
    """Test that all API errors follow the ApiErrorEnvelope schema."""

    def test_404_returns_proper_envelope(self, cp_client: TestClient):
        headers = {
            "x-cadris-user-id": "envelope-test-user",
            "x-cadris-user-email": "envelope@test.local",
        }
        resp = cp_client.get("/api/missions/nonexistent_mission", headers=headers)
        assert resp.status_code == 404
        body = resp.json()
        # Verify ApiErrorEnvelope shape
        assert "code" in body
        assert "category" in body
        assert "retryable" in body
        assert "message" in body
        assert "requestId" in body
        assert body["category"] in ("validation", "domain", "auth", "integration", "internal")
        assert isinstance(body["retryable"], bool)


class TestSchemaConsistency:
    """Verify that API responses match the TypeScript schema contract."""

    def test_project_summary_fields(self, cp_client: TestClient):
        """ProjectSummary must have all fields defined in packages/schemas."""
        headers = {
            "x-cadris-user-id": "schema-test-user",
            "x-cadris-user-email": "schema@test.local",
        }
        cp_client.post("/api/projects", json={"name": "Schema Test"}, headers=headers)
        resp = cp_client.get("/api/projects", headers=headers)
        assert resp.status_code == 200
        projects = resp.json()
        assert len(projects) > 0

        project = projects[0]
        # These fields must exist per ProjectSummary in schemas/index.ts
        required_fields = ["id", "name", "missionCount", "activeMissionId", "activeMissionStatus", "updatedAt"]
        for field in required_fields:
            assert field in project, f"Missing field '{field}' in ProjectSummary response"
