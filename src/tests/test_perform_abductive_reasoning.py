# src/tests/test_perform_abductive_reasoning.py

import unittest
from unittest.mock import patch
import json
from src.modules.perform_abductive_reasoning import perform_abductive_reasoning

class TestPerformAbductiveReasoning(unittest.TestCase):

    @patch('src.modules.perform_abductive_reasoning.process_prompt')
    def test_perform_abductive_reasoning(self, mock_process_prompt):
        # Mock the response from the language model
        mock_response = json.dumps({
            "best_explanation": "The patient has the flu",
            "best_explanation_likelihood": "High",
            "explanation_analysis": [
                {
                    "explanation": "The patient has the flu",
                    "likelihood": "High",
                    "supporting_factors": ["Matches common flu symptoms", "It's flu season"],
                    "weaknesses": ["Could be confused with other respiratory infections"]
                },
                {
                    "explanation": "The patient has allergies",
                    "likelihood": "Low",
                    "supporting_factors": ["Some symptoms overlap with allergies"],
                    "weaknesses": ["Fever is not typical for allergies", "Sudden onset is atypical for allergies"]
                }
            ],
            "additional_comments": "While the flu is the most likely explanation, a medical examination is recommended for a definitive diagnosis."
        })
        mock_process_prompt.return_value = mock_response

        # Test input
        observation = "The patient has a fever, body aches, and a cough."
        possible_explanations = [
            "The patient has the flu",
            "The patient has allergies",
            "The patient has a common cold"
        ]

        # Perform the abductive reasoning
        result = perform_abductive_reasoning(observation, possible_explanations)

        # Assertions
        self.assertEqual(result['best_explanation'], "The patient has the flu")
        self.assertEqual(result['best_explanation_likelihood'], "High")
        self.assertEqual(len(result['explanation_analysis']), 2)
        self.assertIsNotNone(result['additional_comments'])

        # Check the structure of the explanation analysis
        for explanation in result['explanation_analysis']:
            self.assertIn('explanation', explanation)
            self.assertIn('likelihood', explanation)
            self.assertIn('supporting_factors', explanation)
            self.assertIn('weaknesses', explanation)

        # Verify that process_prompt was called with the correct arguments
        mock_process_prompt.assert_called_once()
        call_args = mock_process_prompt.call_args[0]
        self.assertIn("Observation:", call_args[0])
        self.assertIn("Possible Explanations:", call_args[0])
        self.assertEqual(call_args[1], "llama3.1:latest")
        self.assertEqual(call_args[2], "AbductiveReasoner")

if __name__ == '__main__':
    unittest.main()
