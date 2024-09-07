# src/modules/helper_probabilistic.py

from typing import Dict, List, Tuple
import math

def calculate_probability(favorable_outcomes: int, total_outcomes: int) -> float:
    """
    Calculate the probability of an event.

    Args:
    favorable_outcomes (int): Number of favorable outcomes.
    total_outcomes (int): Total number of possible outcomes.

    Returns:
    float: Probability of the event.
    """
    if total_outcomes == 0:
        raise ValueError("Total outcomes cannot be zero")
    return favorable_outcomes / total_outcomes

def bayes_theorem(prior: float, likelihood: float, evidence: float) -> float:
    """
    Apply Bayes' theorem to calculate the posterior probability.

    Args:
    prior (float): Prior probability of the hypothesis.
    likelihood (float): Probability of the evidence given the hypothesis.
    evidence (float): Total probability of the evidence.

    Returns:
    float: Posterior probability of the hypothesis given the evidence.
    """
    if evidence == 0:
        raise ValueError("Evidence probability cannot be zero")
    return (likelihood * prior) / evidence

def conditional_probability(joint_probability: float, condition_probability: float) -> float:
    """
    Calculate conditional probability.

    Args:
    joint_probability (float): Probability of both events occurring.
    condition_probability (float): Probability of the condition.

    Returns:
    float: Conditional probability.
    """
    if condition_probability == 0:
        raise ValueError("Condition probability cannot be zero")
    return joint_probability / condition_probability

def independent_events_probability(probabilities: List[float]) -> float:
    """
    Calculate the probability of independent events all occurring.

    Args:
    probabilities (List[float]): List of probabilities for each independent event.

    Returns:
    float: Probability of all events occurring.
    """
    return math.prod(probabilities)

def mutually_exclusive_events_probability(probabilities: List[float]) -> float:
    """
    Calculate the probability of any of the mutually exclusive events occurring.

    Args:
    probabilities (List[float]): List of probabilities for each mutually exclusive event.

    Returns:
    float: Probability of any of the events occurring.
    """
    return sum(probabilities)

def update_probabilities(prior_probabilities: Dict[str, float], evidence: str,
                         likelihoods: Dict[str, float]) -> Dict[str, float]:
    """
    Update probabilities based on new evidence using Bayes' theorem.

    Args:
    prior_probabilities (Dict[str, float]): Prior probabilities for each hypothesis.
    evidence (str): The observed evidence.
    likelihoods (Dict[str, float]): Likelihood of the evidence for each hypothesis.

    Returns:
    Dict[str, float]: Updated probabilities for each hypothesis.
    """
    total_probability = sum(prior_probabilities[h] * likelihoods[h] for h in prior_probabilities)

    return {
        hypothesis: bayes_theorem(prior_probabilities[hypothesis], likelihoods[hypothesis], total_probability)
        for hypothesis in prior_probabilities
    }

def entropy(probabilities: List[float]) -> float:
    """
    Calculate the entropy of a probability distribution.

    Args:
    probabilities (List[float]): List of probabilities.

    Returns:
    float: Entropy of the distribution.
    """
    return -sum(p * math.log2(p) for p in probabilities if p > 0)

def information_gain(prior_entropy: float, posterior_entropies: List[Tuple[float, float]]) -> float:
    """
    Calculate the information gain.

    Args:
    prior_entropy (float): Entropy of the prior distribution.
    posterior_entropies (List[Tuple[float, float]]): List of (probability, entropy) tuples for posterior distributions.

    Returns:
    float: Information gain.
    """
    weighted_posterior_entropy = sum(prob * entropy for prob, entropy in posterior_entropies)
    return prior_entropy - weighted_posterior_entropy
