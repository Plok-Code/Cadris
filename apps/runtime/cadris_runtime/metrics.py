"""Lightweight observability metrics for the runtime engine.

Collects counters and histograms in-memory, exposed via /internal/runtime/metrics
as JSON. Compatible with:
- Cloud Run custom metrics (via structured logging)
- Future Prometheus/OpenTelemetry integration (swap this module)

No external dependencies — pure stdlib + structured JSON logging.
"""
from __future__ import annotations

import logging
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class _Histogram:
    """Simple histogram: tracks count, sum, min, max per bucket."""
    count: int = 0
    total: float = 0.0
    min_val: float = float("inf")
    max_val: float = 0.0

    def observe(self, value: float) -> None:
        self.count += 1
        self.total += value
        self.min_val = min(self.min_val, value)
        self.max_val = max(self.max_val, value)

    @property
    def avg(self) -> float:
        return self.total / self.count if self.count > 0 else 0.0

    def to_dict(self) -> dict:
        if self.count == 0:
            return {"count": 0}
        return {
            "count": self.count,
            "avg_ms": round(self.avg, 1),
            "min_ms": round(self.min_val, 1),
            "max_ms": round(self.max_val, 1),
            "total_ms": round(self.total, 1),
        }


class RuntimeMetrics:
    """Thread-safe runtime metrics collector."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # Counters
        self.missions_started: int = 0
        self.missions_completed: int = 0
        self.missions_failed: int = 0
        self.agents_executed: int = 0
        self.agents_failed: int = 0
        self.agents_fallback: int = 0
        self.documents_produced: int = 0
        self.critic_runs: int = 0
        self.retries_total: int = 0
        # Per-agent histograms (agent_code → histogram)
        self.agent_latency: dict[str, _Histogram] = defaultdict(_Histogram)
        # Per-plan counters
        self.missions_by_plan: dict[str, int] = defaultdict(int)
        # Errors by type
        self.errors_by_type: dict[str, int] = defaultdict(int)

    def record_mission_start(self, plan: str) -> None:
        with self._lock:
            self.missions_started += 1
            self.missions_by_plan[plan] += 1

    def record_mission_complete(self) -> None:
        with self._lock:
            self.missions_completed += 1

    def record_mission_failed(self) -> None:
        with self._lock:
            self.missions_failed += 1

    def record_agent_execution(self, agent_code: str, elapsed_ms: float, success: bool) -> None:
        with self._lock:
            self.agents_executed += 1
            self.agent_latency[agent_code].observe(elapsed_ms)
            if not success:
                self.agents_failed += 1

    def record_agent_fallback(self, agent_code: str) -> None:
        with self._lock:
            self.agents_fallback += 1

    def record_documents(self, count: int) -> None:
        with self._lock:
            self.documents_produced += count

    def record_critic_run(self) -> None:
        with self._lock:
            self.critic_runs += 1

    def record_retry(self, agent_code: str, error_type: str) -> None:
        with self._lock:
            self.retries_total += 1
            self.errors_by_type[error_type] += 1

    def snapshot(self) -> dict:
        """Return a JSON-serializable snapshot of all metrics."""
        with self._lock:
            return {
                "missions": {
                    "started": self.missions_started,
                    "completed": self.missions_completed,
                    "failed": self.missions_failed,
                    "by_plan": dict(self.missions_by_plan),
                },
                "agents": {
                    "executed": self.agents_executed,
                    "failed": self.agents_failed,
                    "fallback": self.agents_fallback,
                    "retries": self.retries_total,
                    "latency_by_agent": {
                        code: hist.to_dict()
                        for code, hist in self.agent_latency.items()
                    },
                },
                "documents_produced": self.documents_produced,
                "critic_runs": self.critic_runs,
                "errors_by_type": dict(self.errors_by_type),
            }


# Singleton instance
metrics = RuntimeMetrics()
