"""Classify exceptions from LLM providers by type instead of string matching.

This module replaces the fragile `"timeout" in str(exc).lower()` pattern
with proper exception type checks. Works for both OpenAI and Together AI
(which uses the OpenAI-compatible client).

Scaling note: add new exception types here as we integrate new providers.
"""

from __future__ import annotations

import asyncio
import json

import httpx
from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
)
from pydantic import ValidationError

# ── Permanent errors (no point retrying) ────────────────────────

_PERMANENT_EXCEPTIONS = (
    AuthenticationError,  # invalid_api_key
    BadRequestError,  # invalid_request, malformed prompt
)


def is_permanent(exc: Exception) -> bool:
    """Return True if this error will never succeed on retry."""
    if isinstance(exc, _PERMANENT_EXCEPTIONS):
        return True
    # RateLimitError with "insufficient_quota" means billing issue, not transient
    if isinstance(exc, RateLimitError):
        msg = str(exc).lower()
        return "insufficient_quota" in msg or "billing" in msg
    return False


# ── JSON / validation errors (retry with shorter prompt) ────────

_JSON_EXCEPTIONS = (
    json.JSONDecodeError,
    ValidationError,
)


def is_json_error(exc: Exception) -> bool:
    """Return True if this is a JSON parsing or Pydantic validation error."""
    if isinstance(exc, _JSON_EXCEPTIONS):
        return True
    # Some providers wrap JSON errors in APIStatusError or generic Exception
    if isinstance(exc, (APIStatusError, ValueError)):
        msg = str(exc).lower()
        return any(k in msg for k in (
            "invalid json", "json_invalid", "eof while parsing",
            "expected value", "unterminated string",
        ))
    return False


# ── Retryable errors (transient, will likely succeed on retry) ──

_RETRYABLE_EXCEPTIONS = (
    APIConnectionError,  # network issues
    APITimeoutError,  # timeout
    RateLimitError,  # rate limit (non-quota)
    httpx.ConnectError,
    httpx.NetworkError,
    httpx.TimeoutException,
    asyncio.TimeoutError,
    ConnectionError,
    TimeoutError,
)


def is_retryable(exc: Exception) -> bool:
    """Return True if this is a transient error worth retrying."""
    if is_permanent(exc):
        return False
    if is_json_error(exc):
        return True  # JSON errors are retryable with modified prompt
    if isinstance(exc, _RETRYABLE_EXCEPTIONS):
        return True
    # APIStatusError with 5xx or 429 status codes
    if isinstance(exc, APIStatusError) and exc.status_code in (429, 500, 502, 503, 529):
        return True
    # httpx HTTPStatusError with server errors
    if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code >= 500:
        return True
    return False
