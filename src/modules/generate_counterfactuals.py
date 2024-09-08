# src/modules/generate_counterfactuals.py

import json
from typing import Dict, Any
from src.modules.ollama_client import process_prompt

def generate_counterfactuals(scenario: str, target_outcome: str, num_counterfactuals: int = 3) -> Dict[str, Any]:
    """
    Generate counterfactual scenarios based on a given scenario and target outcome.

    Args:
    scenario (str): The original scenario or situation.
    target_outcome (str): The desired or alternative outcome.
    num_counterfactuals (int): The number of counterfactuals to generate (default is 3).

    Returns:
    Dict[str, Any]: A dictionary containing the generated counterfactuals, their plausibility,
                    and potential implications.
    """
    prompt = f"""
    Generate counterfactual scenarios based on the following:

    Original Scenario:
    {scenario}

    Target Outcome:
    {target_outcome}

    Generate {num_counterfactuals} counterfactual scenarios that could lead to the target outcome.
    For each counterfactual, assess its plausibility and potential implications.
    Return your analysis in the following JSON format:

    {{
        "counterfactuals": [
            {{
                "scenario": "Description of the counterfactual scenario",
                "plausibility": "High/Medium/Low",
                "key_changes": ["Change 1", "Change 2", ...],
                "potential_implications": ["Implication 1", "Implication 2", ...]
            }},
            ...
        ],
        "analysis": "Overall analysis of the counterfactuals and their significance",
        "additional_comments": "Any additional insights or comments"
    }}
    """

    response = process_prompt(prompt, "llama3.1:latest", "CounterfactualGenerator")
    return json.loads(response)
