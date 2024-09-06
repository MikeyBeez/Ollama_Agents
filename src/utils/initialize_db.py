# src/utils/initialize_db.py

import os
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
    else:
        print(f"Creating new database: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Execute the schema
    cursor.executescript(SCHEMA)

    conn.commit()
    conn.close()
    print("Database schema initialized.")

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

    conn.close()

def main():
    initialize_database()
    check_database_status()
    print("\nDatabase setup completed successfully.")

if __name__ == "__main__":
    main()
