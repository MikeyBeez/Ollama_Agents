# src/utils/test_edge_migration.py

import os
#import sqlite3
#from pathlib import Path
from collections import Counter

# Adjust the import path as necessary
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.kb_graph import get_db_connection, get_related_nodes
from migrate_to_edge import main as migrate_main

def test_edge_migration():
    # Run the migration
    migrate_main()

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all unique nodes
    cursor.execute("SELECT DISTINCT source_id FROM edges UNION SELECT DISTINCT target_id FROM edges")
    all_nodes = [row[0] for row in cursor.fetchall()]

    print(f"Total unique nodes: {len(all_nodes)}")

    # Get edge statistics
    cursor.execute("SELECT COUNT(*) FROM edges")
    total_edges = cursor.fetchone()[0]
    print(f"Total edges: {total_edges}")

    cursor.execute("SELECT relationship_type, COUNT(*) FROM edges GROUP BY relationship_type")
    edge_types = cursor.fetchall()
    print("Edge types distribution:")
    for edge_type, count in edge_types:
        print(f"  {edge_type}: {count}")

    # Analyze node connectivity
    connectivity = []
    for node in all_nodes:
        related = get_related_nodes(node)
        connectivity.append(len(related))

    print(f"Average connections per node: {sum(connectivity) / len(connectivity):.2f}")
    print(f"Max connections for a node: {max(connectivity)}")
    print(f"Min connections for a node: {min(connectivity)}")

    # Find the most connected node
    most_connected_node = all_nodes[connectivity.index(max(connectivity))]
    print(f"Most connected node: {most_connected_node}")
    print("Its connections:")
    for related_node, relationship_type, strength in get_related_nodes(most_connected_node):
        print(f"  Connected to {related_node} with relationship {relationship_type} (strength: {strength})")

    # Analyze relationship type distribution for a random node
    random_node = all_nodes[len(all_nodes) // 2]  # Just picking the middle node for this example
    print(f"\nAnalyzing relationships for node: {random_node}")
    relationships = get_related_nodes(random_node)
    relationship_types = Counter([rel[1] for rel in relationships])
    for rel_type, count in relationship_types.items():
        print(f"  {rel_type}: {count}")

    conn.close()

if __name__ == "__main__":
    test_edge_migration()
