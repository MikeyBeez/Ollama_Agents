# src/tests/test_evaluate_reasoning_process.py

import unittest
from unittest.mock import patch
import json
from src.modules.evaluate_reasoning_process import evaluate_reasoning_process

class TestEvaluateReasoningProcess(unittest.TestCase):

    @patch('src.modules.evaluate_reasoning_process.process_prompt')
    def test_evaluate_reasoning_process(self, mock_process_prompt):
        # Mock the response from the language model
        mock_response = json.dumps({
            "overall_validity": "Questionable",
            "logical_structure": "The argument follows a deductive structure, but there are issues with some premises",
            "strengths": [
                "Clear progression of ideas",
                "Attempts to use empirical evidence"
            ],
            "weaknesses": [
                "Overgeneralization in premise 2",
                "Potential sampling bias in the evidence"
            ],
            "fallacies_identified": [
                {
                    "fallacy": "Hasty Generalization",
                    "explanation": "The conclusion is drawn from too small a sample in premise 2"
                }
            ],
            "assumptions": [
                "All birds have similar dietary needs",
                "The observed feeding behavior is representative of the species"
            ],
            "biases": [
                "Confirmation bias in selecting supporting evidence"
            ],
            "coherence_score": 7,
            "evidence_quality": "Moderate",
            "counterarguments": [
                "There might be other factors influencing the birds' behavior",
                "The sample size might not be representative of all sparrows"
            ],
            "suggestions_for_improvement": [
                "Increase the sample size and diversity of observations",
                "Consider alternative explanations for the observed behavior",
                "Address potential counterarguments in the reasoning"
            ],
            "overall_assessment": "While the reasoning process shows a clear structure, it suffers from overgeneralization and potential biases. The conclusion, while plausible, requires stronger evidence and consideration of alternative explanations."
        })
        mock_process_prompt.return_value = mock_response

        # Test input
        reasoning_steps = [
            "Premise 1: Most birds eat seeds.",
            "Premise 2: I observed 5 sparrows eating seeds in my backyard.",
            "Premise 3: Sparrows are a type of bird.",
            "Conclusion: Therefore, all sparrows primarily eat seeds."
        ]

        # Evaluate reasoning process
        result = evaluate_reasoning_process(reasoning_steps)

        # Assertions
        self.assertEqual(result['overall_validity'], "Questionable")
        self.assertIsNotNone(result['logical_structure'])
        self.assertGreater(len(result['strengths']), 0)
        self.assertGreater(len(result['weaknesses']), 0)
        self.assertGreater(len(result['fallacies_identified']), 0)
        self.assertGreater(len(result['assumptions']), 0)
        self.assertGreater(len(result['biases']), 0)
        self.assertIsInstance(result['coherence_score'], int)
        self.assertIn(result['evidence_quality'], ["Strong", "Moderate", "Weak"])
        self.assertGreater(len(result['counterarguments']), 0)
        self.assertGreater(len(result['suggestions_for_improvement']), 0)
        self.assertIsNotNone(result['overall_assessment'])

        # Check the structure of fallacies identified
        for fallacy in result['fallacies_identified']:
            self.assertIn('fallacy', fallacy)
            self.assertIn('explanation', fallacy)

        # Verify that process_prompt was called with the correct arguments
        mock_process_prompt.assert_called_once()
        call_args = mock_process_prompt.call_args[0]
        self.assertIn("Reasoning Steps:", call_args[0])
        self.assertEqual(call_args[1], "llama3.1:latest")
        self.assertEqual(call_args[2], "ReasoningEvaluator")

if __name__ == '__main__':
    unittest.main()
