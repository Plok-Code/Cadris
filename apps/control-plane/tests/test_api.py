"""Tests for the control-plane API contracts."""
from __future__ import annotations


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_create_project_requires_auth(client):
    response = client.post("/api/projects", json={"name": "Test auth"})
    assert response.status_code == 401


def test_create_project(client, auth_headers):
    response = client.post(
        "/api/projects",
        json={"name": "Mon Super Projet"},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == "Mon Super Projet"


def test_list_projects(client, auth_headers):
    client.post("/api/projects", json={"name": "Projet A"}, headers=auth_headers)
    response = client.get("/api/projects", headers=auth_headers)
    assert response.status_code == 200
    projects = response.json()
    assert isinstance(projects, list)
    assert len(projects) >= 1


def test_create_project_name_too_short(client, auth_headers):
    response = client.post(
        "/api/projects",
        json={"name": "AB"},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_get_mission_not_found(client, auth_headers):
    response = client.get("/api/missions/nonexistent", headers=auth_headers)
    assert response.status_code == 404


def test_get_dossier_not_found(client, auth_headers):
    response = client.get("/api/missions/nonexistent/dossier", headers=auth_headers)
    assert response.status_code == 404


def test_get_dossier_pdf_not_found(client, auth_headers):
    response = client.get("/api/missions/nonexistent/dossier/pdf", headers=auth_headers)
    assert response.status_code == 404
