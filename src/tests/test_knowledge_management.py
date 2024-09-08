# src/tests/test_knowledge_management.py

import unittest
import sqlite3
import os
from datetime import datetime, timedelta
from src.modules.knowledge_management import KnowledgeManager
from src.modules.errors import DataProcessingError
from src.utils.schema import SCHEMA

class TestKnowledgeManager(unittest.TestCase):
    def setUp(self):
        self.test_db_path = 'test_knowledge.db'
        self.knowledge_manager = KnowledgeManager(self.test_db_path)

        # Create test database and tables
        conn = sqlite3.connect(self.test_db_path)
        conn.executescript(SCHEMA)
        conn.close()

    def tearDown(self):
        # Close the connection and remove the test database
        self.knowledge_manager.close_connection()
        os.remove(self.test_db_path)

    def test_add_and_get_edge(self):
        self.knowledge_manager.add_edge("Apple", "Fruit", "is_a", 1.0, confidence=0.95, bidirectional=True)
        related = self.knowledge_manager.get_related_nodes("Apple")
        self.assertEqual(len(related), 1)
        self.assertEqual(related[0], ("Fruit", "is_a", 1.0, 0.95))

    def test_update_edge_strength(self):
        self.knowledge_manager.add_edge("Dog", "Animal", "is_a", 0.8)
        self.knowledge_manager.update_edge_strength("Dog", "Animal", "is_a", 0.9)
        related = self.knowledge_manager.get_related_nodes("Dog")
        self.assertEqual(related[0][2], 0.9)

    def test_add_and_get_node_attribute(self):
        self.knowledge_manager.add_node_attribute("Apple", "color", "red", confidence=0.9)
        attributes = self.knowledge_manager.get_node_attributes("Apple")
        self.assertEqual(len(attributes), 1)
        self.assertEqual(attributes[0], ("color", "red", 0.9))

    def test_add_and_get_hierarchy(self):
        self.knowledge_manager.add_hierarchy("Fruits", "Apple", "category", confidence=1.0)
        children = self.knowledge_manager.get_children("Fruits")
        parents = self.knowledge_manager.get_parents("Apple")
        self.assertEqual(len(children), 1)
        self.assertEqual(len(parents), 1)
        self.assertEqual(children[0], ("Apple", "category", 1.0))
        self.assertEqual(parents[0], ("Fruits", "category", 1.0))

    def test_search_edges(self):
        # Clear the database first
        self.knowledge_manager.conn.execute("DELETE FROM edges")
        self.knowledge_manager.conn.commit()

        now = datetime.now().isoformat()
        future = (datetime.now() + timedelta(days=30)).isoformat()

        self.knowledge_manager.add_edge("A", "B", "relates_to", 0.7, confidence=0.8, start_time=now, end_time=future, bidirectional=True)
        self.knowledge_manager.add_edge("C", "D", "relates_to", 0.6, confidence=0.6)

        results = self.knowledge_manager.search_edges(min_confidence=0.7)
        self.assertEqual(len(results), 2)  # Two entries for the bidirectional edge
        # We'll just check the first result, ignoring the duplicate
        self.assertEqual(results[0]['source_id'], "A")
        self.assertEqual(results[0]['target_id'], "B")
        self.assertEqual(results[0]['confidence'], 0.8)
        self.assertTrue(results[0]['bidirectional'])

        results = self.knowledge_manager.search_edges(start_time=now, end_time=future)
        self.assertEqual(len(results), 2)  # Two entries for the bidirectional edge
        # Again, we'll just check the first result
        self.assertEqual(results[0]['source_id'], "A")
        self.assertEqual(results[0]['target_id'], "B")
        self.assertEqual(results[0]['start_time'], now)
        self.assertEqual(results[0]['end_time'], future)

        # Test that lower confidence edge is not returned
        results = self.knowledge_manager.search_edges(min_confidence=0.7)
        self.assertEqual(len(results), 2)  # Only the bidirectional edge meets the criteria
        self.assertFalse(any(r['source_id'] == "C" and r['target_id'] == "D" for r in results))

        # Test all edges are returned with lower confidence threshold
        results = self.knowledge_manager.search_edges(min_confidence=0.5)
        self.assertEqual(len(results), 3)  # 2 for A-B bidirectional, 1 for C-D
        self.assertTrue(any(r['source_id'] == "C" and r['target_id'] == "D" for r in results))

    def test_edge_metadata(self):
        # Clear the database first
        self.knowledge_manager.conn.execute("DELETE FROM edges")
        self.knowledge_manager.conn.commit()

        metadata = {"source": "test_database", "last_updated": "2023-06-01"}
        self.knowledge_manager.add_edge("X", "Y", "connected_to", 1.0, metadata=metadata)

        results = self.knowledge_manager.search_edges()
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['metadata'], metadata)

    def test_bidirectional_edge(self):
        self.knowledge_manager.add_edge("City", "Town", "similar_to", 0.8, bidirectional=True)
        city_related = self.knowledge_manager.get_related_nodes("City")
        town_related = self.knowledge_manager.get_related_nodes("Town")
        self.assertEqual(len(city_related), 1)
        self.assertEqual(len(town_related), 1)

    def test_error_handling(self):
        with self.assertRaises(DataProcessingError):
            invalid_db = KnowledgeManager("invalid_path.db")
            invalid_db.add_edge("A", "B", "test", 1.0)

if __name__ == '__main__':
    unittest.main()
