# src/modules/helper_analogy.py

from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from src.modules.helper_probabilistic import bayes_theorem, calculate_probability, normal_probability
import random

def find_analogies(source_domain: str, target_domain: str, num_analogies: int = 3) -> List[Dict[str, Any]]:
    """
    Find analogies between the source domain and the target domain.

    Args:
    source_domain (str): The domain from which to draw analogies.
    target_domain (str): The domain to which analogies should be applied.
    num_analogies (int): The number of analogies to generate.

    Returns:
    List[Dict[str, Any]]: A list of analogies, each containing the source concept, target concept, and similarity score.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([source_domain, target_domain])

    source_vec = tfidf_matrix[0]
    target_vec = tfidf_matrix[1]

    similarity = cosine_similarity(source_vec, target_vec)[0][0]

    # Generate simple analogies based on common words
    source_words = source_domain.split()
    target_words = target_domain.split()

    analogies = []
    for i in range(min(num_analogies, len(source_words), len(target_words))):
        analogies.append({
            "source_concept": source_words[i],
            "target_concept": target_words[i],
            "similarity": similarity
        })

    return analogies

def map_concepts(source_concept: str, source_domain: str, target_domain: str) -> Dict[str, Any]:
    """
    Map a concept from the source domain to the target domain.

    Args:
    source_concept (str): The concept to map from the source domain.
    source_domain (str): The domain of the source concept.
    target_domain (str): The domain to map the concept to.

    Returns:
    Dict[str, Any]: A dictionary containing the mapped concept and similarity score.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([source_concept, source_domain, target_domain])

    concept_vec = tfidf_matrix[0]
    source_vec = tfidf_matrix[1]
    target_vec = tfidf_matrix[2]

    source_similarity = cosine_similarity(concept_vec, source_vec)[0][0]
    target_similarity = cosine_similarity(concept_vec, target_vec)[0][0]

    # Find the most similar word in the target domain
    target_words = target_domain.split()
    mapped_concept = max(target_words, key=lambda word: cosine_similarity(vectorizer.transform([word]), concept_vec)[0][0])

    return {
        "source_concept": source_concept,
        "mapped_concept": mapped_concept,
        "source_similarity": source_similarity,
        "target_similarity": target_similarity
    }

def apply_analogy(source_problem: str, source_solution: str, target_problem: str) -> Dict[str, Any]:
    """
    Apply analogical reasoning to solve a target problem based on a source problem-solution pair.

    Args:
    source_problem (str): The problem in the source domain.
    source_solution (str): The solution to the source problem.
    target_problem (str): The problem in the target domain to solve.

    Returns:
    Dict[str, Any]: A dictionary containing the proposed solution, confidence score, and probabilistic assessment.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([source_problem, source_solution, target_problem])

    source_problem_vec = tfidf_matrix[0]
    source_solution_vec = tfidf_matrix[1]
    target_problem_vec = tfidf_matrix[2]

    problem_similarity = cosine_similarity(source_problem_vec, target_problem_vec)[0][0]

    # Generate a simple solution by replacing words
    source_problem_words = source_problem.split()
    source_solution_words = source_solution.split()
    target_problem_words = target_problem.split()

    proposed_solution_words = []
    for word in source_solution_words:
        if word in source_problem_words:
            index = source_problem_words.index(word)
            if index < len(target_problem_words):
                proposed_solution_words.append(target_problem_words[index])
            else:
                proposed_solution_words.append(word)
        else:
            proposed_solution_words.append(word)

    proposed_solution = " ".join(proposed_solution_words)
    confidence = problem_similarity

    # Probabilistic assessment
    prior_probability = 0.5  # Assuming a neutral prior
    likelihood = normal_probability(problem_similarity, 0.5, 0.2)  # Assuming a normal distribution
    evidence = calculate_probability(len(set(source_problem_words) & set(target_problem_words)),
                                     len(set(source_problem_words) | set(target_problem_words)))

    posterior_probability = bayes_theorem(prior_probability, likelihood, evidence)

    return {
        "proposed_solution": proposed_solution,
        "confidence": confidence,
        "probabilistic_assessment": {
            "prior_probability": prior_probability,
            "likelihood": likelihood,
            "evidence": evidence,
            "posterior_probability": posterior_probability
        }
    }

def evaluate_analogy(analogy: Dict[str, Any], context: str) -> Dict[str, Any]:
    """
    Evaluate the relevance and applicability of an analogy in a given context.

    Args:
    analogy (Dict[str, Any]): The analogy to evaluate.
    context (str): The context in which to evaluate the analogy.

    Returns:
    Dict[str, Any]: A dictionary containing the evaluation metrics.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([analogy['source_concept'], analogy['target_concept'], context])

    source_vec = tfidf_matrix[0]
    target_vec = tfidf_matrix[1]
    context_vec = tfidf_matrix[2]

    source_relevance = cosine_similarity(source_vec, context_vec)[0][0]
    target_relevance = cosine_similarity(target_vec, context_vec)[0][0]

    overall_relevance = (source_relevance + target_relevance) / 2
    applicability = analogy['similarity'] * overall_relevance

    return {
        "source_relevance": source_relevance,
        "target_relevance": target_relevance,
        "overall_relevance": overall_relevance,
        "applicability": applicability
    }

def generate_analogy_chain(initial_domain: str, target_domain: str, steps: int = 3) -> List[Dict[str, Any]]:
    """
    Generate a chain of analogies from an initial domain to a target domain.

    Args:
    initial_domain (str): The starting domain.
    target_domain (str): The final target domain.
    steps (int): The number of intermediate steps in the analogy chain.

    Returns:
    List[Dict[str, Any]]: A list of analogies forming a chain from initial to target domain.
    """
    analogy_chain = []
    current_domain = initial_domain

    for i in range(steps):
        next_domain = generate_intermediate_domain(current_domain, target_domain, (i + 1) / steps)
        analogy = find_analogies(current_domain, next_domain, num_analogies=1)[0]
        analogy_chain.append(analogy)
        current_domain = next_domain

    final_analogy = find_analogies(current_domain, target_domain, num_analogies=1)[0]
    analogy_chain.append(final_analogy)

    return analogy_chain

def generate_intermediate_domain(domain1: str, domain2: str, interpolation: float) -> str:
    """
    Generate an intermediate domain between two domains.

    Args:
    domain1 (str): The first domain.
    domain2 (str): The second domain.
    interpolation (float): A value between 0 and 1 indicating how close the result should be to domain2.

    Returns:
    str: An intermediate domain.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([domain1, domain2])

    words1 = domain1.split()
    words2 = domain2.split()

    intermediate_words = []
    for i in range(min(len(words1), len(words2))):
        if random.random() < interpolation:
            intermediate_words.append(words2[i])
        else:
            intermediate_words.append(words1[i])

    return " ".join(intermediate_words)
