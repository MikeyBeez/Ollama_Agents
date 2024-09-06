# src/utils/schema.py

SCHEMA = """
CREATE TABLE IF NOT EXISTS edges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    strength REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_id, target_id, relationship_type)
);

CREATE INDEX IF NOT EXISTS idx_source_id ON edges(source_id);
CREATE INDEX IF NOT EXISTS idx_target_id ON edges(target_id);
CREATE INDEX IF NOT EXISTS idx_relationship_type ON edges(relationship_type);

CREATE TRIGGER IF NOT EXISTS update_edges_timestamp
AFTER UPDATE ON edges
BEGIN
    UPDATE edges SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
"""
