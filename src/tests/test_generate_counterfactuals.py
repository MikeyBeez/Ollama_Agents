# src/tests/test_generate_counterfactuals.py

import unittest
from unittest.mock import patch
import json
from src.modules.generate_counterfactuals import generate_counterfactuals

class TestGenerateCounterfactuals(unittest.TestCase):

    @patch('src.modules.generate_counterfactuals.process_prompt')
    def test_generate_counterfactuals(self, mock_process_prompt):
        # Mock the response from the language model
        mock_response = json.dumps({
            "counterfactuals": [
                {
                    "scenario": "If the driver had left 10 minutes earlier, they would have avoided the traffic jam.",
                    "plausibility": "High",
                    "key_changes": ["Earlier departure time"],
                    "potential_implications": ["Arrives at work on time", "Less stress during commute"]
                },
                {
                    "scenario": "If the city had implemented better traffic management systems, the congestion would have been reduced.",
                    "plausibility": "Medium",
                    "key_changes": ["Improved traffic management", "Infrastructure investment"],
                    "potential_implications": ["Reduced overall commute times", "Improved city logistics"]
                },
                {
                    "scenario": "If teleportation technology existed, the driver could have instantly transported to work.",
                    "plausibility": "Low",
                    "key_changes": ["Existence of teleportation technology"],
                    "potential_implications": ["Elimination of traditional commuting", "Radical changes in urban planning"]
                }
            ],
            "analysis": "The counterfactuals range from highly plausible personal choices to less likely technological advancements, showcasing various levels of individual and systemic changes that could affect the outcome.",
            "additional_comments": "These counterfactuals highlight the interplay between personal decisions, city planning, and technological advancements in addressing commute issues."
        })
        mock_process_prompt.return_value = mock_response

        # Test input
        scenario = "A person is stuck in heavy traffic and arrives late to work."
        target_outcome = "The person arrives at work on time."

        # Generate counterfactuals
        result = generate_counterfactuals(scenario, target_outcome)

        # Assertions
        self.assertEqual(len(result['counterfactuals']), 3)
        self.assertIsNotNone(result['analysis'])
        self.assertIsNotNone(result['additional_comments'])

        # Check the structure of each counterfactual
        for counterfactual in result['counterfactuals']:
            self.assertIn('scenario', counterfactual)
            self.assertIn('plausibility', counterfactual)
            self.assertIn('key_changes', counterfactual)
            self.assertIn('potential_implications', counterfactual)

        # Verify that process_prompt was called with the correct arguments
        mock_process_prompt.assert_called_once()
        call_args = mock_process_prompt.call_args[0]
        self.assertIn("Original Scenario:", call_args[0])
        self.assertIn("Target Outcome:", call_args[0])
        self.assertEqual(call_args[1], "llama3.1:latest")
        self.assertEqual(call_args[2], "CounterfactualGenerator")

if __name__ == '__main__':
    unittest.main()
