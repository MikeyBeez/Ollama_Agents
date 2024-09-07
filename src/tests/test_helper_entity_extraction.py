# src/tests/test_helper_entity_extraction.py

import unittest
from src.modules.helper_entity_extraction import EntityExtractionHelper

class TestEntityExtractionHelper(unittest.TestCase):
    def setUp(self):
        self.extractor = EntityExtractionHelper()

    def test_helper_extract_entities(self):
        test_cases = [
            ("Apple Inc. released a new iPhone model in California last week.",
             {"Apple Inc.", "iPhone", "California", "a new iPhone model"}),
            ("CEO Tim Cook announced the new product during a special event.",
             {"Tim Cook", "the new product", "CEO Tim Cook", "a special event"}),
            ("Microsoft and Google are competing in the AI market, while researchers at MIT are making breakthroughs.",
             {"the AI market", "MIT", "Google", "researchers", "Microsoft", "breakthroughs", "AI"}),
            ("The quick brown fox jumps over the lazy dog.",
             {"The quick brown fox", "the lazy dog"})
        ]

        for i, (context, expected) in enumerate(test_cases, start=1):
            with self.subTest(f"Test case {i}"):
                result = set(self.extractor.helper_extract_entities(context))
                print(f"\nTest case {i}:")
                print(f"Context: {context}")
                print(f"Expected: {expected}")
                print(f"Result:   {result}")
                self.assertSetEqual(result, expected)

    def test_helper_extract_entities_empty_input(self):
        # Test case 5: Empty input
        context5 = ""
        expected5 = set()
        result5 = set(self.extractor.helper_extract_entities(context5))
        self.assertSetEqual(result5, expected5)

if __name__ == '__main__':
    unittest.main()
