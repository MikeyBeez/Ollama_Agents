# src/tests/test_kb_graph.py

import unittest
import sqlite3
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
import logging
from src.modules.kb_graph import (
    create_edge, update_knowledge_graph, extract_key_concepts,
    get_related_nodes, analyze_file_pair, compare_content, compare_tags,
    compare_titles, compare_timestamps
)

class TestKBGraph(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.conn.execute('''
            CREATE TABLE edges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id TEXT NOT NULL,
                target_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,
                strength REAL NOT NULL
            )
        ''')
        self.conn.commit()
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        self.conn.close()

    @patch('src.modules.kb_graph.get_db_connection')
    def test_create_edge(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.conn
        create_edge("A", "B", "RELATED_TO", 0.8)
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM edges")
        result = cursor.fetchone()
        self.assertIsNotNone(result, "No edge was inserted")
        if result:
            self.assertEqual(result[1], "A")
            self.assertEqual(result[2], "B")
            self.assertEqual(result[3], "RELATED_TO")
            self.assertEqual(result[4], 0.8)

    def test_extract_key_concepts(self):
        text = "Python is a programming language. Python is widely used in data science."
        concepts = extract_key_concepts(text)
        self.assertIn("python", concepts)
        self.assertIn("is", concepts)

    @patch('src.modules.kb_graph.get_db_connection')
    def test_get_related_nodes(self, mock_get_db_connection):
        mock_get_db_connection.return_value = self.conn
        create_edge("A", "B", "RELATED_TO", 0.8)
        create_edge("A", "C", "PART_OF", 0.9)
        related = get_related_nodes("A")
        self.assertEqual(len(related), 2)
        self.assertIn(("B", "RELATED_TO", 0.8), related)
        self.assertIn(("C", "PART_OF", 0.9), related)

    @patch('src.modules.kb_graph.compare_content')
    @patch('src.modules.kb_graph.compare_tags')
    @patch('src.modules.kb_graph.compare_titles')
    @patch('src.modules.kb_graph.compare_timestamps')
    def test_analyze_file_pair(self, mock_compare_timestamps, mock_compare_titles, mock_compare_tags, mock_compare_content):
        mock_compare_content.return_value = 0.8
        mock_compare_tags.return_value = 0.6
        mock_compare_titles.return_value = 0.7
        mock_compare_timestamps.return_value = ("TEMPORALLY_CLOSE", 0.9)

        file1 = {
            "title": "Python Basics",
            "content": "Python is a popular programming language used in various fields.",
            "tags": ["python", "programming"],
            "timestamp": "2023-05-01T10:00:00Z"
        }
        file2 = {
            "title": "Python in Data Science",
            "content": "Python is widely used in data science and programming.",
            "tags": ["python", "data science"],
            "timestamp": "2023-05-01T11:00:00Z"
        }
        categories = analyze_file_pair(file1, file2)

        self.assertTrue(any(cat[0] == "SIMILAR_CONTENT" for cat in categories), f"Categories: {categories}")
        self.assertTrue(any(cat[0] == "SHARED_TAGS" for cat in categories))
        self.assertTrue(any(cat[0] == "RELATED_TOPIC" for cat in categories))
        self.assertTrue(any(cat[0] == "TEMPORALLY_CLOSE" for cat in categories))

    def test_analyze_file_pair_empty(self):
        empty_file = {}
        non_empty_file = {
            "title": "Test",
            "content": "Test content",
            "tags": ["test"],
            "timestamp": "2023-05-01T10:00:00Z"
        }

        categories = analyze_file_pair(empty_file, non_empty_file)
        self.assertEqual(categories, [], "Expected empty list for empty file pair")

        categories = analyze_file_pair(non_empty_file, empty_file)
        self.assertEqual(categories, [], "Expected empty list for empty file pair")

        categories = analyze_file_pair(empty_file, empty_file)
        self.assertEqual(categories, [], "Expected empty list for both empty files")

    def test_compare_content(self):
        content1 = "Python is a programming language"
        content2 = "Python is used in data science"
        similarity = compare_content(content1, content2)
        self.assertGreater(similarity, 0)

    def test_compare_tags(self):
        tags1 = ["python", "programming"]
        tags2 = ["python", "data science"]
        similarity = compare_tags(tags1, tags2)
        self.assertGreater(similarity, 0)

    def test_compare_titles(self):
        title1 = "Python Basics"
        title2 = "Python in Data Science"
        similarity = compare_titles(title1, title2)
        self.assertGreater(similarity, 0)

def test_compare_timestamps(self):
    now = datetime.now().isoformat()
    one_hour_later = (datetime.now() + timedelta(hours=1)).isoformat()
    one_day_later = (datetime.now() + timedelta(days=1)).isoformat()
    one_week_later = (datetime.now() + timedelta(weeks=1)).isoformat()
    two_weeks_later = (datetime.now() + timedelta(weeks=2)).isoformat()

    self.assertEqual(compare_timestamps(now, one_hour_later)[0], "TEMPORALLY_CLOSE")
    self.assertEqual(compare_timestamps(now, one_day_later)[0], "SAME_DAY")
    self.assertEqual(compare_timestamps(now, one_week_later)[0], "SAME_WEEK")
    self.assertIsNone(compare_timestamps(now, two_weeks_later))

if __name__ == '__main__':
    unittest.main()
