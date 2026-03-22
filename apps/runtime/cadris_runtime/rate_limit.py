"""In-memory sliding-window rate limiter with bounded memory.

Copied from control-plane pattern. NOT shared across processes.
Suitable for single-instance or per-container deployments (Cloud Run).

Memory safety: keys are evicted on access (lazy) and via periodic
full sweep. MAX_KEYS caps total entries to prevent unbounded growth.
"""
from __future__ import annotations

import logging
import time
from collections import defaultdict

logger = logging.getLogger(__name__)

MAX_KEYS = 10_000  # hard cap on distinct rate-limit keys

_buckets: dict[str, list[float]] = defaultdict(list)
_last_sweep: float = 0.0
_SWEEP_INTERVAL = 300.0  # full sweep every 5 minutes


def _sweep_stale_keys(now: float, max_window: int = 300) -> None:
    """Remove all keys whose newest timestamp is older than max_window."""
    global _last_sweep
    if now - _last_sweep < _SWEEP_INTERVAL:
        return
    _last_sweep = now
    stale = [k for k, timestamps in _buckets.items() if not timestamps or now - timestamps[-1] > max_window]
    for k in stale:
        del _buckets[k]
    if stale:
        logger.debug("rate_limit: swept %d stale keys, %d remaining", len(stale), len(_buckets))


def check_rate_limit(key: str, *, max_requests: int = 5, window_seconds: int = 60) -> bool:
    """Return True if the request is allowed, False if rate-limited.

    Prunes expired timestamps on each call to keep memory bounded.
    Enforces MAX_KEYS to prevent unbounded growth from distinct keys.
    """
    now = time.time()

    # Periodic sweep of stale keys
    _sweep_stale_keys(now, max_window=max(window_seconds, 300))

    # Reject new keys if we're at capacity (fail-closed)
    if key not in _buckets and len(_buckets) >= MAX_KEYS:
        logger.warning("rate_limit: MAX_KEYS (%d) reached, rejecting new key", MAX_KEYS)
        return False

    bucket = _buckets[key]
    _buckets[key] = [t for t in bucket if now - t < window_seconds]
    if len(_buckets[key]) >= max_requests:
        return False
    _buckets[key].append(now)
    return True
