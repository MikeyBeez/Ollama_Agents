import unittest
from unittest.mock import patch, MagicMock
from src.modules.save_history import ChatHistory, save_memory, save_interaction, save_document_chunk

class TestSaveHistory(unittest.TestCase):
    def setUp(self):
        self.chat_history = ChatHistory()
        self.chat_history.history = []

    def test_add_entry(self):
        self.chat_history.add_entry("Hello", "Hi there!")
        self.assertEqual(len(self.chat_history.history), 1)
        self.assertEqual(self.chat_history.history[0]["prompt"], "Hello")
        self.assertEqual(self.chat_history.history[0]["response"], "Hi there!")

    @patch('src.modules.save_history.write_json_file')
    def test_save_history(self, mock_write_json_file):
        self.chat_history.add_entry("Test", "Response")
        mock_write_json_file.reset_mock()  # Reset the mock before save_history
        self.chat_history.save_history()
        mock_write_json_file.assert_called_once()

    @patch('src.modules.save_history.read_json_file')
    def test_load_history(self, mock_read_json_file):
        mock_read_json_file.return_value = [{"prompt": "Test", "response": "Response"}]
        self.chat_history.load_history()
        self.assertEqual(len(self.chat_history.history), 1)
        self.assertEqual(self.chat_history.history[0]["prompt"], "Test")

    @patch('src.modules.save_history.write_json_file')
    @patch('src.modules.save_history.ensure_directory_exists')
    def test_save_memory(self, mock_ensure_dir, mock_write_json_file):
        save_memory("test", "content", "user", "model")
        mock_ensure_dir.assert_called_once()
        mock_write_json_file.assert_called_once()

    @patch('src.modules.save_history.save_memory')
    def test_save_interaction(self, mock_save_memory):
        save_interaction("Hello", "Hi", "user", "model")
        mock_save_memory.assert_called_once_with("interaction", {"prompt": "Hello", "response": "Hi"}, "user", "model")

    @patch('src.modules.save_history.save_memory')
    def test_save_document_chunk(self, mock_save_memory):
        save_document_chunk("chunk1", "content", "user", "model")
        mock_save_memory.assert_called_once_with("document_chunk", "content", "user", "model", {"chunk_id": "chunk1"})

if __name__ == '__main__':
    unittest.main()
