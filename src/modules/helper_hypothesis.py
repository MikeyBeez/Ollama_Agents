# src/modules/helper_hypothesis.py

from typing import List, Dict, Any
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def generate_hypotheses(context: str, num_hypotheses: int = 3) -> List[Dict[str, Any]]:
    """
    Generate hypotheses based on the given context.

    Args:
    context (str): The context to generate hypotheses from.
    num_hypotheses (int): The number of hypotheses to generate.

    Returns:
    List[Dict[str, Any]]: A list of hypotheses, each containing the hypothesis text and its initial likelihood.
    """
    # In a real implementation, this would use more sophisticated NLP techniques
    # For now, we'll use a simple keyword-based approach
    keywords = ['increase', 'decrease', 'cause', 'effect', 'correlation', 'impact']
    hypotheses = []

    for _ in range(num_hypotheses):
        hypothesis = f"The {random.choice(keywords)} in {context.split()[random.randint(0, len(context.split())-1)]} " \
                     f"leads to {random.choice(keywords)} in {context.split()[random.randint(0, len(context.split())-1)]}"
        likelihood = random.uniform(0.1, 0.9)
        hypotheses.append({"hypothesis": hypothesis, "likelihood": likelihood})

    return hypotheses

def test_hypothesis(hypothesis: Dict[str, Any], context: str, evidence: str) -> Dict[str, Any]:
    """
    Test a given hypothesis against provided evidence.

    Args:
    hypothesis (Dict[str, Any]): The hypothesis to test.
    context (str): The original context.
    evidence (str): New evidence to test the hypothesis against.

    Returns:
    Dict[str, Any]: The updated hypothesis with test results.
    """
    # Use TF-IDF and cosine similarity to measure the relevance of the evidence to the hypothesis
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([hypothesis['hypothesis'], context, evidence])

    hypothesis_vec = tfidf_matrix[0]
    context_vec = tfidf_matrix[1]
    evidence_vec = tfidf_matrix[2]

    relevance_to_context = cosine_similarity(hypothesis_vec, context_vec)[0][0]
    relevance_to_evidence = cosine_similarity(hypothesis_vec, evidence_vec)[0][0]

    # Update the likelihood based on the relevance
    updated_likelihood = (hypothesis['likelihood'] + relevance_to_evidence) / 2

    # Determine if the hypothesis is supported, refuted, or inconclusive
    if relevance_to_evidence > 0.7:
        result = "supported"
    elif relevance_to_evidence < 0.3:
        result = "refuted"
    else:
        result = "inconclusive"

    return {
        "hypothesis": hypothesis['hypothesis'],
        "original_likelihood": hypothesis['likelihood'],
        "updated_likelihood": updated_likelihood,
        "relevance_to_context": relevance_to_context,
        "relevance_to_evidence": relevance_to_evidence,
        "result": result
    }

def rank_hypotheses(hypotheses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Rank hypotheses based on their updated likelihood.

    Args:
    hypotheses (List[Dict[str, Any]]): A list of tested hypotheses.

    Returns:
    List[Dict[str, Any]]: The list of hypotheses sorted by their updated likelihood in descending order.
    """
    return sorted(hypotheses, key=lambda h: h['updated_likelihood'], reverse=True)

def generate_experiment(hypothesis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate an experiment design to further test a hypothesis.

    Args:
    hypothesis (Dict[str, Any]): The hypothesis to design an experiment for.

    Returns:
    Dict[str, Any]: An experiment design.
    """
    # In a real implementation, this would be more sophisticated
    experiment = {
        "hypothesis": hypothesis['hypothesis'],
        "method": f"Conduct a controlled study to measure the impact of {hypothesis['hypothesis'].split('in')[1]} on {hypothesis['hypothesis'].split('to')[1]}",
        "variables": {
            "independent": hypothesis['hypothesis'].split('in')[1].strip(),
            "dependent": hypothesis['hypothesis'].split('to')[1].strip()
        },
        "expected_outcome": f"If the hypothesis is correct, we expect to see a significant {hypothesis['hypothesis'].split()[1]} in the dependent variable."
    }
    return experiment
