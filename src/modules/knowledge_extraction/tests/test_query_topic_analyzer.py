# src/modules/knowledge_extraction/tests/test_query_topic_analyzer.py

import unittest
from unittest.mock import patch
from src.modules.knowledge_extraction.query_topic_analyzer import analyze_query_topic

class TestQueryTopicAnalyzer(unittest.TestCase):

    @patch('src.modules.knowledge_extraction.query_topic_analyzer.process_prompt')
    def test_analyze_query_topic(self, mock_process_prompt):
        mock_process_prompt.return_value = '{"topic": "Climate Change", "confidence": 0.9, "depth": 4}'

        result = analyze_query_topic("What are the main causes of global warming?", "test_model")

        self.assertEqual(result['topic'], "Climate Change")
        self.assertEqual(result['confidence'], 0.9)
        self.assertEqual(result['depth'], 4)

    @patch('src.modules.knowledge_extraction.query_topic_analyzer.process_prompt')
    def test_analyze_query_topic_error(self, mock_process_prompt):
        mock_process_prompt.side_effect = Exception("API Error")

        result = analyze_query_topic("What are the main causes of global warming?", "test_model")

        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()
