# src/tests/test_helper_statistics.py

import unittest
import math
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.helper_statistics import (
    mean, median, mode, variance, standard_deviation,
    covariance, correlation, z_score, percentile,
    summary_statistics, t_test, chi_square_test
)

class TestHelperStatistics(unittest.TestCase):
    def test_mean(self):
        self.assertAlmostEqual(mean([1, 2, 3, 4, 5]), 3)
        self.assertAlmostEqual(mean([1.5, 2.5, 3.5]), 2.5)
        with self.assertRaises(ValueError):
            mean([])

    def test_median(self):
        self.assertEqual(median([1, 2, 3, 4, 5]), 3)
        self.assertEqual(median([1, 2, 3, 4]), 2.5)
        self.assertEqual(median([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]), 4)

    def test_mode(self):
        self.assertEqual(mode([1, 2, 3, 3, 4, 5]), [3])
        self.assertEqual(set(mode([1, 2, 2, 3, 3, 4])), {2, 3})
        self.assertEqual(mode(['a', 'b', 'c', 'a', 'b', 'a']), ['a'])

    def test_variance(self):
        self.assertAlmostEqual(variance([1, 2, 3, 4, 5]), 2.5)
        with self.assertRaises(ValueError):
            variance([1])

    def test_standard_deviation(self):
        self.assertAlmostEqual(standard_deviation([1, 2, 3, 4, 5]), math.sqrt(2.5))

    def test_covariance(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 5, 4, 5]
        self.assertAlmostEqual(covariance(x, y), 1.5)
        with self.assertRaises(ValueError):
            covariance(x, y[:-1])

    def test_correlation(self):
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 5, 4, 5]
        self.assertAlmostEqual(correlation(x, y), 0.7745966692414834)

    def test_z_score(self):
        data = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(z_score(4, data), 0.6324555320336759)

    def test_percentile(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(percentile(data, 50), 5.5)
        self.assertEqual(percentile(data, 25), 3.25)
        self.assertEqual(percentile(data, 75), 7.75)

    def test_summary_statistics(self):
        data = [1, 2, 3, 4, 5]
        stats = summary_statistics(data)
        self.assertAlmostEqual(stats['mean'], 3)
        self.assertAlmostEqual(stats['median'], 3)
        self.assertEqual(stats['mode'], [1, 2, 3, 4, 5])
        self.assertAlmostEqual(stats['variance'], 2.5)
        self.assertAlmostEqual(stats['std_dev'], math.sqrt(2.5))

    def test_t_test(self):
        sample1 = [1, 2, 3, 4, 5]
        sample2 = [2, 4, 6, 8, 10]
        t_stat, p_value = t_test(sample1, sample2)
        self.assertAlmostEqual(t_stat, -1.8973665961010275, places=7)
        self.assertAlmostEqual(p_value, 0.09434977284243756, places=7)

    def test_chi_square_test(self):
        # Example: Test of fairness of a die
        # Observed frequencies of outcomes in 600 rolls
        observed = [100, 90, 110, 95, 105, 100]
        # Expected frequencies (fair die)
        expected = [100, 100, 100, 100, 100, 100]

        chi_square, p_value = chi_square_test(observed, expected)

        # Known chi-square value for this example (calculated manually)
        expected_chi_square = 2.5

        self.assertAlmostEqual(chi_square, expected_chi_square, places=7)
        self.assertGreater(p_value, 0.05)  # Not significant at 0.05 level

if __name__ == '__main__':
    unittest.main()
