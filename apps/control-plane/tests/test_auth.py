from __future__ import annotations

import time

from cadris_cp.auth import build_trusted_proxy_signature
from cadris_cp.config import settings


def _signed_headers(*, method: str, path: str, user_id: str = "test-user", user_email: str = "test@example.com") -> dict[str, str]:
    timestamp = str(int(time.time()))
    signature = build_trusted_proxy_signature(
        secret="test-shared-secret",
        timestamp=timestamp,
        method=method,
        path=path,
        user_id=user_id,
        user_email=user_email,
    )
    return {
        "x-cadris-user-id": user_id,
        "x-cadris-user-email": user_email,
        "x-cadris-auth-timestamp": timestamp,
        "x-cadris-auth-signature": signature,
    }


def test_unsigned_request_rejected_when_trusted_proxy_secret_enabled(client, monkeypatch):
    monkeypatch.setattr(settings, "trusted_proxy_secret", "test-shared-secret")

    response = client.get("/api/projects", headers={"x-cadris-user-id": "test-user"})

    assert response.status_code == 401


def test_signed_request_allowed_when_trusted_proxy_secret_enabled(client, monkeypatch):
    monkeypatch.setattr(settings, "trusted_proxy_secret", "test-shared-secret")

    response = client.post(
        "/api/projects",
        json={"name": "Projet securise"},
        headers=_signed_headers(method="POST", path="/api/projects"),
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Projet securise"
