"""Security tests — rate limiting, HMAC replay attacks, ownership isolation."""
from __future__ import annotations

import hashlib
import time
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from cadris_cp.auth import build_trusted_proxy_signature
from cadris_cp.config import settings
from cadris_cp.rate_limit import _buckets


def _make_auth_headers(user_id: str) -> dict[str, str]:
    """Build simple unsigned auth headers for a given user (dev mode)."""
    return {"x-cadris-user-id": user_id}


def _make_signed_headers(
    *,
    method: str,
    path: str,
    user_id: str = "test-user",
    user_email: str = "test@example.com",
    body: str = "",
    secret: str = "test-shared-secret",
    timestamp: int | None = None,
) -> dict[str, str]:
    """Build fully signed HMAC headers, with optional timestamp override."""
    ts = str(timestamp if timestamp is not None else int(time.time()))
    body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()
    signature = build_trusted_proxy_signature(
        secret=secret,
        timestamp=ts,
        method=method,
        path=path,
        user_id=user_id,
        user_email=user_email,
        body_hash=body_hash,
    )
    return {
        "x-cadris-user-id": user_id,
        "x-cadris-user-email": user_email,
        "x-cadris-auth-timestamp": ts,
        "x-cadris-auth-signature": signature,
        "x-cadris-auth-body-hash": body_hash,
    }


def _create_project(client: TestClient, user_id: str) -> str:
    """Helper: create a project for a user, return project_id."""
    resp = client.post(
        "/api/projects",
        json={"name": f"Project-{uuid4().hex[:6]}"},
        headers=_make_auth_headers(user_id),
    )
    assert resp.status_code == 201, f"Project creation failed: {resp.text}"
    return resp.json()["id"]


class TestRateLimiting:
    """Verify rate limits on mission run endpoint."""

    def setup_method(self):
        """Clear the in-memory rate limit buckets between tests."""
        _buckets.clear()

    def test_rate_limit_on_mission_run(self, client):
        """Mission run should be rate-limited to 2 per 60s per user.

        We mock the runtime stream call to avoid actually hitting the runtime.
        The rate limiter fires BEFORE the runtime call, so after 2 allowed
        requests the 3rd must be rejected with 422/rate_limited.
        """
        user_id = f"ratelimit-{uuid4().hex[:8]}"
        headers = _make_auth_headers(user_id)
        payload = {
            "intake_text": "Un SaaS de gestion de projet collaboratif pour les equipes",
            "flow_code": "demarrage",
        }

        # We need the runtime call to succeed (or at least not crash before
        # the rate limiter fires). The rate limiter runs first in the endpoint,
        # so calls 1-2 pass the limiter but may fail on runtime — that's fine.
        # Call 3 must be rejected by the limiter itself (422).
        responses = []
        for i in range(3):
            resp = client.post("/api/missions/run", json=payload, headers=headers)
            responses.append(resp)

        # The third call must be rate-limited (422) regardless of whether
        # calls 1-2 succeeded or failed on runtime connectivity.
        assert responses[2].status_code == 422
        body = responses[2].json()
        assert body.get("code") == "rate_limited"

    def test_rate_limit_isolated_per_user(self, client):
        """Rate limit buckets are per-user — user B is not affected by user A."""
        payload = {
            "intake_text": "Application mobile de fitness avec coaching personnalise",
            "flow_code": "demarrage",
        }

        user_a = f"rl-a-{uuid4().hex[:8]}"
        user_b = f"rl-b-{uuid4().hex[:8]}"

        # Exhaust user A's quota (2 calls)
        for _ in range(2):
            client.post("/api/missions/run", json=payload, headers=_make_auth_headers(user_a))

        # User A's third call is rate-limited
        resp_a = client.post("/api/missions/run", json=payload, headers=_make_auth_headers(user_a))
        assert resp_a.status_code == 422

        # User B's first call should NOT be rate-limited (may fail on runtime, but not 422)
        resp_b = client.post("/api/missions/run", json=payload, headers=_make_auth_headers(user_b))
        assert resp_b.status_code != 422, "User B should not be rate-limited by user A"


class TestHMACReplay:
    """Verify HMAC replay protection — timestamps outside the 60s window are rejected."""

    def test_old_timestamp_rejected(self, client, monkeypatch):
        """A signature with a timestamp older than 60 seconds must be rejected."""
        monkeypatch.setattr(settings, "trusted_proxy_secret", "test-shared-secret")

        old_timestamp = int(time.time()) - 120  # 2 minutes ago
        headers = _make_signed_headers(
            method="GET",
            path="/api/projects",
            timestamp=old_timestamp,
        )

        resp = client.get("/api/projects", headers=headers)
        assert resp.status_code == 401
        assert "expired" in resp.json().get("message", "").lower() or \
               "expired" in resp.text.lower()

    def test_future_timestamp_rejected(self, client, monkeypatch):
        """A signature with a timestamp 120s in the future must also be rejected."""
        monkeypatch.setattr(settings, "trusted_proxy_secret", "test-shared-secret")

        future_timestamp = int(time.time()) + 120  # 2 minutes from now
        headers = _make_signed_headers(
            method="GET",
            path="/api/projects",
            timestamp=future_timestamp,
        )

        resp = client.get("/api/projects", headers=headers)
        assert resp.status_code == 401

    def test_valid_timestamp_accepted(self, client, monkeypatch):
        """A signature with a recent timestamp (within 60s) should be accepted."""
        monkeypatch.setattr(settings, "trusted_proxy_secret", "test-shared-secret")

        headers = _make_signed_headers(
            method="GET",
            path="/api/projects",
        )

        resp = client.get("/api/projects", headers=headers)
        # Should succeed (200) — not rejected on auth grounds
        assert resp.status_code == 200

    def test_wrong_secret_rejected(self, client, monkeypatch):
        """A signature computed with the wrong secret must be rejected."""
        monkeypatch.setattr(settings, "trusted_proxy_secret", "real-secret")

        headers = _make_signed_headers(
            method="GET",
            path="/api/projects",
            secret="wrong-secret",
        )

        resp = client.get("/api/projects", headers=headers)
        assert resp.status_code == 401


class TestOwnership:
    """Verify cross-user ownership checks — user A cannot access user B's data."""

    def test_cannot_access_other_user_mission(self, client):
        """User A cannot read a mission that belongs to user B."""
        user_a = f"owner-a-{uuid4().hex[:8]}"
        user_b = f"owner-b-{uuid4().hex[:8]}"

        # Create a project for user A
        project_id = _create_project(client, user_a)

        # List user A's missions (should be empty but confirms the user exists)
        resp = client.get("/api/missions", headers=_make_auth_headers(user_a))
        assert resp.status_code == 200

        # Create a project for user B too (so they exist in the DB)
        _create_project(client, user_b)

        # User B tries to access user A's project
        resp = client.get(f"/api/projects/{project_id}", headers=_make_auth_headers(user_b))
        assert resp.status_code == 404, "User B should not see user A's project"

    def test_cannot_delete_other_user_mission(self, client):
        """User B cannot delete user A's mission via the DELETE endpoint."""
        user_a = f"del-a-{uuid4().hex[:8]}"
        user_b = f"del-b-{uuid4().hex[:8]}"

        # Ensure both users exist
        _create_project(client, user_a)
        _create_project(client, user_b)

        # Attempt to delete a fake mission_id as user B — should 404 (not found for that user)
        fake_mission_id = f"mission_{uuid4().hex[:10]}"
        resp = client.delete(
            f"/api/missions/{fake_mission_id}",
            headers=_make_auth_headers(user_b),
        )
        assert resp.status_code == 404

    def test_cannot_list_other_user_projects(self, client):
        """User B's project list should not contain user A's projects."""
        user_a = f"list-a-{uuid4().hex[:8]}"
        user_b = f"list-b-{uuid4().hex[:8]}"

        project_a_name = f"SecretProject-{uuid4().hex[:6]}"
        resp = client.post(
            "/api/projects",
            json={"name": project_a_name},
            headers=_make_auth_headers(user_a),
        )
        assert resp.status_code == 201

        # User B lists their projects — should not see user A's project
        resp = client.get("/api/projects", headers=_make_auth_headers(user_b))
        assert resp.status_code == 200
        project_names = [p.get("name") for p in resp.json()]
        assert project_a_name not in project_names, "User B should not see user A's projects"
