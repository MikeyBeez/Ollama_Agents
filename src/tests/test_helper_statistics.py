# src/tests/test_helper_statistics.py

import unittest
import math
from src.modules.helper_statistics import *

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
        self.assertAlmostEqual(correlation(x, y), 0.7745966692414834, places=7)

    def test_z_score(self):
        data = [1, 2, 3, 4, 5]
        self.assertAlmostEqual(z_score(4, data), 0.6324555320336759, places=7)

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
        observed = [16, 18, 16, 14, 12, 12]
        expected = [16, 16, 16, 16, 16, 8]
        chi2, p_value = chi_square_test(observed, expected)
        self.assertAlmostEqual(chi2, 3.5)
        self.assertAlmostEqual(p_value, 0.6233876277495822, places=7)

    def test_calculate_basic_probability(self):
        self.assertAlmostEqual(calculate_basic_probability(3, 10), 0.3)
        with self.assertRaises(ValueError):
            calculate_basic_probability(1, 0)

    def test_calculate_conditional_probability(self):
        self.assertAlmostEqual(calculate_conditional_probability(0.2, 0.5), 0.4)
        with self.assertRaises(ValueError):
            calculate_conditional_probability(0.1, 0)

    def test_calculate_bayes_theorem(self):
        self.assertAlmostEqual(calculate_bayes_theorem(0.1, 0.8, 0.15), 0.5333333333333333)
        with self.assertRaises(ValueError):
            calculate_bayes_theorem(0.1, 0.8, 0)

    def test_binomial_probability(self):
        self.assertAlmostEqual(binomial_probability(10, 3, 0.5), 0.11718750000000006)

    def test_normal_probability(self):
        self.assertAlmostEqual(normal_probability(0, 0, 1), 0.3989422804014327)

    def test_poisson_probability(self):
        self.assertAlmostEqual(poisson_probability(5, 3), 0.10081881344492458)

    def test_confidence_interval(self):
        data = [1, 2, 3, 4, 5]
        lower, upper = confidence_interval(data)
        self.assertAlmostEqual(lower, 1.036756838522439, places=7)
        self.assertAlmostEqual(upper, 4.963243161477561, places=7)

if __name__ == '__main__':
    unittest.main()
