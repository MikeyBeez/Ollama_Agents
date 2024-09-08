# src/modules/perform_abductive_reasoning.py

import json
from typing import List, Dict, Any
from src.modules.ollama_client import process_prompt

def perform_abductive_reasoning(observation: str, possible_explanations: List[str]) -> Dict[str, Any]:
    """
    Perform abductive reasoning based on an observation and possible explanations.

    Args:
    observation (str): The observed phenomenon or fact.
    possible_explanations (List[str]): A list of possible explanations or hypotheses.

    Returns:
    Dict[str, Any]: A dictionary containing the best explanation, its likelihood,
                    and an analysis of all provided explanations.
    """
    prompt = f"""
    Perform abductive reasoning on the following:

    Observation:
    {observation}

    Possible Explanations:
    {json.dumps(possible_explanations)}

    Analyze each explanation, determine the best (most likely) explanation,
    and provide a likelihood assessment for each. Return your analysis
    in the following JSON format:

    {{
        "best_explanation": "The most likely explanation",
        "best_explanation_likelihood": "High/Medium/Low",
        "explanation_analysis": [
            {{
                "explanation": "Explanation 1",
                "likelihood": "High/Medium/Low",
                "supporting_factors": ["Factor 1", "Factor 2", ...],
                "weaknesses": ["Weakness 1", "Weakness 2", ...]
            }},
            ...
        ],
        "additional_comments": "Any additional insights or comments"
    }}
    """

    response = process_prompt(prompt, "llama3.1:latest", "AbductiveReasoner")
    return json.loads(response)
