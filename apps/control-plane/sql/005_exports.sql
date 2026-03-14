-- T14: Export tracking and share links
CREATE TABLE IF NOT EXISTS exports (
    id TEXT PRIMARY KEY,
    mission_id TEXT NOT NULL REFERENCES missions(id) ON DELETE CASCADE,
    bundle_type TEXT NOT NULL DEFAULT 'MissionDossier',  -- MissionDossier | SelectedArtifacts
    format TEXT NOT NULL,                                 -- Markdown | PDF | ShareLink
    snapshot_version INTEGER NOT NULL DEFAULT 1,
    partial BOOLEAN NOT NULL DEFAULT FALSE,
    token TEXT UNIQUE,                                    -- share link token (null if not shared)
    file_url TEXT,                                        -- URL of rendered file if applicable
    revoked BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    revoked_at TEXT
);

CREATE INDEX IF NOT EXISTS idx_exports_mission_id ON exports(mission_id);
CREATE INDEX IF NOT EXISTS idx_exports_token ON exports(token) WHERE token IS NOT NULL;
