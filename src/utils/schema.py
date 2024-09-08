# src/utils/schema.py

SCHEMA = """
CREATE TABLE IF NOT EXISTS edges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id TEXT NOT NULL,
    target_id TEXT NOT NULL,
    relationship_type TEXT NOT NULL,
    strength REAL NOT NULL,
    confidence REAL NOT NULL DEFAULT 1.0,
    bidirectional BOOLEAN DEFAULT FALSE,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_id, target_id, relationship_type)
);

CREATE TABLE IF NOT EXISTS node_attributes (
    node_id TEXT NOT NULL,
    attribute_name TEXT NOT NULL,
    attribute_value TEXT NOT NULL,
    confidence REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (node_id, attribute_name)
);

CREATE TABLE IF NOT EXISTS hierarchies (
    parent_id TEXT NOT NULL,
    child_id TEXT NOT NULL,
    hierarchy_type TEXT NOT NULL,
    confidence REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (parent_id, child_id, hierarchy_type)
);

CREATE INDEX IF NOT EXISTS idx_edges_source_id ON edges(source_id);
CREATE INDEX IF NOT EXISTS idx_edges_target_id ON edges(target_id);
CREATE INDEX IF NOT EXISTS idx_edges_relationship_type ON edges(relationship_type);
CREATE INDEX IF NOT EXISTS idx_edges_start_time ON edges(start_time);
CREATE INDEX IF NOT EXISTS idx_edges_end_time ON edges(end_time);
CREATE INDEX IF NOT EXISTS idx_node_attributes_node_id ON node_attributes(node_id);
CREATE INDEX IF NOT EXISTS idx_hierarchies_parent_id ON hierarchies(parent_id);
CREATE INDEX IF NOT EXISTS idx_hierarchies_child_id ON hierarchies(child_id);

CREATE TRIGGER IF NOT EXISTS update_edges_timestamp
AFTER UPDATE ON edges
BEGIN
    UPDATE edges SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

CREATE TRIGGER IF NOT EXISTS update_node_attributes_timestamp
AFTER UPDATE ON node_attributes
BEGIN
    UPDATE node_attributes SET updated_at = CURRENT_TIMESTAMP
    WHERE node_id = NEW.node_id AND attribute_name = NEW.attribute_name;
END;

CREATE TRIGGER IF NOT EXISTS update_hierarchies_timestamp
AFTER UPDATE ON hierarchies
BEGIN
    UPDATE hierarchies SET updated_at = CURRENT_TIMESTAMP
    WHERE parent_id = NEW.parent_id AND child_id = NEW.child_id AND hierarchy_type = NEW.hierarchy_type;
END;
"""
