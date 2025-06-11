# src/modules/knowledge_extraction/query_topic_analyzer.py

from typing import Dict, Any
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from .json_response_parser import extract_json_from_response, handle_extraction_error

def analyze_query_topic(query: str, model_name: str) -> Dict[str, Any]:
    prompt = f"""
    Analyze the following query:
    "{query}"

    Provide your response as a JSON object with the following structure:
    {{
        "topic": "The main topic of the query",
        "confidence": 0.0 to 1.0,
        "depth": 1 to 5
    }}
    """

    try:
        response = process_prompt(prompt, model_name, "QueryAnalyzer")
        logger.debug(f"Raw response from QueryAnalyzer: {response}")

        result = extract_json_from_response(response)

        if 'topic' in result and 'confidence' in result and 'depth' in result:
            result['confidence'] = float(result['confidence'])
            result['depth'] = int(result['depth'])
            return result
        else:
            raise ValueError("Missing required keys in query analysis result")
    except Exception as e:
        return handle_extraction_error(e, "Error in query analysis")
