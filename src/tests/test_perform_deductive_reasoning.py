# src/tests/test_perform_deductive_reasoning.py

import unittest
from unittest.mock import patch
import json
from src.modules.perform_deductive_reasoning import perform_deductive_reasoning

class TestPerformDeductiveReasoning(unittest.TestCase):

    @patch('src.modules.perform_deductive_reasoning.process_prompt')
    def test_perform_deductive_reasoning(self, mock_process_prompt):
        # Mock the response from the language model
        mock_response = json.dumps({
            "is_valid": True,
            "explanation": "The argument follows the structure of modus ponens, which is a valid form of deductive reasoning.",
            "logical_structure": "Modus Ponens",
            "additional_comments": "This is a classic example of a valid deductive argument."
        })
        mock_process_prompt.return_value = mock_response

        # Test input
        premises = [
            "If it's raining, the streets are wet.",
            "It's raining."
        ]
        conclusion = "Therefore, the streets are wet."

        # Perform the deductive reasoning
        result = perform_deductive_reasoning(premises, conclusion)

        # Assertions
        self.assertTrue(result['is_valid'])
        self.assertEqual(result['logical_structure'], "Modus Ponens")
        self.assertIn("modus ponens", result['explanation'].lower())
        self.assertIsNotNone(result['additional_comments'])

        # Verify that process_prompt was called with the correct arguments
        mock_process_prompt.assert_called_once()
        call_args = mock_process_prompt.call_args[0]
        self.assertIn("Premises:", call_args[0])
        self.assertIn("Conclusion:", call_args[0])
        self.assertEqual(call_args[1], "llama3.1:latest")
        self.assertEqual(call_args[2], "DeductiveReasoner")

if __name__ == '__main__':
    unittest.main()
