# src/modules/knowledge_extraction/tests/test_text_sentiment_analyzer.py

import unittest
from unittest.mock import patch
from src.modules.knowledge_extraction.text_sentiment_analyzer import analyze_sentiment

class TestTextSentimentAnalyzer(unittest.TestCase):

    @patch('src.modules.knowledge_extraction.text_sentiment_analyzer.process_prompt')
    def test_analyze_sentiment(self, mock_process_prompt):
        mock_process_prompt.return_value = '{"sentiment": "positive", "intensity": 0.8}'

        result = analyze_sentiment("I love this product! It's amazing!")

        self.assertEqual(result['sentiment'], "positive")
        self.assertEqual(result['intensity'], 0.8)

    @patch('src.modules.knowledge_extraction.text_sentiment_analyzer.process_prompt')
    def test_analyze_sentiment_error(self, mock_process_prompt):
        mock_process_prompt.side_effect = Exception("API Error")

        result = analyze_sentiment("I love this product! It's amazing!")

        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()
