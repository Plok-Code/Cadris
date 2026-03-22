"""Simple in-memory sliding-window rate limiter.

Not shared across processes — suitable for single-instance or
per-container deployments.  For multi-replica setups, replace with
Redis-backed counters.
"""
from __future__ import annotations

import time
from collections import defaultdict

_buckets: dict[str, list[float]] = defaultdict(list)


def check_rate_limit(key: str, *, max_requests: int = 5, window_seconds: int = 60) -> bool:
    """Return True if the request is allowed, False if rate-limited.

    Prunes expired timestamps on each call to keep memory bounded.
    """
    now = time.time()
    bucket = _buckets[key]
    _buckets[key] = [t for t in bucket if now - t < window_seconds]
    if len(_buckets[key]) >= max_requests:
        return False
    _buckets[key].append(now)
    return True
