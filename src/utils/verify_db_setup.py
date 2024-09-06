# src/utils/verify_db_setup.py

import sqlite3
from pathlib import Path

DB_DIR = Path('data/edgebase')
DB_FILE = 'knowledge_edges.db'
DB_PATH = DB_DIR / DB_FILE

def verify_setup():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Verifying database setup...")

    # Check indexes
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='edges';")
    indexes = cursor.fetchall()
    print("\nIndexes on 'edges' table:")
    for index in indexes:
        print(f"  - {index[0]}")

    # Test creating an edge
    try:
        cursor.execute("""
        INSERT INTO edges (source_id, target_id, relationship_type, strength)
        VALUES ('test_source', 'test_target', 'test_relation', 0.5)
        """)
        print("\nTest edge inserted successfully.")
    except sqlite3.Error as e:
        print(f"\nError inserting test edge: {e}")

    # Verify the insertion
    cursor.execute("SELECT * FROM edges WHERE source_id = 'test_source'")
    result = cursor.fetchone()
    if result:
        print(f"Retrieved test edge: {result}")
    else:
        print("Failed to retrieve test edge.")

    # Test updating the edge
    try:
        cursor.execute("""
        UPDATE edges
        SET strength = 0.7
        WHERE source_id = 'test_source' AND target_id = 'test_target'
        """)
        print("\nTest edge updated successfully.")
    except sqlite3.Error as e:
        print(f"\nError updating test edge: {e}")

    # Verify the update and trigger
    cursor.execute("SELECT * FROM edges WHERE source_id = 'test_source'")
    result = cursor.fetchone()
    if result:
        print(f"Retrieved updated test edge: {result}")
        print("Check if 'updated_at' timestamp has changed.")
    else:
        print("Failed to retrieve updated test edge.")

    # Clean up test data
    cursor.execute("DELETE FROM edges WHERE source_id = 'test_source'")
    print("\nTest data cleaned up.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    verify_setup()
