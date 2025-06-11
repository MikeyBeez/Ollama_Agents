# src/tests/test_knowledge_extraction.py

import unittest
from unittest.mock import patch, Mock
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.knowledge_extraction import extract_knowledge

class TestKnowledgeExtraction(unittest.TestCase):

    @patch('src.modules.knowledge_extraction.extract_key_concepts')
    @patch('src.modules.knowledge_extraction.extract_named_entities')
    @patch('src.modules.knowledge_extraction.extract_entities_and_relationships')
    @patch('src.modules.knowledge_extraction.analyze_query_topic')
    @patch('src.modules.knowledge_extraction.analyze_sentiment')
    def test_extract_knowledge_success(self, mock_sentiment, mock_topic, mock_entities_rel, mock_named_entities, mock_key_concepts):
        # Arrange
        test_text = "Apple Inc. was founded by Steve Jobs in California. The company revolutionized the smartphone industry with the iPhone."

        mock_key_concepts.return_value = ["Apple Inc.", "Steve Jobs", "iPhone"]
        mock_named_entities.return_value = [
            {"text": "Apple Inc.", "label": "ORG"},
            {"text": "Steve Jobs", "label": "PERSON"},
            {"text": "California", "label": "GPE"}
        ]
        mock_entities_rel.return_value = {
            "entities": [
                {"text": "Apple Inc.", "label": "ORG"},
                {"text": "Steve Jobs", "label": "PERSON"},
                {"text": "California", "label": "GPE"}
            ],
            "relationships": [
                {"subject": "Steve Jobs", "relationship": "FOUNDED", "object": "Apple Inc."}
            ]
        }
        mock_topic.return_value = {"topic": "Technology", "confidence": 0.9}
        mock_sentiment.return_value = {"sentiment": "positive", "score": 0.8}

        # Act
        result = extract_knowledge(test_text)

        # Assert
        self.assertEqual(result['key_concepts'], ["Apple Inc.", "Steve Jobs", "iPhone"])
        self.assertEqual(len(result['named_entities']), 3)
        self.assertEqual(len(result['entities_and_relationships']['entities']), 3)
        self.assertEqual(len(result['entities_and_relationships']['relationships']), 1)
        self.assertEqual(result['query_topic'], {"topic": "Technology", "confidence": 0.9})
        self.assertEqual(result['sentiment'], {"sentiment": "positive", "score": 0.8})

        # Verify that all mock functions were called
        mock_key_concepts.assert_called_once_with(test_text)
        mock_named_entities.assert_called_once_with(test_text)
        mock_entities_rel.assert_called_once_with(test_text)
        mock_topic.assert_called_once_with(test_text)
        mock_sentiment.assert_called_once_with(test_text)

    @patch('src.modules.knowledge_extraction.extract_key_concepts')
    def test_extract_knowledge_partial_failure(self, mock_key_concepts):
        # Arrange
        test_text = "This is a test text."
        mock_key_concepts.side_effect = Exception("Test exception")

        # Act
        result = extract_knowledge(test_text)

        # Assert
        self.assertIn('error', result)
        self.assertEqual(result['key_concepts'], [])
        self.assertEqual(result['named_entities'], [])
        self.assertEqual(result['entities_and_relationships'], {"entities": [], "relationships": []})
        self.assertEqual(result['query_topic'], {})
        self.assertEqual(result['sentiment'], {})

    def test_extract_knowledge_empty_input(self):
        # Arrange
        test_text = ""

        # Act
        result = extract_knowledge(test_text)

        # Assert
        self.assertEqual(result['key_concepts'], [])
        self.assertEqual(result['named_entities'], [])
        self.assertEqual(result['entities_and_relationships'], {"entities": [], "relationships": []})
        self.assertEqual(result['query_topic'], {})
        self.assertEqual(result['sentiment'], {})

if __name__ == '__main__':
    unittest.main()
