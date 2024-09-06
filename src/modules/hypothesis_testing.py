# src/modules/hypothesis_testing.py

import json
from typing import List, Dict, Any
from src.modules.ollama_client import generate_response
from src.modules.logging_setup import logger

def generate_hypotheses(context: str, model_name: str) -> List[Dict[str, Any]]:
    """
    Generate hypotheses based on the given context.

    Args:
    context (str): The context to use for generating hypotheses.
    model_name (str): The name of the language model to use.

    Returns:
    List[Dict[str, Any]]: A list of generated hypotheses.
    """
    prompt = f"""
    Based on the following context, generate a list of plausible hypotheses:

    {context}

    For each hypothesis, provide a brief explanation and a initial likelihood score (0-1).

    Format your response as a JSON array of objects with the following structure:
    [
        {{
            "hypothesis": "Statement of the hypothesis",
            "explanation": "Brief explanation or rationale",
            "likelihood": 0.7
        }},
        ...
    ]
    """

    try:
        response = generate_response(prompt, model_name, "HypothesisGenerator")
        hypotheses = json.loads(response)
        logger.info(f"Generated {len(hypotheses)} hypotheses")
        return hypotheses
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON from hypothesis generation: {response}")
        return []
    except Exception as e:
        logger.error(f"Error in hypothesis generation: {str(e)}")
        return []

def design_experiment(hypothesis: str, context: str, model_name: str) -> Dict[str, Any]:
    """
    Design an experiment to test a given hypothesis.

    Args:
    hypothesis (str): The hypothesis to test.
    context (str): Additional context information.
    model_name (str): The name of the language model to use.

    Returns:
    Dict[str, Any]: A dictionary describing the designed experiment.
    """
    prompt = f"""
    Design an experiment to test the following hypothesis:

    Hypothesis: {hypothesis}
    Context: {context}

    Provide a detailed experimental design, including:
    1. Objective
    2. Methodology
    3. Required resources
    4. Expected outcomes
    5. Potential challenges

    Format your response as a JSON object with the following structure:
    {{
        "hypothesis": "The hypothesis being tested",
        "objective": "The main objective of the experiment",
        "methodology": "Step-by-step description of the experimental procedure",
        "resources": ["Resource 1", "Resource 2", ...],
        "expected_outcomes": {{
            "if_hypothesis_true": "Expected outcome if the hypothesis is true",
            "if_hypothesis_false": "Expected outcome if the hypothesis is false"
        }},
        "potential_challenges": ["Challenge 1", "Challenge 2", ...],
        "evaluation_criteria": "Criteria for evaluating the experiment's success"
    }}
    """

    try:
        response = generate_response(prompt, model_name, "ExperimentDesigner")
        experiment = json.loads(response)
        logger.info(f"Designed experiment for hypothesis: {hypothesis}")
        return experiment
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON from experiment design: {response}")
        return {}
    except Exception as e:
        logger.error(f"Error in experiment design: {str(e)}")
        return {}
