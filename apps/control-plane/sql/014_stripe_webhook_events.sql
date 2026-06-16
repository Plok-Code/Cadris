-- Migration 014: Durable Stripe webhook idempotency ledger.
--
-- Replaces the in-memory FIFO set used to dedupe Stripe event deliveries,
-- which lost its state on restart and was not shared across replicas
-- (risking double-processing of subscription/checkout events after a
-- redeploy or under horizontal scaling).
--
-- One row per processed Stripe event id. The PRIMARY KEY gives us atomic
-- "insert-if-absent" semantics: a concurrent duplicate delivery fails the
-- insert and is treated as already processed.

CREATE TABLE IF NOT EXISTS stripe_webhook_events (
  event_id TEXT PRIMARY KEY,
  processed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
