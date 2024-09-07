# src/modules/helper_statistics.py

from typing import List, Tuple, Dict, Any
import math
import scipy.stats as stats

def mean(data: List[float]) -> float:
    if not data:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(data) / len(data)

def median(data: List[float]) -> float:
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 0:
        return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
    else:
        return sorted_data[n//2]

def mode(data: List[Any]) -> List[Any]:
    from collections import Counter
    count = Counter(data)
    max_count = max(count.values())
    return [k for k, v in count.items() if v == max_count]

def variance(data: List[float]) -> float:
    if len(data) < 2:
        raise ValueError("Variance requires at least two data points")
    m = mean(data)
    return sum((x - m) ** 2 for x in data) / (len(data) - 1)

def standard_deviation(data: List[float]) -> float:
    return math.sqrt(variance(data))

def covariance(x: List[float], y: List[float]) -> float:
    if len(x) != len(y):
        raise ValueError("Lists must have the same length")
    if len(x) < 2:
        raise ValueError("Covariance requires at least two data points")
    x_mean, y_mean = mean(x), mean(y)
    return sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, y)) / (len(x) - 1)

def correlation(x: List[float], y: List[float]) -> float:
    if len(x) != len(y):
        raise ValueError("Lists must have the same length")
    if len(x) < 2:
        raise ValueError("Correlation requires at least two data points")
    x_std, y_std = standard_deviation(x), standard_deviation(y)
    if x_std == 0 or y_std == 0:
        raise ValueError("Standard deviation cannot be zero")
    return covariance(x, y) / (x_std * y_std)

def z_score(value: float, data: List[float]) -> float:
    m = mean(data)
    s = standard_deviation(data)
    return (value - m) / s

def percentile(data: List[float], p: float) -> float:
    if p < 0 or p > 100:
        raise ValueError("Percentile must be between 0 and 100")
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * (p / 100)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    d0 = sorted_data[int(f)] * (c - k)
    d1 = sorted_data[int(c)] * (k - f)
    return d0 + d1

def summary_statistics(data: List[float]) -> Dict[str, float]:
    return {
        "mean": mean(data),
        "median": median(data),
        "mode": mode(data),
        "variance": variance(data),
        "std_dev": standard_deviation(data),
        "min": min(data),
        "max": max(data),
        "q1": percentile(data, 25),
        "q3": percentile(data, 75)
    }

def t_test(sample1: List[float], sample2: List[float]) -> Tuple[float, float]:
    t_stat, p_value = stats.ttest_ind(sample1, sample2)
    return t_stat, p_value

def chi_square_test(observed: List[int], expected: List[float]) -> Tuple[float, float]:
    """
    Perform a chi-square goodness-of-fit test.

    Args:
    observed (List[int]): Observed frequencies.
    expected (List[float]): Expected frequencies.

    Returns:
    Tuple[float, float]: Chi-square statistic and p-value.
    """
    if len(observed) != len(expected):
        raise ValueError("Observed and expected lists must be the same length.")

    return stats.chisquare(observed, expected)
