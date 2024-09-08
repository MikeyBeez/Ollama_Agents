# src/modules/helper_probabilistic.py

import math
import random
from typing import List, Dict, Any, Tuple
import numpy as np
from scipy import stats

def calculate_probability(favorable_outcomes: int, total_outcomes: int) -> float:
    """Calculate the probability of an event."""
    if total_outcomes == 0:
        raise ValueError("Total outcomes cannot be zero")
    return favorable_outcomes / total_outcomes

def bayes_theorem(prior: float, likelihood: float, evidence: float) -> float:
    """Apply Bayes' theorem to calculate the posterior probability."""
    if evidence == 0:
        raise ValueError("Evidence probability cannot be zero")
    return (likelihood * prior) / evidence

def conditional_probability(joint_probability: float, condition_probability: float) -> float:
    """Calculate conditional probability."""
    if condition_probability == 0:
        raise ValueError("Condition probability cannot be zero")
    return joint_probability / condition_probability

def independent_events_probability(probabilities: List[float]) -> float:
    """Calculate the probability of independent events all occurring."""
    return math.prod(probabilities)

def mutually_exclusive_events_probability(probabilities: List[float]) -> float:
    """Calculate the probability of any of the mutually exclusive events occurring."""
    return sum(probabilities)

def update_probabilities(prior_probabilities: Dict[str, float], evidence: str,
                         likelihoods: Dict[str, float]) -> Dict[str, float]:
    """Update probabilities based on new evidence using Bayes' theorem."""
    total_probability = sum(prior_probabilities[h] * likelihoods[h] for h in prior_probabilities)
    return {
        hypothesis: bayes_theorem(prior_probabilities[hypothesis], likelihoods[hypothesis], total_probability)
        for hypothesis in prior_probabilities
    }

def entropy(probabilities: List[float]) -> float:
    """Calculate the entropy of a probability distribution."""
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def information_gain(prior_entropy: float, posterior_entropies: List[Tuple[float, float]]) -> float:
    """Calculate the information gain."""
    weighted_posterior_entropy = sum(prob * entropy for prob, entropy in posterior_entropies)
    return prior_entropy - weighted_posterior_entropy

def binomial_probability(n: int, k: int, p: float) -> float:
    """Calculate the binomial probability."""
    return stats.binom.pmf(k, n, p)

def normal_probability(x: float, mean: float, std_dev: float) -> float:
    """Calculate the probability density for a normal distribution."""
    return stats.norm.pdf(x, mean, std_dev)

def poisson_probability(k: int, lambda_param: float) -> float:
    """Calculate the Poisson probability."""
    return stats.poisson.pmf(k, lambda_param)

def confidence_interval(data: List[float], confidence: float = 0.95) -> Tuple[float, float]:
    """Calculate the confidence interval for a dataset."""
    return stats.t.interval(confidence, len(data)-1, loc=np.mean(data), scale=stats.sem(data))

def monte_carlo_simulation(func: callable, num_simulations: int, **kwargs) -> List[float]:
    """Perform a Monte Carlo simulation."""
    return [func(**kwargs) for _ in range(num_simulations)]

def probability_distribution_fit(data: List[float]) -> Tuple[str, Dict[str, float]]:
    """Fit a probability distribution to the given data."""
    distributions = [
        stats.norm, stats.expon, stats.lognorm, stats.gamma, stats.beta
    ]
    best_fit = min(distributions, key=lambda dist: stats.kstest(data, dist.name, dist.fit(data)).statistic)
    params = best_fit.fit(data)
    param_names = best_fit.shapes.split(',') + ['loc', 'scale']
    return best_fit.name, dict(zip(param_names, params))
