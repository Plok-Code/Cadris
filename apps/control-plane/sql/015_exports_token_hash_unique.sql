-- Migration 015: Enforce uniqueness of share-link token hashes.
--
-- exports.token_hash stores the SHA-256 of a share token (the raw token is
-- never persisted). secrets.token_urlsafe(32) already makes collisions
-- astronomically unlikely, but a UNIQUE index turns any hypothetical
-- collision into a fast, loud failure instead of silent ambiguity, and it
-- doubles as the lookup index for get_export_by_token_hash().
--
-- NULL token_hash (non-share exports: PDF/PPTX/ZIP) is allowed many times:
-- both SQLite and Postgres treat NULLs as distinct in a UNIQUE index.

CREATE UNIQUE INDEX IF NOT EXISTS ix_exports_token_hash_unique
  ON exports (token_hash);
