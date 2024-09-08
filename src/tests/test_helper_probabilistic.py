# src/tests/test_helper_probabilistic.py

import unittest
import math
import random
import numpy as np
from src.modules.helper_probabilistic import *

class TestHelperProbabilistic(unittest.TestCase):

    def test_calculate_probability(self):
        self.assertAlmostEqual(calculate_probability(1, 6), 1/6)
        self.assertAlmostEqual(calculate_probability(3, 10), 0.3)
        with self.assertRaises(ValueError):
            calculate_probability(1, 0)

    def test_bayes_theorem(self):
        self.assertAlmostEqual(bayes_theorem(0.1, 0.8, 0.15), 0.53333, places=5)
        with self.assertRaises(ValueError):
            bayes_theorem(0.1, 0.8, 0)

    def test_conditional_probability(self):
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

    def test_information_gain(self):
        prior_entropy = 1.0
        posterior_entropies = [(0.7, 0.8), (0.3, 0.6)]
        self.assertAlmostEqual(information_gain(prior_entropy, posterior_entropies), 0.26)

    def test_binomial_probability(self):
        self.assertAlmostEqual(binomial_probability(10, 3, 0.5), 0.1171875)

    def test_normal_probability(self):
        self.assertAlmostEqual(normal_probability(0, 0, 1), 0.3989423)

    def test_poisson_probability(self):
        self.assertAlmostEqual(poisson_probability(5, 3), 0.1008188)

    def test_confidence_interval(self):
        data = [1, 2, 3, 4, 5]
        lower, upper = confidence_interval(data)
        self.assertLess(lower, 3)
        self.assertGreater(upper, 3)

    def test_monte_carlo_simulation(self):
        def coin_flip():
            return random.choice([0, 1])
        results = monte_carlo_simulation(coin_flip, 1000)
        self.assertAlmostEqual(sum(results) / len(results), 0.5, places=1)

    def test_probability_distribution_fit(self):
        np.random.seed(42)  # Set seed for reproducibility
        data = np.random.normal(0, 1, 1000)
        dist_name, params = probability_distribution_fit(data)
        self.assertIn(dist_name, ['norm', 'gamma', 'beta', 'expon', 'lognorm'])
        self.assertIn('loc', params)
        self.assertIn('scale', params)

if __name__ == '__main__':
    unittest.main()
