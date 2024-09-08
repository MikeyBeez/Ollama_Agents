# src/modules/evaluate_reasoning_process.py

import json
from typing import List, Dict, Any
from src.modules.ollama_client import process_prompt

def evaluate_reasoning_process(reasoning_steps: List[str]) -> Dict[str, Any]:
    """
    Evaluate the quality and validity of a given reasoning process.

    Args:
    reasoning_steps (List[str]): A list of steps in the reasoning process.

    Returns:
    Dict[str, Any]: A dictionary containing the evaluation of the reasoning process,
                    including validity, strengths, weaknesses, and suggestions for improvement.
    """
    prompt = f"""
    Evaluate the following reasoning process:

    Reasoning Steps:
    {json.dumps(reasoning_steps, indent=2)}

    Analyze the logical structure, validity, and strength of the reasoning process.
    Identify any fallacies, assumptions, or biases. Provide an overall assessment
    and suggestions for improvement. Return your analysis in the following JSON format:

    {{
        "overall_validity": "Valid/Questionable/Invalid",
        "logical_structure": "Description of the logical structure",
        "strengths": ["Strength 1", "Strength 2", ...],
        "weaknesses": ["Weakness 1", "Weakness 2", ...],
        "fallacies_identified": [
            {{
                "fallacy": "Name of the fallacy",
                "explanation": "Explanation of how it applies to the reasoning"
            }},
            ...
        ],
        "assumptions": ["Assumption 1", "Assumption 2", ...],
        "biases": ["Bias 1", "Bias 2", ...],
        "coherence_score": "Score from 1-10",
        "evidence_quality": "Strong/Moderate/Weak",
        "counterarguments": ["Potential counterargument 1", "Potential counterargument 2", ...],
        "suggestions_for_improvement": ["Suggestion 1", "Suggestion 2", ...],
        "overall_assessment": "A summary of the evaluation and final judgment"
    }}
    """

    response = process_prompt(prompt, "llama3.1:latest", "ReasoningEvaluator")
    return json.loads(response)
