# src/tests/test_ollama_client.py

import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os
import requests  # Add this import

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.ollama_client import OllamaClient, process_prompt

class TestOllamaClient(unittest.TestCase):

    def setUp(self):
        self.client = OllamaClient()

    @patch('requests.post')
    def test_process_prompt_success(self, mock_post):
        # Mock the streaming response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [
            json.dumps({"response": "Hello"}).encode(),
            json.dumps({"response": " world"}).encode(),
            json.dumps({"response": "!", "done": True}).encode()
        ]
        mock_post.return_value.__enter__.return_value = mock_response

        result = self.client.process_prompt("Hi", "test_model", "test_user")
        self.assertEqual(result, "Hello world!")

    @patch('requests.post')
    def test_process_prompt_api_error(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value.__enter__.return_value = mock_response

        result = self.client.process_prompt("Hi", "test_model", "test_user")
        self.assertTrue(result.startswith("Error: Received status code 500"))

    @patch('requests.post')
    def test_process_prompt_connection_error(self, mock_post):
        mock_post.side_effect = requests.RequestException("Connection error")

        result = self.client.process_prompt("Hi", "test_model", "test_user")
        self.assertTrue(result.startswith("Error connecting to Ollama"))

    @patch('src.modules.ollama_client.default_client.process_prompt')
    def test_process_prompt_function(self, mock_client_process):
        mock_client_process.return_value = "Test response"
        result = process_prompt("Test prompt", "test_model", "test_user")
        self.assertEqual(result, "Test response")
        mock_client_process.assert_called_once_with("Test prompt", "test_model", "test_user")

if __name__ == '__main__':
    unittest.main()
