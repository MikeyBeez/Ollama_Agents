# src/tests/test_helper_probabilistic.py

import unittest
import sys
import os
import math

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.helper_probabilistic import (
    calculate_probability,
    bayes_theorem,
    conditional_probability,
    independent_events_probability,
    mutually_exclusive_events_probability,
    update_probabilities,
    entropy,
    information_gain
)

class TestHelperProbabilistic(unittest.TestCase):
    def test_calculate_probability(self):
        self.assertAlmostEqual(calculate_probability(1, 6), 1/6)
        self.assertAlmostEqual(calculate_probability(3, 10), 0.3)
        with self.assertRaises(ValueError):
            calculate_probability(1, 0)

    def test_bayes_theorem(self):
        # P(A|B) = P(B|A) * P(A) / P(B)
        self.assertAlmostEqual(bayes_theorem(0.1, 0.8, 0.15), 0.53333, places=5)
        with self.assertRaises(ValueError):
            bayes_theorem(0.1, 0.8, 0)

    def test_conditional_probability(self):
        # P(A|B) = P(A and B) / P(B)
        self.assertAlmostEqual(conditional_probability(0.03, 0.1), 0.3)
        with self.assertRaises(ValueError):
            conditional_probability(0.1, 0)

    def test_independent_events_probability(self):
        self.assertAlmostEqual(independent_events_probability([0.5, 0.6, 0.7]), 0.21)

    def test_mutually_exclusive_events_probability(self):
        self.assertAlmostEqual(mutually_exclusive_events_probability([0.1, 0.2, 0.3]), 0.6)

    def test_update_probabilities(self):
        prior_probabilities = {'H1': 0.3, 'H2': 0.7}
        likelihoods = {'H1': 0.8, 'H2': 0.4}
        evidence = 'E'
        updated = update_probabilities(prior_probabilities, evidence, likelihoods)
        self.assertAlmostEqual(updated['H1'], 0.4615, places=4)
        self.assertAlmostEqual(updated['H2'], 0.5385, places=4)

    def test_entropy(self):
        self.assertAlmostEqual(entropy([0.5, 0.5]), 1.0)
        self.assertAlmostEqual(entropy([1/3, 1/3, 1/3]), math.log2(3))
        self.assertAlmostEqual(entropy([0.1, 0.9]), 0.4689955935892812, places=7)

    def test_information_gain(self):
        prior_entropy = 1.0
        posterior_entropies = [(0.7, 0.8), (0.3, 0.6)]
        self.assertAlmostEqual(information_gain(prior_entropy, posterior_entropies), 0.26)

if __name__ == '__main__':
    unittest.main()
