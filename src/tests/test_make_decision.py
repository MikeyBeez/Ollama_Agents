# src/tests/test_make_decision.py

import unittest
from unittest.mock import patch
import json
from src.modules.make_decision import make_decision

class TestMakeDecision(unittest.TestCase):

    @patch('src.modules.make_decision.process_prompt')
    def test_make_decision(self, mock_process_prompt):
        # Mock the response from the language model
        mock_response = json.dumps({
            "recommended_option": "Electric Car",
            "recommendation_confidence": 0.85,
            "option_analysis": [
                {
                    "option": "Electric Car",
                    "pros": ["Environmentally friendly", "Lower operating costs"],
                    "cons": ["Higher upfront cost", "Limited range"],
                    "score": 8.5
                },
                {
                    "option": "Gasoline Car",
                    "pros": ["Lower upfront cost", "Wider range"],
                    "cons": ["Environmental impact", "Higher fuel costs"],
                    "score": 7.0
                }
            ],
            "criteria_breakdown": [
                {
                    "criterion": "Environmental Impact",
                    "importance": 0.4,
                    "option_scores": {
                        "Electric Car": 9.0,
                        "Gasoline Car": 5.0
                    }
                },
                {
                    "criterion": "Cost",
                    "importance": 0.3,
                    "option_scores": {
                        "Electric Car": 7.0,
                        "Gasoline Car": 8.0
                    }
                },
                {
                    "criterion": "Performance",
                    "importance": 0.3,
                    "option_scores": {
                        "Electric Car": 8.0,
                        "Gasoline Car": 8.5
                    }
                }
            ],
            "decision_process": "The decision was made by weighing the pros and cons of each option against the given criteria, taking into account the importance of each criterion.",
            "sensitivity_analysis": "If the importance of environmental impact decreases, the gasoline car becomes more competitive. However, the electric car remains the recommended option unless the importance of environmental impact drops significantly.",
            "alternative_recommendations": ["Hybrid Car", "Public Transportation"],
            "additional_considerations": ["Future advancements in battery technology", "Availability of charging infrastructure"],
            "overall_summary": "Based on the given criteria and preferences, the electric car is recommended due to its strong environmental performance and good overall balance across all criteria. However, individual circumstances and potential future developments should be considered before making a final decision."
        })
        mock_process_prompt.return_value = mock_response

        # Test input
        options = ["Electric Car", "Gasoline Car"]
        criteria = ["Environmental Impact", "Cost", "Performance"]
        preferences = {
            "Environmental Impact": 0.4,
            "Cost": 0.3,
            "Performance": 0.3
        }

        # Make decision
        result = make_decision(options, criteria, preferences)

        # Assertions
        self.assertIn(result['recommended_option'], options)
        self.assertGreaterEqual(result['recommendation_confidence'], 0.0)
        self.assertLessEqual(result['recommendation_confidence'], 1.0)
        self.assertEqual(len(result['option_analysis']), len(options))
        self.assertEqual(len(result['criteria_breakdown']), len(criteria))
        self.assertIsNotNone(result['decision_process'])
        self.assertIsNotNone(result['sensitivity_analysis'])
        self.assertGreater(len(result['alternative_recommendations']), 0)
        self.assertGreater(len(result['additional_considerations']), 0)
        self.assertIsNotNone(result['overall_summary'])

        # Check the structure of option_analysis
        for option in result['option_analysis']:
            self.assertIn('option', option)
            self.assertIn('pros', option)
            self.assertIn('cons', option)
            self.assertGreaterEqual(option['score'], 0.0)
            self.assertLessEqual(option['score'], 10.0)

        # Check the structure of criteria_breakdown
        for criterion in result['criteria_breakdown']:
            self.assertIn('criterion', criterion)
            self.assertGreaterEqual(criterion['importance'], 0.0)
            self.assertLessEqual(criterion['importance'], 1.0)
            self.assertEqual(len(criterion['option_scores']), len(options))

        # Verify that process_prompt was called with the correct arguments
        mock_process_prompt.assert_called_once()
        call_args = mock_process_prompt.call_args[0]
        self.assertIn("Options:", call_args[0])
        self.assertIn("Criteria:", call_args[0])
        self.assertIn("Preferences", call_args[0])
        self.assertEqual(call_args[1], "llama3.1:latest")
        self.assertEqual(call_args[2], "DecisionMaker")

if __name__ == '__main__':
    unittest.main()
