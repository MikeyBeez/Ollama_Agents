# src/modules/evaluate_ethical_implications.py

import json
from typing import Dict, Any
from src.modules.ollama_client import process_prompt

def evaluate_ethical_implications(action: str, context: str) -> Dict[str, Any]:
    """
    Evaluate the ethical implications of a given action in a specific context.

    Args:
    action (str): The action or decision to be evaluated.
    context (str): The context or situation in which the action takes place.

    Returns:
    Dict[str, Any]: A dictionary containing the ethical analysis, including potential
                    consequences, stakeholder impacts, and overall ethical assessment.
    """
    prompt = f"""
    Evaluate the ethical implications of the following action in the given context:

    Action:
    {action}

    Context:
    {context}

    Provide a comprehensive ethical analysis, considering various ethical frameworks
    (e.g., utilitarianism, deontology, virtue ethics). Return your analysis in the following JSON format:

    {{
        "ethical_assessment": "Ethically Acceptable/Questionable/Unacceptable",
        "key_ethical_considerations": ["Consideration 1", "Consideration 2", ...],
        "potential_consequences": [
            {{
                "consequence": "Description of the consequence",
                "likelihood": "High/Medium/Low",
                "impact": "Positive/Negative",
                "severity": "High/Medium/Low"
            }},
            ...
        ],
        "stakeholder_impact": [
            {{
                "stakeholder": "Description of the stakeholder group",
                "impact": "Description of how they are impacted"
            }},
            ...
        ],
        "ethical_principles": [
            {{
                "principle": "Name of the ethical principle",
                "alignment": "Aligns/Conflicts",
                "explanation": "Explanation of how the action aligns or conflicts with this principle"
            }},
            ...
        ],
        "alternative_actions": ["Alternative 1", "Alternative 2", ...],
        "overall_analysis": "A summary of the ethical analysis and final judgment"
    }}
    """

    response = process_prompt(prompt, "llama3.1:latest", "EthicalEvaluator")
    return json.loads(response)
