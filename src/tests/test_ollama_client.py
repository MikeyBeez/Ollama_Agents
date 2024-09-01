import unittest
from unittest.mock import patch, MagicMock
from src.modules.ollama_client import OllamaClient, process_prompt

class TestOllamaClient(unittest.TestCase):
    def setUp(self):
        self.client = OllamaClient()

    @patch('requests.post')
    def test_process_prompt(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.iter_lines.return_value = [
            b'{"response": "Hello", "done": false}',
            b'{"response": " world", "done": false}',
            b'{"response": "!", "done": true}'
        ]
        mock_post.return_value.__enter__.return_value = mock_response

        result = self.client.process_prompt("Hi", "model1", "user1")
        self.assertEqual(result, "Hello world!")

    @patch('src.modules.ollama_client.default_client.process_prompt')
    def test_process_prompt_function(self, mock_client_process):
        mock_client_process.return_value = "Test response"
        result = process_prompt("Test prompt", "model1", "user1")
        self.assertEqual(result, "Test response")
        mock_client_process.assert_called_once_with("Test prompt", "model1", "user1")

if __name__ == '__main__':
    unittest.main()
