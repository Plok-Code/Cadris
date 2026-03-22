-- Migration 012: Idempotent re-declaration of ALTER TABLE columns for Postgres.
--
-- SQLite silently handled duplicate ADD COLUMN via the migration runner's
-- per-statement error handler (catches "duplicate column" / "already exists").
-- Postgres also raises errors caught by the same handler.
--
-- This migration uses ADD COLUMN IF NOT EXISTS (Postgres 9.6+) as a
-- belt-and-suspenders safeguard so that re-running on Postgres never errors,
-- even outside the migration runner.
--
-- For SQLite < 3.35 (no IF NOT EXISTS support): the migration runner's
-- per-statement try/except already catches the duplicate-column error, so
-- these statements are safe on both engines.

-- From 003_upload_inputs.sql
ALTER TABLE mission_inputs ADD COLUMN IF NOT EXISTS display_name TEXT;
ALTER TABLE mission_inputs ADD COLUMN IF NOT EXISTS mime_type TEXT;
ALTER TABLE mission_inputs ADD COLUMN IF NOT EXISTS byte_size INTEGER;
ALTER TABLE mission_inputs ADD COLUMN IF NOT EXISTS storage_path TEXT;
ALTER TABLE mission_inputs ADD COLUMN IF NOT EXISTS preview_text TEXT;

-- From 006_billing_user_columns.sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS name TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS stripe_customer_id TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS plan_expires_at TEXT;
ALTER TABLE users ADD COLUMN IF NOT EXISTS missions_this_month INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN IF NOT EXISTS month_reset_at TEXT;

-- From 008_mission_persistence.sql
ALTER TABLE missions ADD COLUMN IF NOT EXISTS phase TEXT DEFAULT 'intake';
ALTER TABLE missions ADD COLUMN IF NOT EXISTS current_wave INTEGER DEFAULT 0;
ALTER TABLE missions ADD COLUMN IF NOT EXISTS qualification_answers_json TEXT DEFAULT '{}';

-- From 009_qualification_questions.sql
ALTER TABLE missions ADD COLUMN IF NOT EXISTS qualification_questions_json TEXT DEFAULT '[]';
