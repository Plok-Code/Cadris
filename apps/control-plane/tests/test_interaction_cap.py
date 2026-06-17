"""Server-side per-mission interaction cap — abuse / cost ceiling.

A single (fixed-price) mission must not be loopable to run up our LLM cost.
The UI caps corrections at 3/block for normal users; this is the server-side
backstop that counts every resume round-trip and blocks past the ceiling.
"""
from __future__ import annotations

from uuid import uuid4

import pytest

from cadris_cp.errors import AppError
from cadris_cp.records import MissionRecord, ProjectRecord, UserRecord
from cadris_cp.routers.missions import (
    MAX_MISSION_INTERACTIONS,
    _enforce_interaction_cap,
)

from .conftest import _TestSession


def _seed_mission(user_id: str, interaction_count: int) -> str:
    mission_id = f"mission_{uuid4().hex[:8]}"
    project_id = f"project_{uuid4().hex[:8]}"
    with _TestSession() as session:
        session.add(UserRecord(id=user_id, email=f"{user_id}@dev.local"))
        session.add(ProjectRecord(id=project_id, user_id=user_id, name="P"))
        session.add(
            MissionRecord(
                id=mission_id,
                project_id=project_id,
                title="M",
                status="waiting_user",
                summary="s",
                next_step="n",
                intake_text="x",
                timeline_json="[]",
                interaction_count=interaction_count,
            )
        )
        session.commit()
    return mission_id


class TestInteractionCapEndpoint:
    def test_resume_blocked_at_cap(self, client):
        user_id = f"cap-{uuid4().hex[:8]}"
        mission_id = _seed_mission(user_id, MAX_MISSION_INTERACTIONS)
        resp = client.post(
            f"/api/missions/{mission_id}/resume",
            json={"action": "next_wave"},
            headers={"x-cadris-user-id": user_id},
        )
        assert resp.status_code == 403


class TestInteractionCapHelper:
    def test_increments_below_cap(self):
        user_id = f"cap-inc-{uuid4().hex[:8]}"
        mission_id = _seed_mission(user_id, 0)
        with _TestSession() as session:
            _enforce_interaction_cap(session, mission_id)
            record = session.get(MissionRecord, mission_id)
            assert record.interaction_count == 1

    def test_raises_at_cap(self):
        user_id = f"cap-max-{uuid4().hex[:8]}"
        mission_id = _seed_mission(user_id, MAX_MISSION_INTERACTIONS)
        with _TestSession() as session:
            with pytest.raises(AppError):
                _enforce_interaction_cap(session, mission_id)
