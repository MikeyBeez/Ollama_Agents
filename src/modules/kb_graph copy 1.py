# src/modules/kb_graph.py

import json
import hashlib
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Tuple, Union
from collections import Counter
import re
from datetime import datetime
#from src.modules.knowledge_extraction import extract_entities_and_relationships

# Define DB_DIR and DB_FILE here
DB_DIR = Path('data/edgebase')
DB_FILE = 'knowledge_edges.db'
DB_PATH = DB_DIR / DB_FILE

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_edge(source_id: str, target_id: str, relationship_type: str, strength: float):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO edges (source_id, target_id, relationship_type, strength)
            VALUES (?, ?, ?, ?)
        ''', (source_id, target_id, relationship_type, strength))
        conn.commit()

def update_knowledge_graph(new_information: str):
    extracted_info = extract_entities_and_relationships(new_information)

    # Create edges for entities
    for entity in extracted_info["entities"]:
        create_edge("INFO", entity["text"], entity["label"], 1.0)

    # Create edges for relationships
    for relation in extracted_info["relationships"]:
        create_edge(relation["subject"], relation["object"], relation["relationship"], 1.0)

    # Create edges for key concepts (assuming we still want to keep this functionality)
    key_concepts = extract_key_concepts(new_information)
    info_id = hashlib.md5(new_information.encode()).hexdigest()
    for concept in key_concepts:
        create_edge(info_id, concept, "RELATED_TO", 1.0)

    print(f"Updated knowledge graph with new information (ID: {info_id})")

def extract_key_concepts(information: str) -> List[str]:
    # This is a simple implementation. In practice, you might want to use
    # more sophisticated NLP techniques here.
    words = re.findall(r'\w+', information.lower())
    word_freq = Counter(words)
    # Consider words that appear more than once as key concepts
    return [word for word, freq in word_freq.items() if freq > 1]

def get_related_nodes(node_id: str, relationship_type: str = None) -> List[Tuple[str, str, float]]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if relationship_type:
            cursor.execute('''
                SELECT target_id, relationship_type, strength
                FROM edges
                WHERE source_id = ? AND relationship_type = ?
                UNION
                SELECT source_id, relationship_type, strength
                FROM edges
                WHERE target_id = ? AND relationship_type = ?
            ''', (node_id, relationship_type, node_id, relationship_type))
        else:
            cursor.execute('''
                SELECT target_id, relationship_type, strength
                FROM edges
                WHERE source_id = ?
                UNION
                SELECT source_id, relationship_type, strength
                FROM edges
                WHERE target_id = ?
            ''', (node_id, node_id))
        return [(row['target_id'], row['relationship_type'], row['strength']) for row in cursor.fetchall()]

def analyze_file_pair(file1: Dict[str, Any], file2: Dict[str, Any]) -> List[Tuple[str, float]]:
    edge_categories = []

    if 'content' in file1 and 'content' in file2:
        content_similarity = compare_content(file1['content'], file2['content'])
        if content_similarity > 0.3:
            edge_categories.append(("SIMILAR_CONTENT", content_similarity))

    if 'tags' in file1 and 'tags' in file2:
        tag_similarity = compare_tags(file1['tags'], file2['tags'])
        if tag_similarity > 0:
            edge_categories.append(("SHARED_TAGS", tag_similarity))

    if 'title' in file1 and 'title' in file2:
        title_similarity = compare_titles(file1['title'], file2['title'])
        if title_similarity > 0.5:
            edge_categories.append(("RELATED_TOPIC", title_similarity))

    if 'timestamp' in file1 and 'timestamp' in file2:
        time_relation = compare_timestamps(file1['timestamp'], file2['timestamp'])
        if time_relation:
            edge_categories.append(time_relation)

    return edge_categories

def compare_content(content1: Union[str, Dict, List], content2: Union[str, Dict, List]) -> float:
    def extract_text(content: Union[str, Dict, List]) -> str:
        if isinstance(content, str):
            return content
        elif isinstance(content, dict):
            return ' '.join(str(v) for v in content.values() if isinstance(v, str))
        elif isinstance(content, list):
            return ' '.join(str(item) for item in content if isinstance(item, str))
        else:
            return ''

    text1 = extract_text(content1)
    text2 = extract_text(content2)

    words1 = set(re.findall(r'\w+', text1.lower()))
    words2 = set(re.findall(r'\w+', text2.lower()))
    common_words = words1.intersection(words2)
    return len(common_words) / (len(words1) + len(words2) - len(common_words)) if (words1 or words2) else 0

def compare_tags(tags1: List[str], tags2: List[str]) -> float:
    common_tags = set(tags1).intersection(set(tags2))
    return len(common_tags) / len(set(tags1).union(set(tags2))) if (tags1 or tags2) else 0

def compare_titles(title1: str, title2: str) -> float:
    words1 = set(re.findall(r'\w+', title1.lower()))
    words2 = set(re.findall(r'\w+', title2.lower()))
    common_words = words1.intersection(words2)
    return len(common_words) / (len(words1) + len(words2) - len(common_words)) if (words1 or words2) else 0

def compare_timestamps(timestamp1: str, timestamp2: str) -> Union[Tuple[str, float], None]:
    t1 = datetime.fromisoformat(timestamp1.replace('Z', '+00:00'))
    t2 = datetime.fromisoformat(timestamp2.replace('Z', '+00:00'))
    time_diff = abs((t2 - t1).total_seconds())

    if time_diff < 3600:  # Within an hour
        return ("TEMPORALLY_CLOSE", 0.9)
    elif time_diff < 86400:  # Within a day
        return ("SAME_DAY", 0.7)
    elif time_diff < 604800:  # Within a week
        return ("SAME_WEEK", 0.5)
    else:
        return None

if __name__ == "__main__":
    file1 = {
        "title": "Introduction to Python",
        "content": "Python is a high-level programming language...",
        "tags": ["programming", "beginner", "python"],
        "timestamp": "2023-05-01T10:00:00Z"
    }
    file2 = {
        "title": "Python for Data Science",
        "content": "Python is widely used in data science for its simplicity...",
        "tags": ["programming", "data science", "python"],
        "timestamp": "2023-05-01T11:30:00Z"
    }

    edge_categories = analyze_file_pair(file1, file2)
    print("Edge categories:", edge_categories)

    update_knowledge_graph(file1)
    update_knowledge_graph(file2)

    file1_id = hashlib.md5(json.dumps(file1, sort_keys=True).encode()).hexdigest()
    file2_id = hashlib.md5(json.dumps(file2, sort_keys=True).encode()).hexdigest()
    for category, strength in edge_categories:
        create_edge(file1_id, file2_id, category, strength)

    related_nodes = get_related_nodes(file1_id)
    print("Related nodes:", related_nodes)
