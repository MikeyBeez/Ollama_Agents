# src/modules/perform_inductive_reasoning.py

import json
from typing import List, Dict, Any
from src.modules.ollama_client import process_prompt

def perform_inductive_reasoning(observations: List[str], hypothesis: str) -> Dict[str, Any]:
    """
    Perform inductive reasoning based on given observations and a proposed hypothesis.

    Args:
    observations (List[str]): A list of observed facts or instances.
    hypothesis (str): The proposed general conclusion or hypothesis.

    Returns:
    Dict[str, Any]: A dictionary containing the strength of the inductive argument,
                    explanation, and potential counterexamples or limitations.
    """
    prompt = f"""
    Perform inductive reasoning on the following:

    Observations:
    {json.dumps(observations)}

    Proposed Hypothesis:
    {hypothesis}

    Analyze the inductive strength of the argument, provide an explanation,
    and identify potential counterexamples or limitations. Return your analysis
    in the following JSON format:

    {{
        "inductive_strength": "Strong/Moderate/Weak",
        "explanation": "Detailed explanation of the reasoning",
        "supporting_factors": ["Factor 1", "Factor 2", ...],
        "limitations": ["Limitation 1", "Limitation 2", ...],
        "potential_counterexamples": ["Counterexample 1", "Counterexample 2", ...],
        "additional_comments": "Any additional insights or comments"
    }}
    """

    response = process_prompt(prompt, "llama3.1:latest", "InductiveReasoner")
    return json.loads(response)
