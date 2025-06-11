# test_extract_knowledge.py

import unittest
from typing import Dict, Any
from src.modules.knowledge_extraction import extract_knowledge

class TestExtractKnowledge(unittest.TestCase):

    def assert_knowledge_extraction(self, input_text: str, expected_output: Dict[str, Any]):
        result = extract_knowledge(input_text)
        self.assertEqual(result, expected_output)
        print(f"\nInput: {input_text}")
        print(f"Expected Output: {expected_output}")
        print(f"Actual Output: {result}")
        print("=" * 50)

    def test_extract_knowledge_examples(self):
        test_cases = [
            (
                "Apple Inc. was founded by Steve Jobs in California.",
                {
                    "key_concepts": ["Apple Inc.", "Steve Jobs", "California"],
                    "named_entities": [
                        {"text": "Apple Inc.", "label": "ORG"},
                        {"text": "Steve Jobs", "label": "PERSON"},
                        {"text": "California", "label": "GPE"}
                    ],
                    "entities_and_relationships": {
                        "entities": [
                            {"text": "Apple Inc.", "label": "ORG"},
                            {"text": "Steve Jobs", "label": "PERSON"},
                            {"text": "California", "label": "GPE"}
                        ],
                        "relationships": [
                            {"subject": "Steve Jobs", "relationship": "FOUNDED", "object": "Apple Inc."}
                        ]
                    },
                    "query_topic": {"topic": "Technology Company Foundation", "confidence": 0.9},
                    "sentiment": {"sentiment": "neutral", "score": 0.0}
                }
            ),
            (
                "The Eiffel Tower in Paris is a famous landmark.",
                {
                    "key_concepts": ["Eiffel Tower", "Paris", "landmark"],
                    "named_entities": [
                        {"text": "Eiffel Tower", "label": "LOC"},
                        {"text": "Paris", "label": "GPE"}
                    ],
                    "entities_and_relationships": {
                        "entities": [
                            {"text": "Eiffel Tower", "label": "LOC"},
                            {"text": "Paris", "label": "GPE"}
                        ],
                        "relationships": [
                            {"subject": "Eiffel Tower", "relationship": "LOCATED_IN", "object": "Paris"}
                        ]
                    },
                    "query_topic": {"topic": "Famous Landmarks", "confidence": 0.95},
                    "sentiment": {"sentiment": "positive", "score": 0.6}
                }
            ),
            (
                "Python is a popular programming language used in data science.",
                {
                    "key_concepts": ["Python", "programming language", "data science"],
                    "named_entities": [
                        {"text": "Python", "label": "PRODUCT"}
                    ],
                    "entities_and_relationships": {
                        "entities": [
                            {"text": "Python", "label": "PRODUCT"},
                            {"text": "data science", "label": "FIELD"}
                        ],
                        "relationships": [
                            {"subject": "Python", "relationship": "USED_IN", "object": "data science"}
                        ]
                    },
                    "query_topic": {"topic": "Programming Languages", "confidence": 0.9},
                    "sentiment": {"sentiment": "positive", "score": 0.7}
                }
            ),
            (
                "Climate change is causing global temperatures to rise.",
                {
                    "key_concepts": ["climate change", "global temperatures"],
                    "named_entities": [],
                    "entities_and_relationships": {
                        "entities": [
                            {"text": "climate change", "label": "CONCEPT"},
                            {"text": "global temperatures", "label": "MEASURE"}
                        ],
                        "relationships": [
                            {"subject": "climate change", "relationship": "CAUSES", "object": "global temperatures to rise"}
                        ]
                    },
                    "query_topic": {"topic": "Climate Change", "confidence": 0.95},
                    "sentiment": {"sentiment": "negative", "score": 0.6}
                }
            ),
            (
                "The COVID-19 pandemic has affected global health and economy.",
                {
                    "key_concepts": ["COVID-19", "pandemic", "global health", "economy"],
                    "named_entities": [
                        {"text": "COVID-19", "label": "EVENT"}
                    ],
                    "entities_and_relationships": {
                        "entities": [
                            {"text": "COVID-19", "label": "EVENT"},
                            {"text": "global health", "label": "CONCEPT"},
                            {"text": "economy", "label": "CONCEPT"}
                        ],
                        "relationships": [
                            {"subject": "COVID-19 pandemic", "relationship": "AFFECTS", "object": "global health"},
                            {"subject": "COVID-19 pandemic", "relationship": "AFFECTS", "object": "economy"}
                        ]
                    },
                    "query_topic": {"topic": "Global Pandemic Impact", "confidence": 0.95},
                    "sentiment": {"sentiment": "negative", "score": 0.8}
                }
            ),
            (
                "Artificial intelligence is transforming various industries.",
                {
                    "key_concepts": ["artificial intelligence", "industries", "transforming"],
                    "named_entities": [],
                    "entities_and_relationships": {
                        "entities": [
                            {"text": "artificial intelligence", "label": "TECH"},
                            {"text": "industries", "label": "CONCEPT"}
                        ],
                        "relationships": [
                            {"subject": "artificial intelligence", "relationship": "TRANSFORMS", "object": "industries"}
                        ]
                    },
                    "query_topic": {"topic": "AI Impact on Industries", "confidence": 0.9},
                    "sentiment": {"sentiment": "positive", "score": 0.7}
                }
            ),
            (
                "The Great Wall of China is visible from space.",
                {
                    "key_concepts": ["Great Wall of China", "visible", "space"],
                    "named_entities": [
                        {"text": "Great Wall of China", "label": "LOC"}
                    ],
                    "entities_and_relationships": {
                        "entities": [
                            {"text": "Great Wall of China", "label": "LOC"},
                            {"text": "space", "label": "LOC"}
                        ],
                        "relationships": [
                            {"subject": "Great Wall of China", "relationship": "VISIBLE_FROM", "object": "space"}
                        ]
                    },
                    "query_topic": {"topic": "Famous Landmarks", "confidence": 0.9},
                    "sentiment": {"sentiment": "neutral", "score": 0.0}
                }
            ),
            (
                "Renewable energy sources are crucial for combating climate change.",
                {
                    "key_concepts": ["renewable energy", "climate change"],
                    "named_entities": [],
                    "entities_and_relationships": {
                        "entities": [
                            {"text": "renewable energy", "label": "CONCEPT"},
                            {"text": "climate change", "label": "CONCEPT"}
                        ],
                        "relationships": [
                            {"subject": "renewable energy", "relationship": "COMBATS", "object": "climate change"}
                        ]
                    },
                    "query_topic": {"topic": "Renewable Energy and Climate", "confidence": 0.95},
                    "sentiment": {"sentiment": "positive", "score": 0.8}
                }
            ),
            (
                "William Shakespeare wrote many famous plays including Hamlet and Macbeth.",
                {
                    "key_concepts": ["William Shakespeare", "plays", "Hamlet", "Macbeth"],
                    "named_entities": [
                        {"text": "William Shakespeare", "label": "PERSON"},
                        {"text": "Hamlet", "label": "WORK_OF_ART"},
                        {"text": "Macbeth", "label": "WORK_OF_ART"}
                    ],
                    "entities_and_relationships": {
                        "entities": [
                            {"text": "William Shakespeare", "label": "PERSON"},
                            {"text": "Hamlet", "label": "WORK_OF_ART"},
                            {"text": "Macbeth", "label": "WORK_OF_ART"}
                        ],
                        "relationships": [
                            {"subject": "William Shakespeare", "relationship": "WROTE", "object": "Hamlet"},
                            {"subject": "William Shakespeare", "relationship": "WROTE", "object": "Macbeth"}
                        ]
                    },
                    "query_topic": {"topic": "Literature", "confidence": 0.95},
                    "sentiment": {"sentiment": "positive", "score": 0.6}
                }
            ),
            (
                "The human genome contains approximately 3 billion base pairs.",
                {
                    "key_concepts": ["human genome", "base pairs"],
                    "named_entities": [],
                    "entities_and_relationships": {
                        "entities": [
                            {"text": "human genome", "label": "CONCEPT"},
                            {"text": "base pairs", "label": "QUANTITY"}
                        ],
                        "relationships": [
                            {"subject": "human genome", "relationship": "CONTAINS", "object": "3 billion base pairs"}
                        ]
                    },
                    "query_topic": {"topic": "Genetics", "confidence": 0.9},
                    "sentiment": {"sentiment": "neutral", "score": 0.0}
                }
            ),
            # Add more test cases here to reach about 20 examples
        ]

        for input_text, expected_output in test_cases:
            with self.subTest(input_text=input_text):
                self.assert_knowledge_extraction(input_text, expected_output)

if __name__ == '__main__':
    unittest.main(verbosity=2)
