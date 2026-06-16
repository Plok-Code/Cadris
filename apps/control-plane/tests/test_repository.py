"""Repository ownership-filter unit tests (cov-db-ownership-01).

The get_*_for_user() methods are the last line of defense against cross-user
data leaks. Here we exercise them directly (not just via API integration) so a
regression in a WHERE clause is caught at the source.
"""
from __future__ import annotations

from uuid import uuid4

from cadris_cp.repository import ControlPlaneRepository

from .conftest import _TestSession


def _headers(user_id: str) -> dict[str, str]:
    return {"x-cadris-user-id": user_id}


def _create_project(client, user_id: str, name: str = "Projet") -> str:
    resp = client.post("/api/projects", json={"name": name}, headers=_headers(user_id))
    assert resp.status_code == 201
    return resp.json()["id"]


class TestProjectOwnership:
    def test_owner_can_load_own_project(self, client):
        owner = f"repo-own-{uuid4().hex[:8]}"
        project_id = _create_project(client, owner)
        with _TestSession() as session:
            repo = ControlPlaneRepository(session)
            project = repo.get_project_for_user(owner, project_id)
            assert project is not None
            assert project.id == project_id

    def test_other_user_cannot_load_project(self, client):
        owner = f"repo-a-{uuid4().hex[:8]}"
        other = f"repo-b-{uuid4().hex[:8]}"
        project_id = _create_project(client, owner)
        _create_project(client, other)  # ensure 'other' exists in the DB
        with _TestSession() as session:
            repo = ControlPlaneRepository(session)
            assert repo.get_project_for_user(other, project_id) is None

    def test_unknown_project_returns_none(self, client):
        user = f"repo-u-{uuid4().hex[:8]}"
        _create_project(client, user)
        with _TestSession() as session:
            repo = ControlPlaneRepository(session)
            assert repo.get_project_for_user(user, "project_does_not_exist") is None


class TestMissionOwnership:
    def test_other_user_cannot_load_mission(self, client):
        # No mission exists; the filter must still not leak across users.
        owner = f"repo-m-a-{uuid4().hex[:8]}"
        other = f"repo-m-b-{uuid4().hex[:8]}"
        _create_project(client, owner)
        _create_project(client, other)
        with _TestSession() as session:
            repo = ControlPlaneRepository(session)
            assert repo.get_mission_for_user(other, "mission_whatever") is None
