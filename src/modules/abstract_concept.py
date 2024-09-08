# src/modules/abstract_concept.py

import json
from typing import List, Dict, Any
from src.modules.ollama_client import process_prompt

def abstract_concept(concrete_example: str, context: str = "") -> Dict[str, Any]:
    """
    Generate an abstract concept or principle from a concrete example.

    Args:
    concrete_example (str): A specific example or instance.
    context (str, optional): Additional context or domain information.

    Returns:
    Dict[str, Any]: A dictionary containing the abstracted concept, its properties,
                    and related information.
    """
    prompt = f"""
    Generate an abstract concept or principle from the following concrete example:

    Concrete Example:
    {concrete_example}

    Additional Context (if any):
    {context}

    Analyze the example, identify key features, and formulate an abstract concept or principle.
    Provide a comprehensive analysis of the abstraction process and the resulting concept.
    Return your analysis in the following JSON format:

    {{
        "abstract_concept": "Brief description of the abstracted concept",
        "key_features": ["Feature 1", "Feature 2", "..."],
        "generalization_process": "Explanation of how the abstraction was derived",
        "abstraction_level": "High/Medium/Low",
        "potential_applications": ["Application 1", "Application 2", "..."],
        "related_concepts": ["Concept 1", "Concept 2", "..."],
        "examples": [
            {{
                "example": "Another example fitting the abstract concept",
                "explanation": "How this example fits the concept"
            }},
            "..."
        ],
        "limitations": ["Limitation 1", "Limitation 2", "..."],
        "cross_domain_relevance": [
            {{
                "domain": "Name of a different domain",
                "relevance": "Explanation of how the concept applies in this domain"
            }},
            "..."
        ],
        "abstraction_hierarchy": {{
            "more_abstract": ["Higher level abstraction 1", "Higher level abstraction 2", "..."],
            "more_concrete": ["More specific concept 1", "More specific concept 2", "..."]
        }},
        "overall_assessment": "A summary of the abstraction's significance and potential impact"
    }}
    """

    response = process_prompt(prompt, "llama3.1:latest", "ConceptAbstractor")
    return json.loads(response)
