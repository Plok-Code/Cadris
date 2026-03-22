"""Tests for the typed error classification module."""

import asyncio
import json

import httpx
import pytest
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
)
from pydantic import ValidationError, BaseModel

from cadris_runtime.error_classification import is_json_error, is_permanent, is_retryable


# ── Helpers ──────────────────────────────────────────────────────

def _make_api_status_error(status: int, message: str = "error") -> APIStatusError:
    """Create a mock APIStatusError with the given status code."""
    response = httpx.Response(status, request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"))
    return APIStatusError(message=message, response=response, body=None)


def _make_rate_limit_error(message: str = "Rate limit exceeded") -> RateLimitError:
    response = httpx.Response(429, request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"))
    return RateLimitError(message=message, response=response, body=None)


# ── is_permanent ─────────────────────────────────────────────────

class TestIsPermanent:
    def test_authentication_error(self):
        response = httpx.Response(401, request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"))
        exc = AuthenticationError(message="invalid_api_key", response=response, body=None)
        assert is_permanent(exc) is True

    def test_bad_request_error(self):
        response = httpx.Response(400, request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"))
        exc = BadRequestError(message="invalid request", response=response, body=None)
        assert is_permanent(exc) is True

    def test_rate_limit_with_quota(self):
        exc = _make_rate_limit_error("insufficient_quota: you have exceeded your billing limit")
        assert is_permanent(exc) is True

    def test_rate_limit_transient(self):
        exc = _make_rate_limit_error("Rate limit exceeded, please retry")
        assert is_permanent(exc) is False

    def test_connection_error(self):
        exc = APIConnectionError(request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"))
        assert is_permanent(exc) is False

    def test_generic_exception(self):
        assert is_permanent(Exception("something random")) is False


# ── is_json_error ────────────────────────────────────────────────

class TestIsJsonError:
    def test_json_decode_error(self):
        exc = json.JSONDecodeError("Expecting value", "", 0)
        assert is_json_error(exc) is True

    def test_pydantic_validation_error(self):
        class M(BaseModel):
            x: int
        try:
            M(x="not_a_number")  # type: ignore[arg-type]
        except ValidationError as exc:
            assert is_json_error(exc) is True

    def test_value_error_with_json_message(self):
        exc = ValueError("invalid json in response")
        assert is_json_error(exc) is True

    def test_generic_value_error(self):
        exc = ValueError("something else entirely")
        assert is_json_error(exc) is False

    def test_random_exception(self):
        assert is_json_error(Exception("timeout")) is False


# ── is_retryable ─────────────────────────────────────────────────

class TestIsRetryable:
    def test_connection_error(self):
        exc = APIConnectionError(request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"))
        assert is_retryable(exc) is True

    def test_timeout_error(self):
        exc = APITimeoutError(request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"))
        assert is_retryable(exc) is True

    def test_asyncio_timeout(self):
        exc = asyncio.TimeoutError()
        assert is_retryable(exc) is True

    def test_rate_limit_transient(self):
        exc = _make_rate_limit_error("Rate limit exceeded")
        assert is_retryable(exc) is True

    def test_rate_limit_quota_not_retryable(self):
        exc = _make_rate_limit_error("insufficient_quota")
        assert is_retryable(exc) is False

    def test_server_error_502(self):
        exc = _make_api_status_error(502)
        assert is_retryable(exc) is True

    def test_server_error_503(self):
        exc = _make_api_status_error(503)
        assert is_retryable(exc) is True

    def test_server_error_529(self):
        exc = _make_api_status_error(529)
        assert is_retryable(exc) is True

    def test_client_error_404_not_retryable(self):
        exc = _make_api_status_error(404)
        assert is_retryable(exc) is False

    def test_json_error_is_retryable(self):
        exc = json.JSONDecodeError("Expecting value", "", 0)
        assert is_retryable(exc) is True

    def test_auth_error_not_retryable(self):
        response = httpx.Response(401, request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"))
        exc = AuthenticationError(message="invalid key", response=response, body=None)
        assert is_retryable(exc) is False

    def test_bad_request_not_retryable(self):
        response = httpx.Response(400, request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"))
        exc = BadRequestError(message="bad request", response=response, body=None)
        assert is_retryable(exc) is False

    def test_httpx_connect_error(self):
        exc = httpx.ConnectError("Connection refused")
        assert is_retryable(exc) is True

    def test_httpx_timeout(self):
        exc = httpx.TimeoutException("Read timed out")
        assert is_retryable(exc) is True

    def test_generic_exception_not_retryable(self):
        assert is_retryable(Exception("unknown error")) is False
