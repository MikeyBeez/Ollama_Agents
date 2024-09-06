# src/utils/migrate_to_edge.py

import os
import json
from pathlib import Path
from typing import List, Dict, Any
import hashlib

# Adjust the import path as necessary
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.kb_graph import analyze_file_pair, update_knowledge_graph, create_edge, get_related_nodes

DATA_DIR = Path('data')

def load_json_files(directory: Path) -> List[Dict[str, Any]]:
    json_files = []
    for file_path in directory.glob('**/*.json'):
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
                json_files.append(data)
            except json.JSONDecodeError:
                print(f"Error decoding JSON from file: {file_path}")
    return json_files

def process_files(files: List[Dict[str, Any]]):
    for i, file1 in enumerate(files):
        try:
            update_knowledge_graph(file1)
            file1_id = hashlib.md5(json.dumps(file1, sort_keys=True).encode()).hexdigest()

            for file2 in files[i+1:]:
                try:
                    file2_id = hashlib.md5(json.dumps(file2, sort_keys=True).encode()).hexdigest()
                    edge_categories = analyze_file_pair(file1, file2)

                    for category, strength in edge_categories:
                        create_edge(file1_id, file2_id, category, strength)
                except Exception as e:
                    print(f"Error processing file pair: {e}")
        except Exception as e:
            print(f"Error processing file: {e}")

def main():
    print("Starting migration process...")
    files = load_json_files(DATA_DIR)
    print(f"Loaded {len(files)} JSON files.")

    process_files(files)
    print("Migration complete.")

if __name__ == "__main__":
    main()
