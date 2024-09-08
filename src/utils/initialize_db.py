# src/utils/initialize_db.py

import sqlite3
from pathlib import Path
from schema import SCHEMA

# Configuration
DB_DIR = Path('data/edgebase')
DB_FILE = 'knowledge_edges.db'
DB_PATH = DB_DIR / DB_FILE

def create_directory():
    """Create the database directory if it doesn't exist."""
    if not DB_DIR.exists():
        DB_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Directory created: {DB_DIR}")
    else:
        print(f"Directory already exists: {DB_DIR}")

def database_exists():
    """Check if the database file already exists."""
    return DB_PATH.is_file()

def initialize_database():
    """Initialize the database, create tables, and set up triggers if they don't exist."""
    create_directory()

    if database_exists():
        print(f"Database already exists: {DB_PATH}")
        update_existing_database()
    else:
        print(f"Creating new database: {DB_PATH}")
        create_new_database()

def create_new_database():
    """Create a new database with the full schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Execute the full schema
    cursor.executescript(SCHEMA)

    conn.commit()
    conn.close()
    print("New database created with full schema.")

def update_existing_database():
    """Update existing database with new tables and columns."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Check if edges table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='edges'")
    if cursor.fetchone():
        # Add new columns to edges table if they don't exist
        columns_to_add = [
            ("confidence", "REAL NOT NULL DEFAULT 1.0"),
            ("bidirectional", "BOOLEAN DEFAULT FALSE"),
            ("start_time", "TIMESTAMP"),
            ("end_time", "TIMESTAMP"),
            ("metadata", "JSON")
        ]
        for column_name, column_type in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE edges ADD COLUMN {column_name} {column_type}")
                print(f"Added column {column_name} to edges table")
            except sqlite3.OperationalError:
                print(f"Column {column_name} already exists in edges table")
    else:
        # If edges table doesn't exist, create it
        cursor.execute("""
        CREATE TABLE edges (
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
        )
        """)
        print("Created edges table")

    # Create new tables if they don't exist
    cursor.executescript("""
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
    """)

    # Create indexes if they don't exist
    cursor.executescript("""
    CREATE INDEX IF NOT EXISTS idx_edges_source_id ON edges(source_id);
    CREATE INDEX IF NOT EXISTS idx_edges_target_id ON edges(target_id);
    CREATE INDEX IF NOT EXISTS idx_edges_relationship_type ON edges(relationship_type);
    CREATE INDEX IF NOT EXISTS idx_edges_start_time ON edges(start_time);
    CREATE INDEX IF NOT EXISTS idx_edges_end_time ON edges(end_time);
    CREATE INDEX IF NOT EXISTS idx_node_attributes_node_id ON node_attributes(node_id);
    CREATE INDEX IF NOT EXISTS idx_hierarchies_parent_id ON hierarchies(parent_id);
    CREATE INDEX IF NOT EXISTS idx_hierarchies_child_id ON hierarchies(child_id);
    """)

    # Create triggers if they don't exist
    cursor.executescript("""
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
    """)

    conn.commit()
    conn.close()
    print("Existing database updated with new schema elements.")

def check_database_status():
    """Check the status of the database and print table information."""
    if not database_exists():
        print("Database does not exist.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("\nDatabase Status:")
    print(f"Tables found: {len(tables)}")

    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        print(f"\nTable: {table_name}")
        print("Columns:")
        for column in columns:
            print(f"  - {column[1]} ({column[2]})")

        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        print(f"Row count: {row_count}")

    # Check triggers
    cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger';")
    triggers = cursor.fetchall()
    print("\nTriggers:")
    for trigger in triggers:
        print(f"  - {trigger[0]}")

    # Check indexes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index';")
    indexes = cursor.fetchall()
    print("\nIndexes:")
    for index in indexes:
        print(f"  - {index[0]}")

    conn.close()

def main():
    initialize_database()
    check_database_status()
    print("\nDatabase setup completed successfully.")

if __name__ == "__main__":
    main()
