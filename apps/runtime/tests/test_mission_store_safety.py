"""Tests for mission_store safety: ID validation, path traversal, locking."""

from __future__ import annotations

import asyncio

import pytest

from cadris_runtime import mission_store
from cadris_runtime.mission_store import _get_lock, _snapshot_path, _validate_mission_id


# ── _validate_mission_id ────────────────────────────────────────


class TestValidateMissionId:
    """Ensure only safe mission IDs pass validation."""

    @pytest.mark.parametrize(
        "mission_id",
        [
            "mission_abc123",
            "mission-abc-123",
            "abc",
            "A",
            "a1b2c3",
            "UPPER_CASE",
            "with-dashes-and_underscores",
            "a" * 64,  # max length
        ],
    )
    def test_accepts_valid_ids(self, mission_id: str):
        # Should not raise
        _validate_mission_id(mission_id)

    @pytest.mark.parametrize(
        "mission_id",
        [
            "../../../etc/passwd",
            "..\\..\\windows\\system32",
            "",
            "a" * 65,  # too long
            "has spaces",
            "has/slash",
            "has.dot",
            "has@symbol",
            "injection; DROP TABLE",
            "\x00null",
            "path/../traversal",
        ],
    )
    def test_rejects_invalid_ids(self, mission_id: str):
        with pytest.raises(ValueError, match="Invalid mission_id format"):
            _validate_mission_id(mission_id)


# ── _snapshot_path ──────────────────────────────────────────────


class TestSnapshotPath:
    def test_returns_json_path(self, tmp_path, monkeypatch):
        monkeypatch.setattr(mission_store, "_snapshot_dir", tmp_path)
        path = _snapshot_path("valid_mission")
        assert path.name == "valid_mission.json"
        assert path.parent == tmp_path

    def test_rejects_traversal_in_id(self, tmp_path, monkeypatch):
        """IDs containing path separators are rejected by _validate_mission_id."""
        monkeypatch.setattr(mission_store, "_snapshot_dir", tmp_path)
        with pytest.raises(ValueError):
            _snapshot_path("../../../etc/passwd")

    def test_rejects_empty_id(self, tmp_path, monkeypatch):
        monkeypatch.setattr(mission_store, "_snapshot_dir", tmp_path)
        with pytest.raises(ValueError):
            _snapshot_path("")


# ── _get_lock ───────────────────────────────────────────────────


class TestGetLock:
    def test_returns_same_lock_for_same_id(self):
        """setdefault atomicity: calling _get_lock twice returns the same Lock."""
        # Clean up to avoid leaking state between tests
        mission_store._locks.pop("test-lock-id", None)
        try:
            lock1 = _get_lock("test-lock-id")
            lock2 = _get_lock("test-lock-id")
            assert lock1 is lock2
            assert isinstance(lock1, asyncio.Lock)
        finally:
            mission_store._locks.pop("test-lock-id", None)

    def test_different_ids_get_different_locks(self):
        mission_store._locks.pop("id-a", None)
        mission_store._locks.pop("id-b", None)
        try:
            lock_a = _get_lock("id-a")
            lock_b = _get_lock("id-b")
            assert lock_a is not lock_b
        finally:
            mission_store._locks.pop("id-a", None)
            mission_store._locks.pop("id-b", None)


# ── Async wrappers validate IDs ────────────────────────────────


class TestAsyncWrapperValidation:
    @pytest.mark.asyncio
    async def test_aget_rejects_bad_id(self):
        with pytest.raises(ValueError, match="Invalid mission_id format"):
            await mission_store.aget("../traversal")

    @pytest.mark.asyncio
    async def test_aput_rejects_bad_id(self, tmp_path, monkeypatch):
        from cadris_runtime.memory import MissionMemory

        monkeypatch.setattr(mission_store, "_snapshot_dir", tmp_path)
        monkeypatch.setattr(mission_store, "_engine", None)
        memory = MissionMemory(
            mission_id="../bad-id",
            intake_text="test",
        )
        with pytest.raises(ValueError, match="Invalid mission_id format"):
            await mission_store.aput(memory)

    @pytest.mark.asyncio
    async def test_aremove_rejects_bad_id(self):
        with pytest.raises(ValueError, match="Invalid mission_id format"):
            await mission_store.aremove("../../etc/shadow")

    @pytest.mark.asyncio
    async def test_aremove_cleans_up_lock(self, tmp_path, monkeypatch):
        """aremove should delete the lock entry to prevent unbounded growth."""
        monkeypatch.setattr(mission_store, "_snapshot_dir", tmp_path)
        monkeypatch.setattr(mission_store, "_engine", None)
        mission_store._store.clear()

        mid = "cleanup-lock-test"
        mission_store._locks.pop(mid, None)

        await mission_store.aremove(mid)
        assert mid not in mission_store._locks
