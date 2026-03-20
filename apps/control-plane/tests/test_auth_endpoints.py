"""Tests for email + password auth endpoints (register, login, forgot-pw, reset-pw)."""
from __future__ import annotations


class TestRegister:
    def test_register_success(self, client):
        resp = client.post("/api/auth/register", json={
            "email": "new@example.com",
            "password": "strongpass123",
            "name": "Test User",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "new@example.com"
        assert data["name"] == "Test User"
        assert "id" in data

    def test_register_duplicate_email(self, client):
        client.post("/api/auth/register", json={
            "email": "dupe@example.com",
            "password": "strongpass123",
        })
        resp = client.post("/api/auth/register", json={
            "email": "dupe@example.com",
            "password": "strongpass123",
        })
        assert resp.status_code == 409

    def test_register_weak_password(self, client):
        resp = client.post("/api/auth/register", json={
            "email": "weak@example.com",
            "password": "short",
        })
        assert resp.status_code == 422

    def test_register_invalid_email(self, client):
        resp = client.post("/api/auth/register", json={
            "email": "not-an-email",
            "password": "strongpass123",
        })
        assert resp.status_code == 422


class TestLogin:
    def _register(self, client, email="login@example.com", password="strongpass123"):
        client.post("/api/auth/register", json={"email": email, "password": password})

    def test_login_success(self, client):
        self._register(client)
        resp = client.post("/api/auth/login", json={
            "email": "login@example.com",
            "password": "strongpass123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "login@example.com"

    def test_login_wrong_password(self, client):
        self._register(client, email="wrong@example.com")
        resp = client.post("/api/auth/login", json={
            "email": "wrong@example.com",
            "password": "wrongpassword",
        })
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        resp = client.post("/api/auth/login", json={
            "email": "ghost@example.com",
            "password": "strongpass123",
        })
        assert resp.status_code == 401


class TestForgotPassword:
    def test_forgot_password_always_succeeds(self, client):
        """Anti-enumeration: always returns success even for nonexistent emails."""
        resp = client.post("/api/auth/forgot-password", json={
            "email": "nonexistent@example.com",
        })
        assert resp.status_code == 200
        assert "message" in resp.json()


class TestResetPassword:
    def test_reset_invalid_token(self, client):
        resp = client.post("/api/auth/reset-password", json={
            "token": "invalid_token_that_doesnt_exist",
            "password": "newstrongpass123",
        })
        assert resp.status_code == 422

    def test_reset_weak_password(self, client):
        resp = client.post("/api/auth/reset-password", json={
            "token": "some_token",
            "password": "short",
        })
        assert resp.status_code == 422
