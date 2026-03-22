"""Tests for exception handlers — verify error envelopes and information hiding.

Uses the FastAPI TestClient from conftest to trigger real handler invocations
through the application's exception handler chain.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from cadris_cp.errors import AppError


# ---------------------------------------------------------------------------
# validation_exception_handler
# ---------------------------------------------------------------------------

class TestValidationExceptionHandler:
    """Pydantic validation errors must return field-level messages, not raw schema."""

    def test_returns_field_level_errors(self, client, auth_headers):
        """Sending invalid data triggers validation with structured field errors."""
        # name is required and min_length=3 — send a 2-char name
        resp = client.post(
            "/api/projects",
            json={"name": "AB"},
            headers=auth_headers,
        )
        assert resp.status_code == 422
        body = resp.json()

        assert body["code"] == "validation_error"
        assert body["category"] == "validation"
        assert body["retryable"] is False
        assert "details" in body
        assert "errors" in body["details"]

        errors = body["details"]["errors"]
        assert isinstance(errors, list)
        assert len(errors) >= 1

        # Each error should have "field" and "message", NOT raw Pydantic "ctx", "type", "url"
        for err in errors:
            assert "field" in err
            assert "message" in err
            assert "ctx" not in err, "Raw Pydantic context must not leak"
            assert "type" not in err, "Raw Pydantic error type must not leak"
            assert "url" not in err, "Pydantic docs URL must not leak"

    def test_missing_required_field(self, client, auth_headers):
        """Missing a required field yields a validation error envelope."""
        resp = client.post(
            "/api/projects",
            json={},
            headers=auth_headers,
        )
        assert resp.status_code == 422
        body = resp.json()
        assert body["code"] == "validation_error"
        assert body["message"] == "Requete invalide."

    def test_field_too_long(self, client, auth_headers):
        """Exceeding max_length on a field triggers validation."""
        resp = client.post(
            "/api/projects",
            json={"name": "A" * 200},  # max_length=120
            headers=auth_headers,
        )
        assert resp.status_code == 422
        body = resp.json()
        assert body["code"] == "validation_error"
        errors = body["details"]["errors"]
        # At least one error should reference the name field
        field_names = [e["field"] for e in errors]
        assert any("name" in f for f in field_names)

    def test_envelope_has_request_id(self, client, auth_headers):
        """All error envelopes include a request_id."""
        resp = client.post(
            "/api/projects",
            json={"name": "AB"},
            headers=auth_headers,
        )
        body = resp.json()
        assert "requestId" in body or "request_id" in body


# ---------------------------------------------------------------------------
# app_error_handler — AppError exceptions
# ---------------------------------------------------------------------------

class TestAppErrorHandler:
    """AppError raised in endpoints must produce the correct envelope."""

    def test_not_found_envelope(self, client, auth_headers):
        """A 404 from a non-existent resource returns a proper envelope."""
        resp = client.get("/api/missions/nonexistent-id-xyz", headers=auth_headers)
        assert resp.status_code == 404
        body = resp.json()

        assert body.get("code") is not None
        assert body.get("message") is not None
        assert body.get("retryable") is False
        # Must NOT contain a Python traceback
        assert "Traceback" not in str(body)

    def test_unauthorized_envelope(self, client):
        """Missing auth produces a 401 with an auth-category envelope."""
        resp = client.get("/api/projects")
        assert resp.status_code == 401
        body = resp.json()

        assert body["code"] in ("unauthorized", "http_error")
        assert "Traceback" not in str(body)

    def test_envelope_structure(self, client, auth_headers):
        """Verify the exact fields present in an error envelope."""
        resp = client.get("/api/missions/does-not-exist", headers=auth_headers)
        body = resp.json()

        # Required envelope fields (camelCase due to alias_generator)
        for key in ("code", "category", "retryable", "message"):
            assert key in body, f"Missing envelope field: {key}"

    def test_checkout_validation_error_envelope(self, client, auth_headers, monkeypatch):
        """Business-logic validation (invalid plan) returns a proper envelope."""
        from cadris_cp.config import settings as cfg
        monkeypatch.setattr(cfg, "stripe_secret_key", "sk_test_fake")

        resp = client.post(
            "/api/billing/checkout",
            json={"plan": "free"},
            headers=auth_headers,
        )
        assert resp.status_code == 422
        body = resp.json()
        assert body.get("code") is not None
        assert body.get("message") is not None


# ---------------------------------------------------------------------------
# unhandled_exception_handler — must never leak internals
# ---------------------------------------------------------------------------

class TestUnhandledExceptionHandler:
    """The 500 handler must return a generic message, never exception details."""

    def test_generic_500_message(self, client, auth_headers):
        """Trigger a 500 via a known broken path and verify no leak."""
        # We can't easily trigger a 500 from the test client without monkeypatching
        # an endpoint. Instead, we verify the handler shape directly.
        from cadris_cp.exception_handlers import unhandled_exception_handler
        from cadris_cp.request_context import set_request_id
        from unittest.mock import MagicMock
        import asyncio

        set_request_id("req_test_500")
        request = MagicMock()
        exc = RuntimeError("super secret database password in error")

        response = asyncio.get_event_loop().run_until_complete(
            unhandled_exception_handler(request, exc)
        )

        assert response.status_code == 500
        import json
        body = json.loads(response.body)

        assert body["code"] == "internal_error"
        assert body["category"] == "internal"
        assert body["message"] == "Erreur interne."
        # Must NOT contain the exception message
        assert "secret" not in str(body).lower()
        assert "password" not in str(body).lower()
        assert "database" not in str(body).lower()
        assert "RuntimeError" not in str(body)

    def test_500_has_request_id(self):
        """The 500 response includes the request_id for correlation."""
        from cadris_cp.exception_handlers import unhandled_exception_handler
        from cadris_cp.request_context import set_request_id
        from unittest.mock import MagicMock
        import asyncio
        import json

        set_request_id("req_correlation_test")
        request = MagicMock()
        exc = ValueError("leaked info")

        response = asyncio.get_event_loop().run_until_complete(
            unhandled_exception_handler(request, exc)
        )

        body = json.loads(response.body)
        request_id = body.get("requestId") or body.get("request_id")
        assert request_id == "req_correlation_test"

    def test_500_is_not_retryable(self):
        """Unhandled exceptions are not marked as retryable."""
        from cadris_cp.exception_handlers import unhandled_exception_handler
        from cadris_cp.request_context import set_request_id
        from unittest.mock import MagicMock
        import asyncio
        import json

        set_request_id("req_retry_check")
        request = MagicMock()
        exc = Exception("crash")

        response = asyncio.get_event_loop().run_until_complete(
            unhandled_exception_handler(request, exc)
        )

        body = json.loads(response.body)
        assert body["retryable"] is False


# ---------------------------------------------------------------------------
# http_exception_handler — standard HTTP errors
# ---------------------------------------------------------------------------

class TestHttpExceptionHandler:
    """FastAPI/Starlette HTTPException must be wrapped in the envelope format."""

    def test_404_via_unknown_route(self, client):
        """Hitting a non-existent route returns an envelope (not raw Starlette)."""
        resp = client.get("/api/this-route-does-not-exist-xyz")
        assert resp.status_code in (404, 405)
        body = resp.json()

        # Should have our envelope structure, not raw Starlette {"detail": "..."}
        assert "code" in body
        assert "message" in body

    def test_401_has_correct_category(self, client):
        """401 responses get category='auth'."""
        resp = client.get("/api/projects")
        assert resp.status_code == 401
        body = resp.json()
        assert body.get("category") == "auth"
