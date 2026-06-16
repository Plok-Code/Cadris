-- Migration 013: Add sections_json to artifacts table.
--
-- The ArtifactRecord ORM model includes sections_json but the initial
-- schema (001) didn't define it on the artifacts table. This brings
-- the SQL schema in sync with the ORM.
--
-- IMPORTANT: this is the SOLE creator of artifacts.sections_json, so it must
-- NOT use "IF NOT EXISTS". SQLite has no ADD COLUMN IF NOT EXISTS syntax,
-- the migration runner would catch the resulting syntax error and skip the
-- statement, leaving the column missing on every fresh SQLite database.
-- Migration 012 can use IF NOT EXISTS only because its columns are already
-- created by earlier plain ALTERs (there it is a Postgres-only no-op).
-- Idempotency on re-run is handled by the runner catching "duplicate column".
-- NB keep migration comments free of the statement separator char, since the
-- runner splits the file on it before executing each chunk.

ALTER TABLE artifacts ADD COLUMN sections_json TEXT DEFAULT '[]';
