# src/tests/test_perform_inductive_reasoning.py

import unittest
from unittest.mock import patch
import json
from src.modules.perform_inductive_reasoning import perform_inductive_reasoning

class TestPerformInductiveReasoning(unittest.TestCase):

    @patch('src.modules.perform_inductive_reasoning.process_prompt')
    def test_perform_inductive_reasoning(self, mock_process_prompt):
        # Mock the response from the language model
        mock_response = json.dumps({
            "inductive_strength": "Moderate",
            "explanation": "The observations provide some support for the hypothesis, but there are limitations.",
            "supporting_factors": ["Consistent pattern in observations", "Large sample size"],
            "limitations": ["Limited diversity in samples", "Potential confounding variables"],
            "potential_counterexamples": ["Exceptions in extreme conditions"],
            "additional_comments": "Further research needed to strengthen the conclusion."
        })
        mock_process_prompt.return_value = mock_response

        # Test input
        observations = [
            "Swan 1 is white.",
            "Swan 2 is white.",
            "Swan 3 is white.",
            "Swan 4 is white.",
            "Swan 5 is white."
        ]
        hypothesis = "All swans are white."

        # Perform the inductive reasoning
        result = perform_inductive_reasoning(observations, hypothesis)

        # Assertions
        self.assertEqual(result['inductive_strength'], "Moderate")
        self.assertIn("some support", result['explanation'].lower())
        self.assertGreater(len(result['supporting_factors']), 0)
        self.assertGreater(len(result['limitations']), 0)
        self.assertGreater(len(result['potential_counterexamples']), 0)
        self.assertIsNotNone(result['additional_comments'])

        # Verify that process_prompt was called with the correct arguments
        mock_process_prompt.assert_called_once()
        call_args = mock_process_prompt.call_args[0]
        self.assertIn("Observations:", call_args[0])
        self.assertIn("Proposed Hypothesis:", call_args[0])
        self.assertEqual(call_args[1], "llama3.1:latest")
        self.assertEqual(call_args[2], "InductiveReasoner")

if __name__ == '__main__':
    unittest.main()
