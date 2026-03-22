-- Security: store share tokens as SHA-256 hashes instead of plaintext,
-- and add expiration to share links.
-- Note: SQLite does not support ADD COLUMN with UNIQUE, so we use a
-- separate CREATE UNIQUE INDEX instead.
ALTER TABLE exports ADD COLUMN token_hash TEXT;
ALTER TABLE exports ADD COLUMN expires_at TEXT;

CREATE UNIQUE INDEX IF NOT EXISTS idx_exports_token_hash_unique ON exports(token_hash) WHERE token_hash IS NOT NULL;
