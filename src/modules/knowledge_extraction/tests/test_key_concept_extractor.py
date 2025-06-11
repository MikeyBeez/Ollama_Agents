# src/modules/knowledge_extraction/tests/test_key_concept_extractor.py

import unittest
from unittest.mock import patch, Mock
from src.modules.knowledge_extraction.key_concept_extractor import extract_key_concepts

class TestKeyConceptExtractor(unittest.TestCase):

    @patch('src.modules.knowledge_extraction.key_concept_extractor.process_prompt')
    @patch('src.modules.knowledge_extraction.key_concept_extractor.extract_json_from_response')
    @patch('src.modules.knowledge_extraction.key_concept_extractor.parse_list_response')
    def test_extract_key_concepts(self, mock_parse_list_response, mock_extract_json, mock_process_prompt):
        # Arrange
        input_text = "AI and ML are subfields of computer science that focus on creating intelligent machines."
        mock_response = '["Artificial Intelligence", "Machine Learning", "Neural Networks"]'
        expected_concepts = ["artificial intelligence", "machine learning", "neural networks"]

        mock_process_prompt.return_value = mock_response
        mock_extract_json.return_value = ["Artificial Intelligence", "Machine Learning", "Neural Networks"]
        mock_parse_list_response.return_value = ["Artificial Intelligence", "Machine Learning", "Neural Networks"]

        # Act
        result = extract_key_concepts(input_text)

        # Assert
        print("\n----- test_extract_key_concepts -----")
        print(f"Input text: {input_text}")
        print(f"Mock response: {mock_response}")
        print(f"Mock extracted JSON: {mock_extract_json.return_value}")
        print(f"Mock parsed list: {mock_parse_list_response.return_value}")
        print(f"Expected concepts: {expected_concepts}")
        print(f"Actual result: {result}")
        print(f"Result length: {len(result)}")
        print("-------------------------------------")

        self.assertEqual(len(result), 3, f"Expected 3 concepts, but got {len(result)}")
        for concept in expected_concepts:
            self.assertIn(concept, result, f"Expected '{concept}' in results, but it was not found")

        mock_process_prompt.assert_called_once()
        mock_extract_json.assert_called_once_with(mock_response)
        mock_parse_list_response.assert_called_once_with(mock_response)

    @patch('src.modules.knowledge_extraction.key_concept_extractor.process_prompt')
    def test_extract_key_concepts_error(self, mock_process_prompt):
        # Arrange
        input_text = "AI and ML are subfields of computer science."
        mock_process_prompt.side_effect = Exception("API Error")

        # Act
        result = extract_key_concepts(input_text)

        # Assert
        print("\n----- test_extract_key_concepts_error -----")
        print(f"Input text: {input_text}")
        print(f"Expected error: API Error")
        print(f"Actual result: {result}")
        print("-------------------------------------")

        self.assertEqual(result, [], "Expected an empty list when an error occurs")

if __name__ == '__main__':
    unittest.main()
