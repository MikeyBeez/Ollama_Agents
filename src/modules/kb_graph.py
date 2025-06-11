# src/modules/kb_graph.py

import json
import hashlib
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

# Configuration
DB_DIR = Path('data/edgebase')
DB_FILE = 'knowledge_edges.db'
DB_PATH = DB_DIR / DB_FILE

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def create_edge(source_id: str, target_id: str, relationship_type: str, strength: float):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO edges (source_id, target_id, relationship_type, strength)
            VALUES (?, ?, ?, ?)
        ''', (source_id, target_id, relationship_type, strength))
        conn.commit()
    logger.info(f"Edge created: {source_id} -> {target_id} ({relationship_type})")

def update_knowledge_graph(new_information: str):
    key_concepts = extract_key_concepts(new_information)
    info_id = hashlib.md5(new_information.encode()).hexdigest()
    for concept in key_concepts:
        create_edge(info_id, concept, "RELATED_TO", 1.0)
    logger.info(f"Updated knowledge graph with new information (ID: {info_id})")

def extract_key_concepts(information: str) -> List[str]:
    words = information.lower().split()
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
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
        return cursor.fetchall()

def analyze_file_pair(file1: Dict[str, Any], file2: Dict[str, Any]) -> List[Tuple[str, float]]:
    logger.info(f"Analyzing file pair:")
    logger.info(f"File 1: {file1}")
    logger.info(f"File 2: {file2}")

    if not file1 or not file2:
        logger.warning("One or both files are empty")
        return []

    categories = []

    if 'content' in file1 and 'content' in file2:
        content_similarity = compare_content(file1['content'], file2['content'])
        logger.info(f"Content similarity: {content_similarity}")
        if content_similarity > 0.3:
            categories.append(("SIMILAR_CONTENT", content_similarity))

    if 'tags' in file1 and 'tags' in file2:
        tag_similarity = compare_tags(file1['tags'], file2['tags'])
        logger.info(f"Tag similarity: {tag_similarity}")
        if tag_similarity > 0:
            categories.append(("SHARED_TAGS", tag_similarity))

    if 'title' in file1 and 'title' in file2:
        title_similarity = compare_titles(file1['title'], file2['title'])
        logger.info(f"Title similarity: {title_similarity}")
        if title_similarity > 0.5:
            categories.append(("RELATED_TOPIC", title_similarity))

    if 'timestamp' in file1 and 'timestamp' in file2:
        time_relation = compare_timestamps(file1['timestamp'], file2['timestamp'])
        logger.info(f"Time relation: {time_relation}")
        if time_relation:
            categories.append(time_relation)

    logger.info(f"Analyzed categories: {categories}")
    return categories

def compare_content(content1: str, content2: str) -> float:
    words1 = set(content1.lower().split())
    words2 = set(content2.lower().split())
    common_words = words1.intersection(words2)
    return len(common_words) / (len(words1) + len(words2) - len(common_words))

def compare_tags(tags1: List[str], tags2: List[str]) -> float:
    common_tags = set(tags1).intersection(set(tags2))
    return len(common_tags) / len(set(tags1).union(set(tags2)))

def compare_titles(title1: str, title2: str) -> float:
    words1 = set(title1.lower().split())
    words2 = set(title2.lower().split())
    common_words = words1.intersection(words2)
    return len(common_words) / (len(words1) + len(words2) - len(common_words))

def compare_timestamps(timestamp1: str, timestamp2: str) -> Tuple[str, float]:
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
