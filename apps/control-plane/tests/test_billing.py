"""Tests for billing API endpoints."""
from __future__ import annotations

from unittest.mock import patch, MagicMock

from cadris_cp.config import settings


class TestBillingPlans:
    def test_get_plans_returns_all_plans(self, client, auth_headers):
        resp = client.get("/api/billing/plans", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert "plans" in data
        assert "current_plan" in data
        plan_names = [p["name"] for p in data["plans"]]
        assert "free" in plan_names
        assert "starter" in plan_names
        assert "pro" in plan_names
        assert "expert" in plan_names

    def test_get_plans_requires_auth(self, client):
        resp = client.get("/api/billing/plans")
        assert resp.status_code == 401

    def test_default_plan_is_free(self, client, auth_headers):
        resp = client.get("/api/billing/plans", headers=auth_headers)
        data = resp.json()
        assert data["current_plan"] == "free"


class TestBillingCheckout:
    def test_checkout_requires_auth(self, client):
        resp = client.post("/api/billing/checkout", json={"plan": "starter"})
        assert resp.status_code == 401

    def test_checkout_invalid_plan(self, client, auth_headers, monkeypatch):
        monkeypatch.setattr(settings, "stripe_secret_key", "sk_test_fake")
        resp = client.post(
            "/api/billing/checkout",
            json={"plan": "nonexistent"},
            headers=auth_headers,
        )
        assert resp.status_code == 422

    def test_checkout_free_plan_rejected(self, client, auth_headers, monkeypatch):
        monkeypatch.setattr(settings, "stripe_secret_key", "sk_test_fake")
        resp = client.post(
            "/api/billing/checkout",
            json={"plan": "free"},
            headers=auth_headers,
        )
        assert resp.status_code == 422

    def test_checkout_no_stripe_configured(self, client, auth_headers, monkeypatch):
        monkeypatch.setattr(settings, "stripe_secret_key", None)
        resp = client.post(
            "/api/billing/checkout",
            json={"plan": "starter"},
            headers=auth_headers,
        )
        assert resp.status_code == 500


class TestBillingPortal:
    def test_portal_requires_auth(self, client):
        resp = client.post("/api/billing/portal")
        assert resp.status_code == 401

    def test_portal_no_subscription(self, client, auth_headers, monkeypatch):
        monkeypatch.setattr(settings, "stripe_secret_key", "sk_test_fake")
        resp = client.post("/api/billing/portal", headers=auth_headers)
        assert resp.status_code == 422


class TestMissionLimit:
    def test_free_plan_check(self):
        from cadris_cp.billing import check_mission_limit, PLANS
        from unittest.mock import MagicMock

        user = MagicMock()
        user.plan = "free"
        user.missions_this_month = 0
        assert check_mission_limit(user) is True

        user.missions_this_month = 1
        assert check_mission_limit(user) is False

    def test_pro_plan_limit(self):
        from cadris_cp.billing import check_mission_limit

        user = MagicMock()
        user.plan = "pro"
        user.missions_this_month = 9
        assert check_mission_limit(user) is True

        user.missions_this_month = 10
        assert check_mission_limit(user) is False
