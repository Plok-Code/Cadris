"""Tests for training_logger.py — JSONL event logging."""
from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import cadris_runtime.training_logger as tl


class TestTrainingLogger:
    def setup_method(self):
        self._tmpdir = tempfile.mkdtemp()
        self._events = Path(self._tmpdir) / "events.jsonl"
        self._feedback = Path(self._tmpdir) / "feedback.jsonl"

    def test_disabled_by_default(self):
        """Logger must not write anything when TRAINING_ENABLED is False."""
        with patch.object(tl, "TRAINING_ENABLED", False):
            tl._append_jsonl(self._events, {"test": True})
        assert not self._events.exists()

    def test_enabled_writes_jsonl(self):
        """When enabled, each call appends one JSON line."""
        with patch.object(tl, "TRAINING_ENABLED", True):
            tl._append_jsonl(self._events, {"type": "test", "value": 42})
            tl._append_jsonl(self._events, {"type": "test", "value": 43})

        lines = self._events.read_text().strip().split("\n")
        assert len(lines) == 2
        assert json.loads(lines[0])["value"] == 42
        assert json.loads(lines[1])["value"] == 43

    def test_log_mission_start(self):
        with patch.object(tl, "TRAINING_ENABLED", True), patch.object(tl, "EVENTS_FILE", self._events):
            tl.log_mission_start(
                mission_id="m1",
                intake_text="Build a SaaS",
                qualification_questions=[{"question": "Q1"}],
                qualification_answers={"Q1": "A1"},
                plan="free",
            )
        data = json.loads(self._events.read_text().strip())
        assert data["type"] == "mission_start"
        assert data["mission_id"] == "m1"
        assert data["plan"] == "free"

    def test_log_document(self):
        with patch.object(tl, "TRAINING_ENABLED", True), patch.object(tl, "EVENTS_FILE", self._events):
            tl.log_document(
                mission_id="m1", doc_id="vision", agent="strategy",
                title="Vision", content="Content here", certainty="solid",
                wave=1, model="gpt-4.1", provider="openai",
            )
        data = json.loads(self._events.read_text().strip())
        assert data["type"] == "document"
        assert data["content_length"] == len("Content here")

    def test_log_feedback(self):
        with patch.object(tl, "TRAINING_ENABLED", True), patch.object(tl, "FEEDBACK_FILE", self._feedback):
            tl.log_feedback(mission_id="m1", doc_id="vision", rating=5, correction="Fix X")
        data = json.loads(self._feedback.read_text().strip())
        assert data["type"] == "feedback"
        assert data["rating"] == 5

    def test_handles_write_error_gracefully(self):
        """OSError on write must not raise — just log a warning."""
        with patch.object(tl, "TRAINING_ENABLED", True):
            # Write to an impossible path
            tl._append_jsonl(Path("/nonexistent/dir/file.jsonl"), {"test": True})
            # Should not raise
