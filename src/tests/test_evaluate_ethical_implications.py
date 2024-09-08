# src/tests/test_evaluate_ethical_implications.py

import unittest
from unittest.mock import patch
import json
from src.modules.evaluate_ethical_implications import evaluate_ethical_implications

class TestEvaluateEthicalImplications(unittest.TestCase):

    @patch('src.modules.evaluate_ethical_implications.process_prompt')
    def test_evaluate_ethical_implications(self, mock_process_prompt):
        # Mock the response from the language model
        mock_response = json.dumps({
            "ethical_assessment": "Ethically Questionable",
            "key_ethical_considerations": [
                "Privacy concerns",
                "Potential for misuse of personal data",
                "Informed consent"
            ],
            "potential_consequences": [
                {
                    "consequence": "Improved targeted advertising",
                    "likelihood": "High",
                    "impact": "Positive",
                    "severity": "Medium"
                },
                {
                    "consequence": "Privacy breaches",
                    "likelihood": "Medium",
                    "impact": "Negative",
                    "severity": "High"
                }
            ],
            "stakeholder_impact": [
                {
                    "stakeholder": "Users",
                    "impact": "Potential loss of privacy and autonomy"
                },
                {
                    "stakeholder": "Company",
                    "impact": "Increased revenue but potential reputational risk"
                }
            ],
            "ethical_principles": [
                {
                    "principle": "Respect for persons",
                    "alignment": "Conflicts",
                    "explanation": "The action may violate user autonomy and privacy"
                },
                {
                    "principle": "Beneficence",
                    "alignment": "Aligns",
                    "explanation": "Could lead to improved user experience and business growth"
                }
            ],
            "alternative_actions": [
                "Implement strict opt-in policies for data collection",
                "Use anonymized data only",
                "Provide clear and transparent information about data usage"
            ],
            "overall_analysis": "While the action has potential benefits, it raises significant ethical concerns regarding privacy and consent. The company should consider less invasive alternatives that respect user autonomy."
        })
        mock_process_prompt.return_value = mock_response

        # Test input
        action = "Collect and analyze user browsing data to improve targeted advertising"
        context = "A social media company wants to enhance its advertising algorithm"

        # Evaluate ethical implications
        result = evaluate_ethical_implications(action, context)

        # Assertions
        self.assertEqual(result['ethical_assessment'], "Ethically Questionable")
        self.assertGreater(len(result['key_ethical_considerations']), 0)
        self.assertGreater(len(result['potential_consequences']), 0)
        self.assertGreater(len(result['stakeholder_impact']), 0)
        self.assertGreater(len(result['ethical_principles']), 0)
        self.assertGreater(len(result['alternative_actions']), 0)
        self.assertIsNotNone(result['overall_analysis'])

        # Check the structure of potential consequences
        for consequence in result['potential_consequences']:
            self.assertIn('consequence', consequence)
            self.assertIn('likelihood', consequence)
            self.assertIn('impact', consequence)
            self.assertIn('severity', consequence)

        # Check the structure of stakeholder impact
        for stakeholder in result['stakeholder_impact']:
            self.assertIn('stakeholder', stakeholder)
            self.assertIn('impact', stakeholder)

        # Check the structure of ethical principles
        for principle in result['ethical_principles']:
            self.assertIn('principle', principle)
            self.assertIn('alignment', principle)
            self.assertIn('explanation', principle)

        # Verify that process_prompt was called with the correct arguments
        mock_process_prompt.assert_called_once()
        call_args = mock_process_prompt.call_args[0]
        self.assertIn("Action:", call_args[0])
        self.assertIn("Context:", call_args[0])
        self.assertEqual(call_args[1], "llama3.1:latest")
        self.assertEqual(call_args[2], "EthicalEvaluator")

if __name__ == '__main__':
    unittest.main()
