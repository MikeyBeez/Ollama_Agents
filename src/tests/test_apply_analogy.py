# src/tests/test_apply_analogy.py

import unittest
from unittest.mock import patch
import json
from src.modules.apply_analogy import apply_analogy

class TestApplyAnalogy(unittest.TestCase):

    @patch('src.modules.apply_analogy.process_prompt')
    def test_apply_analogy(self, mock_process_prompt):
        # Mock the response from the language model
        mock_response = json.dumps({
            "applied_analogy": "Just as a computer processes information through its CPU, the human brain processes information through neurons. Memory in computers is analogous to human memory, with short-term memory similar to RAM and long-term memory similar to hard drive storage.",
            "key_insights": [
                "Information processing is a fundamental aspect of both computers and brains",
                "Both systems have mechanisms for short-term and long-term information storage",
                "The speed and capacity of information processing can vary in both systems"
            ],
            "implications": [
                {
                    "implication": "Techniques for optimizing computer performance might inspire cognitive enhancement strategies",
                    "relevance": "High"
                },
                {
                    "implication": "Understanding computer architecture could provide insights into brain function",
                    "relevance": "Medium"
                }
            ],
            "analogy_strength": "Moderate",
            "analogy_limitations": [
                "Brains are much more complex and adaptable than current computers",
                "The biological basis of cognition differs significantly from electronic computation"
            ],
            "potential_issues": [
                "Oversimplification of brain functions",
                "Ignoring the role of emotions and consciousness in human cognition"
            ],
            "novel_predictions": [
                "Parallel processing in computers might reflect how the brain processes multiple stimuli simultaneously",
                "Brain's plasticity might be analogous to AI's ability to learn and adapt"
            ],
            "suggested_refinements": [
                "Incorporate the concept of neuroplasticity in the analogy",
                "Consider the role of interconnectedness in neural networks"
            ],
            "overall_assessment": "The computer-brain analogy provides valuable insights into information processing and storage mechanisms. While it has limitations due to the complexity of biological systems, it serves as a useful model for understanding certain aspects of cognition and may inspire new approaches in both neuroscience and computer science."
        })
        mock_process_prompt.return_value = mock_response

        # Test input
        source_domain = "Computer systems with CPU and memory components"
        target_domain = "Human brain and cognitive processes"
        analogy_mapping = {
            "CPU": "Neurons",
            "RAM": "Short-term memory",
            "Hard Drive": "Long-term memory",
            "Data": "Information/Knowledge"
        }

        # Apply analogy
        result = apply_analogy(source_domain, target_domain, analogy_mapping)

        # Assertions
        self.assertIsNotNone(result['applied_analogy'])
        self.assertGreater(len(result['key_insights']), 0)
        self.assertGreater(len(result['implications']), 0)
        self.assertIn(result['analogy_strength'], ["Strong", "Moderate", "Weak"])
        self.assertGreater(len(result['analogy_limitations']), 0)
        self.assertGreater(len(result['potential_issues']), 0)
        self.assertGreater(len(result['novel_predictions']), 0)
        self.assertGreater(len(result['suggested_refinements']), 0)
        self.assertIsNotNone(result['overall_assessment'])

        # Check the structure of implications
        for implication in result['implications']:
            self.assertIn('implication', implication)
            self.assertIn('relevance', implication)
            self.assertIn(implication['relevance'], ["High", "Medium", "Low"])

        # Verify that process_prompt was called with the correct arguments
        mock_process_prompt.assert_called_once()
        call_args = mock_process_prompt.call_args[0]
        self.assertIn("Source Domain:", call_args[0])
        self.assertIn("Target Domain:", call_args[0])
        self.assertIn("Analogy Mapping:", call_args[0])
        self.assertEqual(call_args[1], "llama3.1:latest")
        self.assertEqual(call_args[2], "AnalogyApplier")

if __name__ == '__main__':
    unittest.main()
