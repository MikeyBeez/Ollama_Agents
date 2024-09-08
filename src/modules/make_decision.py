# src/modules/make_decision.py

import json
from typing import List, Dict, Any
from src.modules.ollama_client import process_prompt

def make_decision(options: List[str], criteria: List[str], preferences: Dict[str, float]) -> Dict[str, Any]:
    """
    Make a decision based on given options, criteria, and preferences.

    Args:
    options (List[str]): List of available options.
    criteria (List[str]): List of criteria for evaluating options.
    preferences (Dict[str, float]): Dictionary of criteria and their importance (0-1).

    Returns:
    Dict[str, Any]: A dictionary containing the decision analysis, including the
                    recommended option and a breakdown of the decision-making process.
    """
    prompt = f"""
    Make a decision based on the following information:

    Options:
    {json.dumps(options, indent=2)}

    Criteria:
    {json.dumps(criteria, indent=2)}

    Preferences (importance of each criterion, 0-1):
    {json.dumps(preferences, indent=2)}

    Analyze the options based on the given criteria and preferences. Provide a
    comprehensive decision analysis, including a recommendation and the reasoning
    behind it. Return your analysis in the following JSON format:

    {{
        "recommended_option": "Name of the recommended option",
        "recommendation_confidence": 0.0 to 1.0,
        "option_analysis": [
            {{
                "option": "Option name",
                "pros": ["Pro 1", "Pro 2", ...],
                "cons": ["Con 1", "Con 2", ...],
                "score": 0.0 to 10.0
            }},
            ...
        ],
        "criteria_breakdown": [
            {{
                "criterion": "Criterion name",
                "importance": 0.0 to 1.0,
                "option_scores": {{
                    "Option 1": 0.0 to 10.0,
                    "Option 2": 0.0 to 10.0,
                    ...
                }}
            }},
            ...
        ],
        "decision_process": "Explanation of the decision-making process",
        "sensitivity_analysis": "Analysis of how changes in preferences might affect the decision",
        "alternative_recommendations": ["Alternative 1", "Alternative 2", ...],
        "additional_considerations": ["Consideration 1", "Consideration 2", ...],
        "overall_summary": "A summary of the decision analysis and final recommendation"
    }}
    """

    response = process_prompt(prompt, "llama3.1:latest", "DecisionMaker")
    return json.loads(response)
