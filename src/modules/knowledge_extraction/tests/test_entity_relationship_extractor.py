# src/modules/knowledge_extraction/tests/test_entity_relationship_extractor.py

import unittest
from unittest.mock import patch
from src.modules.knowledge_extraction.entity_relationship_extractor import extract_entities_and_relationships

class TestEntityRelationshipExtractor(unittest.TestCase):

    @patch('src.modules.knowledge_extraction.entity_relationship_extractor.process_prompt')
    def test_extract_entities_and_relationships(self, mock_process_prompt):
        mock_process_prompt.return_value = '''
        {
            "entities": [
                {"text": "John Doe", "label": "PERSON"},
                {"text": "Acme Corp", "label": "ORG"}
            ],
            "relationships": [
                {"subject": "John Doe", "relationship": "WORKS_FOR", "object": "Acme Corp"}
            ]
        }
        '''

        result = extract_entities_and_relationships("John Doe works for Acme Corp")

        self.assertEqual(len(result['entities']), 2)
        self.assertEqual(len(result['relationships']), 1)
        self.assertEqual(result['entities'][0]['text'], "John Doe")
        self.assertEqual(result['relationships'][0]['relationship'], "WORKS_FOR")

    @patch('src.modules.knowledge_extraction.entity_relationship_extractor.process_prompt')
    def test_extract_entities_and_relationships_error(self, mock_process_prompt):
        mock_process_prompt.side_effect = Exception("API Error")

        result = extract_entities_and_relationships("John Doe works for Acme Corp")

        self.assertEqual(result, {})

if __name__ == '__main__':
    unittest.main()
