-- Migration 013: Add sections_json to artifacts table.
--
-- The ArtifactRecord ORM model includes sections_json but the initial
-- schema (001) didn't define it on the artifacts table. This brings
-- the SQL schema in sync with the ORM.
--
-- Note: No IF NOT EXISTS — the migration runner handles duplicates
-- gracefully via "duplicate column" error catching (SQLite + Postgres).

ALTER TABLE artifacts ADD COLUMN sections_json TEXT DEFAULT '[]';
