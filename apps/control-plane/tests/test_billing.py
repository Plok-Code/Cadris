"""Tests for billing logic — mission limits, monthly resets, plan resolution.

Uses SQLite in-memory DB via conftest fixtures for tests that need a real
UserRecord, and plain MagicMock for pure-logic tests.
"""
from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.orm import Session

from cadris_cp.billing import (
    PLANS,
    _plan_from_price,
    _reset_monthly_counter_if_needed,
    check_and_increment_mission,
    check_mission_limit,
)
from cadris_cp.config import settings


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_user(**overrides) -> MagicMock:
    """Create a fake UserRecord with sensible defaults."""
    user = MagicMock()
    user.plan = overrides.get("plan", "free")
    user.missions_this_month = overrides.get("missions_this_month", 0)
    user.month_reset_at = overrides.get("month_reset_at", None)
    return user


def _make_db() -> MagicMock:
    """Create a fake DB session."""
    return MagicMock(spec=Session)


# ---------------------------------------------------------------------------
# _plan_from_price
# ---------------------------------------------------------------------------

class TestPlanFromPrice:
    def test_known_starter_price(self):
        """Known price ID resolves to correct plan."""
        price_id = settings.stripe_price_starter
        if price_id:
            assert _plan_from_price(price_id) == "starter"

    def test_known_pro_price(self):
        price_id = settings.stripe_price_pro
        if price_id:
            assert _plan_from_price(price_id) == "pro"

    def test_known_expert_price(self):
        price_id = settings.stripe_price_expert
        if price_id:
            assert _plan_from_price(price_id) == "expert"

    def test_unknown_price_returns_free(self):
        """An unknown Stripe price ID must default to 'free', not 'pro'."""
        result = _plan_from_price("price_UNKNOWN_12345")
        assert result == "free"

    def test_empty_string_returns_free(self):
        result = _plan_from_price("")
        assert result == "free"

    def test_none_like_value_returns_free(self):
        """None-ish strings should still resolve to free."""
        result = _plan_from_price("null")
        assert result == "free"


# ---------------------------------------------------------------------------
# _reset_monthly_counter_if_needed
# ---------------------------------------------------------------------------

class TestResetMonthlyCounter:
    def test_no_prior_reset_sets_timestamp(self):
        """First call (month_reset_at=None) just sets the timestamp."""
        user = _make_user(missions_this_month=3, month_reset_at=None)
        now = datetime(2026, 3, 15, 12, 0, 0, tzinfo=UTC)

        _reset_monthly_counter_if_needed(user, now)

        # Counter should NOT be reset — this is the initial set
        assert user.missions_this_month == 3
        assert user.month_reset_at == now.isoformat()

    def test_same_month_no_reset(self):
        """Within the same month, counter stays untouched."""
        user = _make_user(
            missions_this_month=5,
            month_reset_at=datetime(2026, 3, 1, 0, 0, 0, tzinfo=UTC).isoformat(),
        )
        now = datetime(2026, 3, 20, 14, 30, 0, tzinfo=UTC)

        _reset_monthly_counter_if_needed(user, now)

        assert user.missions_this_month == 5

    def test_new_month_resets_counter(self):
        """Crossing into a new calendar month resets the counter to 0."""
        user = _make_user(
            missions_this_month=7,
            month_reset_at=datetime(2026, 2, 15, 10, 0, 0, tzinfo=UTC).isoformat(),
        )
        now = datetime(2026, 3, 1, 0, 0, 1, tzinfo=UTC)

        _reset_monthly_counter_if_needed(user, now)

        assert user.missions_this_month == 0
        assert user.month_reset_at == now.isoformat()

    def test_year_boundary_resets_counter(self):
        """December -> January triggers a reset (year boundary)."""
        user = _make_user(
            missions_this_month=10,
            month_reset_at=datetime(2025, 12, 28, 23, 0, 0, tzinfo=UTC).isoformat(),
        )
        now = datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)

        _reset_monthly_counter_if_needed(user, now)

        assert user.missions_this_month == 0

    def test_corrupt_month_reset_at_resets_gracefully(self):
        """Invalid month_reset_at string resets counter gracefully."""
        user = _make_user(
            missions_this_month=4,
            month_reset_at="not-a-valid-date",
        )
        now = datetime(2026, 3, 15, 12, 0, 0, tzinfo=UTC)

        _reset_monthly_counter_if_needed(user, now)

        # Should reset because parsing fails -> except branch
        assert user.missions_this_month == 0
        assert user.month_reset_at == now.isoformat()

    def test_same_month_different_day_no_reset(self):
        """March 1 -> March 31 is same month, no reset."""
        user = _make_user(
            missions_this_month=2,
            month_reset_at=datetime(2026, 3, 1, 0, 0, 0, tzinfo=UTC).isoformat(),
        )
        now = datetime(2026, 3, 31, 23, 59, 59, tzinfo=UTC)

        _reset_monthly_counter_if_needed(user, now)

        assert user.missions_this_month == 2


# ---------------------------------------------------------------------------
# check_mission_limit — plan caps
# ---------------------------------------------------------------------------

class TestCheckMissionLimit:
    @pytest.mark.parametrize(
        "plan,limit",
        [
            ("free", 1),
            ("starter", 5),
            ("pro", 10),
            ("expert", 20),
        ],
    )
    def test_plan_limits(self, plan: str, limit: int):
        """Each plan has a specific mission cap."""
        user = _make_user(plan=plan, missions_this_month=0)
        assert check_mission_limit(user) is True

        user.missions_this_month = limit - 1
        assert check_mission_limit(user) is True

        user.missions_this_month = limit
        assert check_mission_limit(user) is False

    def test_unknown_plan_falls_back_to_free(self):
        """Unknown plan names get the free limit (1)."""
        user = _make_user(plan="nonexistent", missions_this_month=0)
        assert check_mission_limit(user) is True

        user.missions_this_month = 1
        assert check_mission_limit(user) is False

    def test_check_with_db_commits(self):
        """When a DB session is passed, check_mission_limit commits."""
        db = _make_db()
        user = _make_user(plan="free", missions_this_month=0)
        check_mission_limit(user, db=db)
        db.commit.assert_called()

    def test_check_without_db_does_not_crash(self):
        """When no DB session is passed, it still works."""
        user = _make_user(plan="free", missions_this_month=0)
        result = check_mission_limit(user)
        assert result is True


# ---------------------------------------------------------------------------
# check_and_increment_mission — atomic check + increment
# ---------------------------------------------------------------------------

class TestCheckAndIncrementMission:
    def test_allowed_increments_counter(self):
        """Under the limit: returns True and increments."""
        user = _make_user(plan="free", missions_this_month=0)
        db = _make_db()

        result = check_and_increment_mission(user, db)

        assert result is True
        assert user.missions_this_month == 1
        db.commit.assert_called()

    def test_at_limit_returns_false_no_increment(self):
        """At the limit: returns False and does NOT increment."""
        user = _make_user(plan="free", missions_this_month=1)
        db = _make_db()

        result = check_and_increment_mission(user, db)

        assert result is False
        assert user.missions_this_month == 1

    def test_starter_limit(self):
        """Starter plan allows 5 missions."""
        db = _make_db()

        # Mission 5 should be allowed (0..4 already done)
        user = _make_user(plan="starter", missions_this_month=4)
        assert check_and_increment_mission(user, db) is True
        assert user.missions_this_month == 5

        # Mission 6 should be blocked
        assert check_and_increment_mission(user, db) is False
        assert user.missions_this_month == 5

    def test_pro_limit(self):
        """Pro plan allows 10 missions."""
        db = _make_db()
        user = _make_user(plan="pro", missions_this_month=9)
        assert check_and_increment_mission(user, db) is True
        assert user.missions_this_month == 10

        assert check_and_increment_mission(user, db) is False
        assert user.missions_this_month == 10

    def test_expert_limit(self):
        """Expert plan allows 20 missions."""
        db = _make_db()
        user = _make_user(plan="expert", missions_this_month=19)
        assert check_and_increment_mission(user, db) is True
        assert user.missions_this_month == 20

        assert check_and_increment_mission(user, db) is False
        assert user.missions_this_month == 20

    def test_resets_month_then_allows(self):
        """If month boundary is crossed, reset counter first, then allow."""
        db = _make_db()
        user = _make_user(
            plan="free",
            missions_this_month=1,
            month_reset_at=datetime(2026, 2, 15, tzinfo=UTC).isoformat(),
        )

        # Patch datetime.now to be March
        with patch("cadris_cp.billing.datetime") as mock_dt:
            mock_dt.now.return_value = datetime(2026, 3, 5, 12, 0, 0, tzinfo=UTC)
            mock_dt.fromisoformat = datetime.fromisoformat
            mock_dt.side_effect = lambda *a, **kw: datetime(*a, **kw)
            result = check_and_increment_mission(user, db)

        assert result is True
        assert user.missions_this_month == 1  # reset to 0 then +1

    def test_unknown_plan_uses_free_limit(self):
        """Unknown plan falls back to free (1 mission/month)."""
        db = _make_db()
        user = _make_user(plan="legacy_beta", missions_this_month=0)
        assert check_and_increment_mission(user, db) is True
        assert user.missions_this_month == 1

        assert check_and_increment_mission(user, db) is False

    def test_commit_called_only_on_success(self):
        """DB commit happens only when mission is allowed."""
        db = _make_db()

        # Allowed
        user = _make_user(plan="free", missions_this_month=0)
        check_and_increment_mission(user, db)
        assert db.commit.call_count >= 1

        db.reset_mock()

        # Denied
        user = _make_user(plan="free", missions_this_month=1)
        check_and_increment_mission(user, db)
        # commit should NOT be called when denied
        db.commit.assert_not_called()


# ---------------------------------------------------------------------------
# PLANS constant sanity checks
# ---------------------------------------------------------------------------

class TestPlansConstant:
    def test_all_plan_names_exist(self):
        assert set(PLANS.keys()) == {"free", "starter", "pro", "expert"}

    def test_free_has_no_price_id(self):
        assert PLANS["free"]["price_id"] is None

    def test_paid_plans_have_missions_per_month(self):
        for name in ("starter", "pro", "expert"):
            assert PLANS[name]["missions_per_month"] > PLANS["free"]["missions_per_month"]


# ---------------------------------------------------------------------------
# Billing API endpoints (integration via TestClient)
# ---------------------------------------------------------------------------

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
