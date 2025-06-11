# src/modules/knowledge_extraction/tests/test_named_entity_recognizer.py

import unittest
from unittest.mock import patch, Mock
from src.modules.knowledge_extraction.named_entity_recognizer import extract_named_entities

class TestNamedEntityRecognizer(unittest.TestCase):

    @patch('src.modules.knowledge_extraction.named_entity_recognizer.process_prompt')
    @patch('src.modules.knowledge_extraction.named_entity_recognizer.extract_json_from_response')
    @patch('src.modules.knowledge_extraction.named_entity_recognizer.parse_list_response')
    def test_extract_named_entities(self, mock_parse_list_response, mock_extract_json, mock_process_prompt):
        # Arrange
        input_text = "Apple Inc. was founded by Steve Jobs in California."
        mock_response = '[{"text": "Apple Inc.", "label": "ORG"}, {"text": "Steve Jobs", "label": "PERSON"}, {"text": "California", "label": "GPE"}]'
        expected_entities = [
            {"text": "Apple Inc.", "label": "ORG"},
            {"text": "Steve Jobs", "label": "PERSON"},
            {"text": "California", "label": "GPE"}
        ]

        mock_process_prompt.return_value = mock_response
        mock_extract_json.return_value = expected_entities
        mock_parse_list_response.return_value = expected_entities

        # Act
        result = extract_named_entities(input_text)

        # Assert
        print("\n----- test_extract_named_entities -----")
        print(f"Input text: {input_text}")
        print(f"Mock response: {mock_response}")
        print(f"Mock extracted JSON: {mock_extract_json.return_value}")
        print(f"Mock parsed list: {mock_parse_list_response.return_value}")
        print(f"Expected entities: {expected_entities}")
        print(f"Actual result: {result}")
        print(f"Result length: {len(result)}")
        print("-------------------------------------")

        self.assertEqual(len(result), 3, f"Expected 3 entities, but got {len(result)}")
        self.assertEqual(result, expected_entities)

        mock_process_prompt.assert_called_once()
        mock_extract_json.assert_called_once_with(mock_response)
        mock_parse_list_response.assert_called_once_with(mock_response)

    @patch('src.modules.knowledge_extraction.named_entity_recognizer.process_prompt')
    def test_extract_named_entities_error(self, mock_process_prompt):
        # Arrange
        input_text = "This is a test sentence."
        mock_process_prompt.side_effect = Exception("API Error")

        # Act
        result = extract_named_entities(input_text)

        # Assert
        print("\n----- test_extract_named_entities_error -----")
        print(f"Input text: {input_text}")
        print(f"Expected error: API Error")
        print(f"Actual result: {result}")
        print("-------------------------------------")

        self.assertEqual(result, [], "Expected an empty list when an error occurs")

if __name__ == '__main__':
    unittest.main()
