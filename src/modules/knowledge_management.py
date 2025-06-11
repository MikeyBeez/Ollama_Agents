# src/modules/knowledge_management.py

import sqlite3
import json
from typing import List, Tuple, Dict, Any
from src.modules.errors import DataProcessingError

class KnowledgeManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = self._get_connection()

    def _get_connection(self):
        try:
            return sqlite3.connect(self.db_path)
        except sqlite3.Error as e:
            raise DataProcessingError(f"Failed to connect to database: {str(e)}")

    def close_connection(self):
        if self.conn:
            self.conn.close()

    def add_edge(self, source_id: str, target_id: str, relationship_type: str, strength: float,
                 confidence: float = 1.0, bidirectional: bool = False,
                 start_time: str = None, end_time: str = None, metadata: Dict[str, Any] = None):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO edges
                (source_id, target_id, relationship_type, strength, confidence, bidirectional, start_time, end_time, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (source_id, target_id, relationship_type, strength, confidence, bidirectional,
                  start_time, end_time, json.dumps(metadata) if metadata else None))
            self.conn.commit()
        except sqlite3.Error as e:
            raise DataProcessingError(f"Failed to add edge: {str(e)}")

    def get_related_nodes(self, node_id: str, relationship_type: str = None) -> List[Tuple[str, str, float, float]]:
        try:
            cursor = self.conn.cursor()
            if relationship_type:
                cursor.execute("""
                    SELECT target_id, relationship_type, strength, confidence
                    FROM edges
                    WHERE source_id = ? AND relationship_type = ?
                    UNION
                    SELECT source_id, relationship_type, strength, confidence
                    FROM edges
                    WHERE target_id = ? AND relationship_type = ? AND bidirectional = 1
                """, (node_id, relationship_type, node_id, relationship_type))
            else:
                cursor.execute("""
                    SELECT target_id, relationship_type, strength, confidence
                    FROM edges
                    WHERE source_id = ?
                    UNION
                    SELECT source_id, relationship_type, strength, confidence
                    FROM edges
                    WHERE target_id = ? AND bidirectional = 1
                """, (node_id, node_id))
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise DataProcessingError(f"Failed to get related nodes: {str(e)}")

    def update_edge_strength(self, source_id: str, target_id: str, relationship_type: str, new_strength: float):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                UPDATE edges
                SET strength = ?, updated_at = CURRENT_TIMESTAMP
                WHERE source_id = ? AND target_id = ? AND relationship_type = ?
            """, (new_strength, source_id, target_id, relationship_type))
            self.conn.commit()
        except sqlite3.Error as e:
            raise DataProcessingError(f"Failed to update edge strength: {str(e)}")

    def add_node_attribute(self, node_id: str, attribute_name: str, attribute_value: str, confidence: float = 1.0):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO node_attributes
                (node_id, attribute_name, attribute_value, confidence)
                VALUES (?, ?, ?, ?)
            """, (node_id, attribute_name, attribute_value, confidence))
            self.conn.commit()
        except sqlite3.Error as e:
            raise DataProcessingError(f"Failed to add node attribute: {str(e)}")

    def get_node_attributes(self, node_id: str) -> List[Tuple[str, str, float]]:
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT attribute_name, attribute_value, confidence
                FROM node_attributes
                WHERE node_id = ?
            """, (node_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise DataProcessingError(f"Failed to get node attributes: {str(e)}")

    def add_hierarchy(self, parent_id: str, child_id: str, hierarchy_type: str, confidence: float = 1.0):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO hierarchies
                (parent_id, child_id, hierarchy_type, confidence)
                VALUES (?, ?, ?, ?)
            """, (parent_id, child_id, hierarchy_type, confidence))
            self.conn.commit()
        except sqlite3.Error as e:
            raise DataProcessingError(f"Failed to add hierarchy: {str(e)}")

    def get_children(self, parent_id: str, hierarchy_type: str = None) -> List[Tuple[str, str, float]]:
        try:
            cursor = self.conn.cursor()
            if hierarchy_type:
                cursor.execute("""
                    SELECT child_id, hierarchy_type, confidence
                    FROM hierarchies
                    WHERE parent_id = ? AND hierarchy_type = ?
                """, (parent_id, hierarchy_type))
            else:
                cursor.execute("""
                    SELECT child_id, hierarchy_type, confidence
                    FROM hierarchies
                    WHERE parent_id = ?
                """, (parent_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise DataProcessingError(f"Failed to get children: {str(e)}")

    def get_parents(self, child_id: str, hierarchy_type: str = None) -> List[Tuple[str, str, float]]:
        try:
            cursor = self.conn.cursor()
            if hierarchy_type:
                cursor.execute("""
                    SELECT parent_id, hierarchy_type, confidence
                    FROM hierarchies
                    WHERE child_id = ? AND hierarchy_type = ?
                """, (child_id, hierarchy_type))
            else:
                cursor.execute("""
                    SELECT parent_id, hierarchy_type, confidence
                    FROM hierarchies
                    WHERE child_id = ?
                """, (child_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            raise DataProcessingError(f"Failed to get parents: {str(e)}")

    def search_edges(self, start_time: str = None, end_time: str = None, min_confidence: float = 0.0) -> List[Dict[str, Any]]:
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT source_id, target_id, relationship_type, strength, confidence, bidirectional, start_time, end_time, metadata
                FROM edges
                WHERE confidence >= ?
            """
            params = [min_confidence]
            if start_time:
                query += " AND (start_time IS NULL OR start_time >= ?)"
                params.append(start_time)
            if end_time:
                query += " AND (end_time IS NULL OR end_time <= ?)"
                params.append(end_time)

            cursor.execute(query, params)
            rows = cursor.fetchall()
            results = []
            for row in rows:
                edge = {
                    "source_id": row[0],
                    "target_id": row[1],
                    "relationship_type": row[2],
                    "strength": row[3],
                    "confidence": row[4],
                    "bidirectional": bool(row[5]),
                    "start_time": row[6],
                    "end_time": row[7],
                    "metadata": json.loads(row[8]) if row[8] else None
                }
                results.append(edge)
                if edge["bidirectional"]:
                    reverse_edge = edge.copy()
                    reverse_edge["source_id"], reverse_edge["target_id"] = edge["target_id"], edge["source_id"]
                    results.append(reverse_edge)
            return results
        except sqlite3.Error as e:
            raise DataProcessingError(f"Failed to search edges: {str(e)}")
