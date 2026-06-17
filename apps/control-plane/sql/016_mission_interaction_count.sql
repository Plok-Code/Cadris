-- Migration 016: per-mission interaction counter (abuse / cost ceiling).
--
-- Every expensive agent round-trip within a mission goes through the resume
-- endpoint (answer_qualification / refine_wave / next_wave). Counting them
-- server-side lets us cap the total LLM work a single (paid, fixed-price)
-- mission can trigger, so a determined abuser can't loop corrections to run up
-- our cost. The UI cap (3 corrections per block) only protects normal users.
--
-- Plain ADD COLUMN (no IF NOT EXISTS) — this is the sole creator of the column
-- and SQLite has no IF NOT EXISTS for ALTER. Keep comments semicolon-free.

ALTER TABLE missions ADD COLUMN interaction_count INTEGER DEFAULT 0;
