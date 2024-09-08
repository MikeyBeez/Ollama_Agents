# src/modules/apply_analogy.py

import json
from typing import Dict, Any
from src.modules.ollama_client import process_prompt

def apply_analogy(source_domain: str, target_domain: str, analogy_mapping: Dict[str, str]) -> Dict[str, Any]:
    """
    Apply an analogy from a source domain to a target domain.

    Args:
    source_domain (str): Description of the source domain.
    target_domain (str): Description of the target domain.
    analogy_mapping (Dict[str, str]): Mapping of concepts from source to target domain.

    Returns:
    Dict[str, Any]: A dictionary containing the applied analogy, its implications,
                    and an assessment of its strength and limitations.
    """
    prompt = f"""
    Apply the following analogy:

    Source Domain:
    {source_domain}

    Target Domain:
    {target_domain}

    Analogy Mapping:
    {json.dumps(analogy_mapping, indent=2)}

    Apply the analogy from the source domain to the target domain. Analyze the implications,
    assess the strength of the analogy, and identify any limitations or potential issues.
    Return your analysis in the following JSON format:

    {{
        "applied_analogy": "Detailed description of how the analogy applies to the target domain",
        "key_insights": ["Insight 1", "Insight 2", ...],
        "implications": [
            {{
                "implication": "Description of an implication",
                "relevance": "High/Medium/Low"
            }},
            ...
        ],
        "analogy_strength": "Strong/Moderate/Weak",
        "analogy_limitations": ["Limitation 1", "Limitation 2", ...],
        "potential_issues": ["Issue 1", "Issue 2", ...],
        "novel_predictions": ["Prediction 1", "Prediction 2", ...],
        "suggested_refinements": ["Refinement 1", "Refinement 2", ...],
        "overall_assessment": "A summary of the analogy's applicability and value"
    }}
    """

    response = process_prompt(prompt, "llama3.1:latest", "AnalogyApplier")
    return json.loads(response)
