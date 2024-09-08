# src/tests/test_abstract_concept.py

import unittest
from unittest.mock import patch
import json
from src.modules.abstract_concept import abstract_concept

class TestAbstractConcept(unittest.TestCase):

    @patch('src.modules.abstract_concept.process_prompt')
    def test_abstract_concept(self, mock_process_prompt):
        # Mock the response from the language model
        mock_response = json.dumps({
            "abstract_concept": "Resilience in the face of adversity",
            "key_features": [
                "Persistence despite challenges",
                "Adaptability to changing circumstances",
                "Maintaining core functionality under stress"
            ],
            "generalization_process": "The abstraction was derived by identifying the common themes of persistence and adaptation in the face of difficult circumstances, which are present in both the tree's growth and broader life challenges.",
            "abstraction_level": "Medium",
            "potential_applications": [
                "Personal development and psychology",
                "Organizational management",
                "Ecological conservation",
                "Engineering and design of robust systems"
            ],
            "related_concepts": [
                "Adaptability",
                "Perseverance",
                "Antifragility",
                "Homeostasis"
            ],
            "examples": [
                {
                    "example": "A startup pivoting its business model in response to market changes",
                    "explanation": "Demonstrates adaptability and persistence in a challenging business environment"
                },
                {
                    "example": "An athlete recovering from a major injury to compete again",
                    "explanation": "Shows resilience in overcoming physical and mental obstacles"
                }
            ],
            "limitations": [
                "May not apply in situations where adaptation is impossible or harmful",
                "Could potentially glorify struggle without acknowledging systemic issues"
            ],
            "cross_domain_relevance": [
                {
                    "domain": "Computer Science",
                    "relevance": "Designing fault-tolerant systems that can operate under various conditions"
                },
                {
                    "domain": "Social Sciences",
                    "relevance": "Studying community resilience in the face of natural disasters or social upheavals"
                }
            ],
            "abstraction_hierarchy": {
                "more_abstract": ["Adaptability of complex systems", "Universal principles of survival"],
                "more_concrete": ["Specific biological adaptations", "Individual coping mechanisms"]
            },
            "overall_assessment": "The concept of resilience in the face of adversity is a powerful abstraction with wide-ranging applications across multiple domains. It captures the essence of how systems, whether biological, social, or artificial, can maintain their integrity and even thrive under challenging conditions. This abstraction provides a valuable framework for understanding and developing strategies for dealing with difficulties in various contexts."
        })
        mock_process_prompt.return_value = mock_response

        # Test input
        concrete_example = "A tree growing through a crack in a concrete sidewalk, its roots adapting to the urban environment while still reaching for sunlight."
        context = "Urban ecology and the adaptability of nature"

        # Generate abstract concept
        result = abstract_concept(concrete_example, context)

        # Assertions
        self.assertIsNotNone(result['abstract_concept'])
        self.assertGreater(len(result['key_features']), 0)
        self.assertIsNotNone(result['generalization_process'])
        self.assertIn(result['abstraction_level'], ["High", "Medium", "Low"])
        self.assertGreater(len(result['potential_applications']), 0)
        self.assertGreater(len(result['related_concepts']), 0)
        self.assertGreater(len(result['examples']), 0)
        self.assertGreater(len(result['limitations']), 0)
        self.assertGreater(len(result['cross_domain_relevance']), 0)
        self.assertIn('more_abstract', result['abstraction_hierarchy'])
        self.assertIn('more_concrete', result['abstraction_hierarchy'])
        self.assertIsNotNone(result['overall_assessment'])

        # Check the structure of examples
        for example in result['examples']:
            self.assertIn('example', example)
            self.assertIn('explanation', example)

        # Check the structure of cross_domain_relevance
        for relevance in result['cross_domain_relevance']:
            self.assertIn('domain', relevance)
            self.assertIn('relevance', relevance)

        # Verify that process_prompt was called with the correct arguments
        mock_process_prompt.assert_called_once()
        call_args = mock_process_prompt.call_args[0]
        self.assertIn("Concrete Example:", call_args[0])
        self.assertIn("Additional Context", call_args[0])
        self.assertEqual(call_args[1], "llama3.1:latest")
        self.assertEqual(call_args[2], "ConceptAbstractor")

if __name__ == '__main__':
    unittest.main()
