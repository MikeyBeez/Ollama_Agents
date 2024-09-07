# src/tests/test_helper_hypothesis.py

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.helper_hypothesis import (
    generate_hypotheses,
    test_hypothesis,
    rank_hypotheses,
    generate_experiment
)

class TestHelperHypothesis(unittest.TestCase):
    def setUp(self):
        self.sample_context = "Climate change affects global temperatures, leading to various environmental impacts."

    def test_generate_hypotheses(self):
        hypotheses = generate_hypotheses(self.sample_context, num_hypotheses=3)
        self.assertEqual(len(hypotheses), 3)
        for hypothesis in hypotheses:
            self.assertIn('hypothesis', hypothesis)
            self.assertIn('likelihood', hypothesis)
            self.assertTrue(0 <= hypothesis['likelihood'] <= 1)

    def test_test_hypothesis(self):
        hypothesis = {
            "hypothesis": "The increase in climate change leads to increase in global temperatures",
            "likelihood": 0.7
        }
        evidence = "Recent studies show a strong correlation between climate change and rising global temperatures."
        result = test_hypothesis(hypothesis, self.sample_context, evidence)

        self.assertIn('original_likelihood', result)
        self.assertIn('updated_likelihood', result)
        self.assertIn('relevance_to_context', result)
        self.assertIn('relevance_to_evidence', result)
        self.assertIn('result', result)
        self.assertTrue(0 <= result['updated_likelihood'] <= 1)
        self.assertTrue(0 <= result['relevance_to_context'] <= 1)
        self.assertTrue(0 <= result['relevance_to_evidence'] <= 1)
        self.assertIn(result['result'], ['supported', 'refuted', 'inconclusive'])

    def test_rank_hypotheses(self):
        hypotheses = [
            {"hypothesis": "H1", "updated_likelihood": 0.8},
            {"hypothesis": "H2", "updated_likelihood": 0.6},
            {"hypothesis": "H3", "updated_likelihood": 0.9}
        ]
        ranked = rank_hypotheses(hypotheses)
        self.assertEqual(len(ranked), 3)
        self.assertEqual(ranked[0]['hypothesis'], "H3")
        self.assertEqual(ranked[-1]['hypothesis'], "H2")

    def test_generate_experiment(self):
        hypothesis = {
            "hypothesis": "The increase in climate change leads to increase in global temperatures"
        }
        experiment = generate_experiment(hypothesis)
        self.assertIn('hypothesis', experiment)
        self.assertIn('method', experiment)
        self.assertIn('variables', experiment)
        self.assertIn('expected_outcome', experiment)
        self.assertIn('independent', experiment['variables'])
        self.assertIn('dependent', experiment['variables'])

if __name__ == '__main__':
    unittest.main()
