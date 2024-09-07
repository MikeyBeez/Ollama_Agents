# src/tests/test_helper_relationship_extraction.py

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.helper_relationship_extraction import extract_relationships

class TestHelperRelationshipExtraction(unittest.TestCase):
    def setUp(self):
        self.sample_context = "The cat chased the mouse. John gave Mary a book."
        self.sample_entities = ["cat", "mouse", "John", "Mary", "book"]

    def test_extract_relationships(self):
        relationships = extract_relationships(self.sample_context, self.sample_entities)

        self.assertIsInstance(relationships, list)
        self.assertTrue(len(relationships) > 0, "No relationships extracted")

        # Print actual relationships for debugging
        print("Actual relationships found:")
        for r in relationships:
            print(f"  {r}")

        # Check for specific relationships
        expected_relationships = [
            {"source": "cat", "target": "mouse", "relationship": "chase"},
            {"source": "John", "target": "Mary", "relationship": "give"},
            {"source": "John", "target": "book", "relationship": "give"}
        ]

        for expected in expected_relationships:
            self.assertTrue(
                any(
                    r["source"].lower() == expected["source"].lower() and
                    r["target"].lower() == expected["target"].lower() and
                    r["relationship"] == expected["relationship"]
                    for r in relationships
                ),
                f"Expected relationship not found: {expected}"
            )

    def test_extract_relationships_empty_input(self):
        relationships = extract_relationships("", [])
        self.assertEqual(relationships, [])

    def test_extract_relationships_no_entities(self):
        relationships = extract_relationships(self.sample_context, [])
        self.assertEqual(relationships, [])

    def test_extract_relationships_complex_sentence(self):
        complex_context = "The big brown dog quickly jumped over the lazy fox in the green garden."
        entities = ["dog", "fox", "garden"]
        relationships = extract_relationships(complex_context, entities)

        self.assertIsInstance(relationships, list)
        self.assertTrue(len(relationships) > 0, "No relationships extracted from complex sentence")

        # Check for a specific relationship
        self.assertTrue(
            any(
                r["source"].lower() == "dog" and
                r["target"].lower() == "fox" and
                "jump" in r["relationship"].lower()
                for r in relationships
            ),
            "Expected 'dog jumped fox' relationship not found"
        )

        # Check for the 'in' relationship
        self.assertTrue(
            any(
                r["source"].lower() == "dog" and
                r["target"].lower() == "garden" and
                "in" in r["relationship"].lower()
                for r in relationships
            ),
            "Expected 'dog in garden' relationship not found"
        )

if __name__ == '__main__':
    unittest.main()
