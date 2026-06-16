"""Tests for durable Stripe webhook idempotency (cov-stripe-webhook-01).

Covers the DB-backed dedupe ledger that replaced the in-memory FIFO set, so a
redeploy or a second replica can no longer double-process a Stripe event.
"""
from __future__ import annotations

from uuid import uuid4

from cadris_cp.billing import _mark_event_processed, _plan_from_price
from cadris_cp.records import StripeWebhookEventRecord

from .conftest import _TestSession


class TestWebhookIdempotency:
    def test_first_delivery_records_and_second_skips(self):
        event_id = f"evt_{uuid4().hex}"
        with _TestSession() as s:
            assert _mark_event_processed(event_id, s) is False  # first time → process
        # New session (simulates a different request / replica / post-restart):
        with _TestSession() as s:
            assert _mark_event_processed(event_id, s) is True  # already processed

    def test_distinct_events_are_independent(self):
        with _TestSession() as s:
            assert _mark_event_processed(f"evt_{uuid4().hex}", s) is False
            assert _mark_event_processed(f"evt_{uuid4().hex}", s) is False

    def test_marker_is_persisted(self):
        event_id = f"evt_{uuid4().hex}"
        with _TestSession() as s:
            _mark_event_processed(event_id, s)
        with _TestSession() as s:
            assert s.get(StripeWebhookEventRecord, event_id) is not None


class TestPlanResolution:
    def test_unknown_price_defaults_to_free(self):
        assert _plan_from_price("price_does_not_exist") == "free"
