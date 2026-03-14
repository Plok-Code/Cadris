-- T12: File Search indexation + citations

ALTER TABLE mission_inputs ADD COLUMN openai_file_id TEXT;
ALTER TABLE mission_inputs ADD COLUMN vector_store_id TEXT;

CREATE TABLE IF NOT EXISTS citations (
    id TEXT PRIMARY KEY,
    mission_id TEXT NOT NULL REFERENCES missions(id) ON DELETE CASCADE,
    input_id TEXT NOT NULL REFERENCES mission_inputs(id) ON DELETE CASCADE,
    agent_code TEXT NOT NULL,
    excerpt TEXT NOT NULL,
    locator TEXT,
    score REAL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_citations_mission_id ON citations(mission_id);
CREATE INDEX IF NOT EXISTS idx_citations_input_id ON citations(input_id);
