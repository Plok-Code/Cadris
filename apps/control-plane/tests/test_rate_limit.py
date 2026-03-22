"""Tests for the in-memory sliding-window rate limiter.

All tests manipulate the module-level _buckets dict directly and patch
time.time() for deterministic behaviour — no real clock dependencies.
"""
from __future__ import annotations

from unittest.mock import patch

import pytest

from cadris_cp.rate_limit import (
    MAX_KEYS,
    _SWEEP_INTERVAL,
    _buckets,
    _sweep_stale_keys,
    check_rate_limit,
)
import cadris_cp.rate_limit as rate_limit_mod


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def _clean_buckets():
    """Reset the global rate-limit state before each test."""
    _buckets.clear()
    rate_limit_mod._last_sweep = 0.0
    yield
    _buckets.clear()
    rate_limit_mod._last_sweep = 0.0


# ---------------------------------------------------------------------------
# Basic allow / deny
# ---------------------------------------------------------------------------

class TestBasicBehaviour:
    def test_first_request_allowed(self):
        """A brand-new key is always allowed."""
        with patch("cadris_cp.rate_limit.time") as mock_time:
            mock_time.time.return_value = 1000.0
            assert check_rate_limit("user-1", max_requests=5, window_seconds=60) is True

    def test_requests_within_limit_allowed(self):
        """Multiple requests under the cap are all allowed."""
        with patch("cadris_cp.rate_limit.time") as mock_time:
            mock_time.time.return_value = 1000.0
            for _ in range(5):
                assert check_rate_limit("user-1", max_requests=5, window_seconds=60) is True

    def test_request_exceeding_limit_denied(self):
        """The request that exceeds the cap is denied."""
        with patch("cadris_cp.rate_limit.time") as mock_time:
            mock_time.time.return_value = 1000.0
            for _ in range(5):
                check_rate_limit("user-1", max_requests=5, window_seconds=60)
            assert check_rate_limit("user-1", max_requests=5, window_seconds=60) is False

    def test_different_keys_independent(self):
        """Rate limits are isolated per key."""
        with patch("cadris_cp.rate_limit.time") as mock_time:
            mock_time.time.return_value = 1000.0
            # Exhaust user-1
            for _ in range(3):
                check_rate_limit("user-1", max_requests=3, window_seconds=60)
            assert check_rate_limit("user-1", max_requests=3, window_seconds=60) is False

            # user-2 is unaffected
            assert check_rate_limit("user-2", max_requests=3, window_seconds=60) is True

    def test_single_request_limit(self):
        """max_requests=1 blocks on the second call."""
        with patch("cadris_cp.rate_limit.time") as mock_time:
            mock_time.time.return_value = 1000.0
            assert check_rate_limit("k", max_requests=1, window_seconds=60) is True
            assert check_rate_limit("k", max_requests=1, window_seconds=60) is False


# ---------------------------------------------------------------------------
# Window expiry
# ---------------------------------------------------------------------------

class TestWindowExpiry:
    def test_timestamps_expire_after_window(self):
        """After the window elapses, old timestamps are pruned and new requests allowed."""
        with patch("cadris_cp.rate_limit.time") as mock_time:
            mock_time.time.return_value = 1000.0
            # Fill the bucket
            for _ in range(3):
                check_rate_limit("user-x", max_requests=3, window_seconds=60)
            assert check_rate_limit("user-x", max_requests=3, window_seconds=60) is False

            # Advance time past the window
            mock_time.time.return_value = 1061.0  # 61 seconds later
            assert check_rate_limit("user-x", max_requests=3, window_seconds=60) is True

    def test_partial_window_expiry(self):
        """Only old timestamps expire; recent ones remain counted."""
        with patch("cadris_cp.rate_limit.time") as mock_time:
            # First two requests at t=1000
            mock_time.time.return_value = 1000.0
            check_rate_limit("u", max_requests=3, window_seconds=60)
            check_rate_limit("u", max_requests=3, window_seconds=60)

            # Third request at t=1050 (within window of all)
            mock_time.time.return_value = 1050.0
            check_rate_limit("u", max_requests=3, window_seconds=60)

            # At t=1061: first two expired, third still valid
            # So bucket has 1 entry, 2 more allowed
            mock_time.time.return_value = 1061.0
            assert check_rate_limit("u", max_requests=3, window_seconds=60) is True
            assert check_rate_limit("u", max_requests=3, window_seconds=60) is True
            assert check_rate_limit("u", max_requests=3, window_seconds=60) is False

    def test_exact_boundary_not_expired(self):
        """A timestamp at exactly window_seconds ago is still within the window (< not <=)."""
        with patch("cadris_cp.rate_limit.time") as mock_time:
            mock_time.time.return_value = 1000.0
            for _ in range(3):
                check_rate_limit("edge", max_requests=3, window_seconds=60)

            # Exactly 60 seconds later — `now - t < window` means t=1000 is pruned
            # because 1060 - 1000 = 60, and 60 < 60 is False
            mock_time.time.return_value = 1060.0
            assert check_rate_limit("edge", max_requests=3, window_seconds=60) is True


# ---------------------------------------------------------------------------
# MAX_KEYS cap
# ---------------------------------------------------------------------------

class TestMaxKeysCap:
    def test_reject_new_key_when_at_capacity(self):
        """When MAX_KEYS is reached, new keys are rejected (fail-closed)."""
        with patch("cadris_cp.rate_limit.time") as mock_time:
            mock_time.time.return_value = 1000.0

            # Fill up to MAX_KEYS
            for i in range(MAX_KEYS):
                key = f"key-{i}"
                assert check_rate_limit(key, max_requests=100, window_seconds=60) is True

            # The next NEW key must be rejected
            assert check_rate_limit("overflow-key", max_requests=100, window_seconds=60) is False

    def test_existing_key_still_works_at_capacity(self):
        """Existing keys can still make requests even when at MAX_KEYS."""
        with patch("cadris_cp.rate_limit.time") as mock_time:
            mock_time.time.return_value = 1000.0

            # Fill to capacity
            for i in range(MAX_KEYS):
                check_rate_limit(f"key-{i}", max_requests=100, window_seconds=60)

            # Existing key is still allowed
            assert check_rate_limit("key-0", max_requests=100, window_seconds=60) is True

    def test_new_key_allowed_after_sweep_frees_slots(self):
        """After a sweep removes stale keys, new keys can be accepted again."""
        with patch("cadris_cp.rate_limit.time") as mock_time:
            mock_time.time.return_value = 1000.0

            # Fill to capacity
            for i in range(MAX_KEYS):
                check_rate_limit(f"key-{i}", max_requests=100, window_seconds=60)

            # Advance time far enough that all keys are stale AND sweep triggers
            mock_time.time.return_value = 1000.0 + _SWEEP_INTERVAL + 1
            rate_limit_mod._last_sweep = 0.0  # force sweep

            # The sweep runs inside check_rate_limit, freeing all stale keys
            assert check_rate_limit("new-key", max_requests=100, window_seconds=60) is True


# ---------------------------------------------------------------------------
# _sweep_stale_keys
# ---------------------------------------------------------------------------

class TestSweepStaleKeys:
    def test_removes_old_entries(self):
        """Stale keys (no recent timestamps) are removed by sweep."""
        _buckets["old-key"] = [500.0]
        _buckets["fresh-key"] = [999.0]
        rate_limit_mod._last_sweep = 0.0  # force sweep

        _sweep_stale_keys(1000.0, max_window=300)

        assert "old-key" not in _buckets
        assert "fresh-key" in _buckets

    def test_sweep_skipped_within_interval(self):
        """Sweep does nothing if called within _SWEEP_INTERVAL."""
        _buckets["old-key"] = [100.0]
        rate_limit_mod._last_sweep = 999.0  # recent sweep

        _sweep_stale_keys(1000.0, max_window=300)

        # Key should still be there because sweep was skipped
        assert "old-key" in _buckets

    def test_sweep_removes_empty_buckets(self):
        """Keys with empty timestamp lists are removed."""
        _buckets["empty"] = []
        rate_limit_mod._last_sweep = 0.0

        _sweep_stale_keys(1000.0, max_window=300)

        assert "empty" not in _buckets

    def test_sweep_updates_last_sweep_timestamp(self):
        """After sweeping, _last_sweep is updated."""
        rate_limit_mod._last_sweep = 0.0

        _sweep_stale_keys(5000.0, max_window=300)

        assert rate_limit_mod._last_sweep == 5000.0

    def test_sweep_preserves_fresh_entries(self):
        """Keys with at least one recent timestamp survive the sweep."""
        _buckets["mixed"] = [100.0, 950.0]  # old + fresh
        rate_limit_mod._last_sweep = 0.0

        _sweep_stale_keys(1000.0, max_window=300)

        # newest (950) is within max_window (1000 - 950 = 50 < 300)
        assert "mixed" in _buckets
