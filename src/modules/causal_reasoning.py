# src/modules/causal_reasoning.py

import json
from typing import List, Dict, Any
from src.modules.ollama_client import generate_response
from src.modules.logging_setup import logger

def infer_causal_relationships(context: str, model_name: str) -> List[Dict[str, Any]]:
    """
    Infer causal relationships from the given context.

    Args:
    context (str): The context to analyze for causal relationships.
    model_name (str): The name of the language model to use.

    Returns:
    List[Dict[str, Any]]: A list of inferred causal relationships.
    """
    prompt = f"""
    Analyze the following context and infer potential causal relationships:

    {context}

    Identify cause-and-effect relationships, considering both direct and indirect causes.
    For each relationship, provide a brief explanation and a confidence score (0-1).

    Format your response as a JSON array of objects with the following structure:
    [
        {{
            "cause": "Identified cause",
            "effect": "Resulting effect",
            "explanation": "Brief explanation of the relationship",
            "confidence": 0.8
        }},
        ...
    ]
    """

    try:
        response = generate_response(prompt, model_name, "CausalReasoner")
        causal_relationships = json.loads(response)
        logger.info(f"Inferred {len(causal_relationships)} causal relationships")
        return causal_relationships
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON from causal inference: {response}")
        return []
    except Exception as e:
        logger.error(f"Error in causal inference: {str(e)}")
        return []

def analyze_causal_chain(event: str, context: str, model_name: str) -> Dict[str, Any]:
    """
    Analyze the causal chain leading to a specific event.

    Args:
    event (str): The event to analyze.
    context (str): Additional context information.
    model_name (str): The name of the language model to use.

    Returns:
    Dict[str, Any]: A dictionary representing the causal chain.
    """
    prompt = f"""
    Analyze the causal chain leading to the following event:

    Event: {event}
    Context: {context}

    Provide a step-by-step breakdown of the causal chain, including:
    1. Root causes
    2. Intermediate factors
    3. Direct triggers

    Format your response as a JSON object with the following structure:
    {{
        "event": "The analyzed event",
        "root_causes": ["Cause 1", "Cause 2", ...],
        "intermediate_factors": ["Factor 1", "Factor 2", ...],
        "direct_triggers": ["Trigger 1", "Trigger 2", ...],
        "explanation": "A brief explanation of the causal chain"
    }}
    """

    try:
        response = generate_response(prompt, model_name, "CausalChainAnalyzer")
        causal_chain = json.loads(response)
        logger.info(f"Analyzed causal chain for event: {event}")
        return causal_chain
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON from causal chain analysis: {response}")
        return {}
    except Exception as e:
        logger.error(f"Error in causal chain analysis: {str(e)}")
        return {}
