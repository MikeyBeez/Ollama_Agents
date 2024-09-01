import unittest
from unittest.mock import patch, MagicMock
from src.modules.memory_search import search_memories, get_embeddings, find_most_similar

class TestMemorySearch(unittest.TestCase):
    @patch('src.modules.memory_search.get_json_files_in_directory')
    @patch('src.modules.memory_search.get_embeddings')
    @patch('src.modules.memory_search.ollama.embeddings')
    @patch('src.modules.memory_search.read_memory')
    def test_search_memories(self, mock_read_memory, mock_ollama_embeddings, mock_get_embeddings, mock_get_json_files):
        mock_get_json_files.return_value = [MagicMock(name='file1.json'), MagicMock(name='file2.json')]
        mock_get_embeddings.side_effect = [[1, 0, 0], [0, 1, 0]]
        mock_ollama_embeddings.return_value = {"embedding": [1, 1, 0]}
        mock_read_memory.side_effect = [
            {"content": "Memory 1", "type": "interaction", "timestamp": "2023-01-01"},
            {"content": "Memory 2", "type": "document_chunk", "timestamp": "2023-01-02"}
        ]

        results = search_memories("test query", top_k=2, similarity_threshold=0.5)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['content'], "Memory 1")
        self.assertEqual(results[1]['content'], "Memory 2")

    def test_find_most_similar(self):
        needle = [1, 1, 0]
        haystack = [[1, 0, 0], [0, 1, 0], [1, 1, 1]]
        results = find_most_similar(needle, haystack)
        self.assertEqual(len(results), 3)
        self.assertAlmostEqual(results[0][0], 0.8164965809277259, places=7)
        self.assertEqual(results[0][1], 2)  # Index of [1, 1, 1]

if __name__ == '__main__':
    unittest.main()
