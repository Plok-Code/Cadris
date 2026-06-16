"""Billing tests against a REAL SQLite session + UserRecord (cov-billing-race-01).

The existing billing tests use MagicMock and never exercise the real
check_and_increment_mission code path (SELECT ... FOR UPDATE falls back to the
ORM object on SQLite). These tests drive the actual ORM object and assert the
free-plan limit holds and the monthly counter resets — without double counting.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from cadris_cp.billing import check_and_increment_mission
from cadris_cp.records import UserRecord

from .conftest import _TestSession


def _new_free_user(session, **overrides) -> UserRecord:
    user = UserRecord(
        id=f"bill-{uuid4().hex[:8]}",
        email=f"{uuid4().hex[:8]}@dev.local",
        plan=overrides.get("plan", "free"),
        missions_this_month=overrides.get("missions_this_month", 0),
        month_reset_at=overrides.get("month_reset_at", datetime.now(UTC).isoformat()),
    )
    session.add(user)
    session.commit()
    return user


class TestRealSessionMissionLimit:
    def test_free_user_limit_enforced(self):
        with _TestSession() as session:
            user = _new_free_user(session)
            assert check_and_increment_mission(user, session) is True   # 1st allowed
            assert check_and_increment_mission(user, session) is False  # limit reached
            session.refresh(user)
            assert user.missions_this_month == 1  # never double-counted

    def test_counter_resets_on_new_month(self):
        with _TestSession() as session:
            last_month = (datetime.now(UTC) - timedelta(days=40)).isoformat()
            user = _new_free_user(session, missions_this_month=1, month_reset_at=last_month)
            # We are in a new calendar month → counter resets, this mission is allowed.
            assert check_and_increment_mission(user, session) is True
            session.refresh(user)
            assert user.missions_this_month == 1

    def test_paid_plan_has_higher_limit(self):
        with _TestSession() as session:
            user = _new_free_user(session, plan="starter")  # starter = 5/month
            allowed = sum(1 for _ in range(5) if check_and_increment_mission(user, session))
            assert allowed == 5
            assert check_and_increment_mission(user, session) is False  # 6th blocked
