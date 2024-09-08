# src/modules/perform_deductive_reasoning.py

import json
from typing import List, Dict, Any
from src.modules.ollama_client import process_prompt

def perform_deductive_reasoning(premises: List[str], conclusion: str) -> Dict[str, Any]:
    """
    Perform deductive reasoning based on given premises and a conclusion.

    Args:
    premises (List[str]): A list of premise statements.
    conclusion (str): The proposed conclusion.

    Returns:
    Dict[str, Any]: A dictionary containing the validity of the argument,
                    explanation, and identified logical structure.
    """
    prompt = f"""
    Perform deductive reasoning on the following argument:

    Premises:
    {json.dumps(premises)}

    Conclusion:
    {conclusion}

    Analyze the logical structure, determine if the argument is valid,
    and provide an explanation. Return your analysis in the following JSON format:

    {{
        "is_valid": true or false,
        "explanation": "Detailed explanation of the reasoning",
        "logical_structure": "Identified logical structure (e.g., modus ponens, syllogism)",
        "additional_comments": "Any additional insights or comments"
    }}
    """

    response = process_prompt(prompt, "llama3.1:latest", "DeductiveReasoner")
    return json.loads(response)
