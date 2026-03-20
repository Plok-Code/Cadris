"""Tests for the Cadris renderer."""
from __future__ import annotations

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

SAMPLE_PAYLOAD = {
    "title": "Dossier Test",
    "summary": "Un dossier de test pour valider le renderer.",
    "sections": [
        {
            "id": "vision",
            "title": "Vision produit",
            "content": "Cadris aide les createurs de projets a structurer leur cadrage.",
            "certainty": "solid",
        },
        {
            "id": "mvp",
            "title": "Boucle MVP",
            "content": "La V1 couvre mission, question, reponse et dossier markdown.",
            "certainty": "to_confirm",
        },
    ],
}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["ok"] is True


def test_render_markdown():
    response = client.post("/internal/renderer/markdown", json=SAMPLE_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert "markdown" in data
    assert "# Dossier Test" in data["markdown"]
    assert "## Vision produit" in data["markdown"]


def test_render_html():
    response = client.post("/internal/renderer/html", json=SAMPLE_PAYLOAD)
    assert response.status_code == 200
    data = response.json()
    assert "html" in data
    assert "<h1>Dossier Test</h1>" in data["html"]
    assert "certainty-solid" in data["html"]


def test_render_html_sanitizes_embedded_html():
    payload = {
        **SAMPLE_PAYLOAD,
        "sections": [
            {
                "id": "security",
                "title": "Security",
                "content": "<script>alert('xss')</script>**Texte sur** [Lien](javascript:alert(1))",
                "certainty": "solid",
            }
        ],
    }

    response = client.post("/internal/renderer/html", json=payload)

    assert response.status_code == 200
    html = response.json()["html"].lower()
    assert "<script" not in html
    assert "javascript:alert" not in html
    assert "<strong>texte sur</strong>" in html


def test_render_pdf():
    response = client.post("/internal/renderer/pdf", json=SAMPLE_PAYLOAD)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    # PDF files start with %PDF
    assert response.content[:5] == b"%PDF-"
