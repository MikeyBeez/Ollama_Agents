# src/modules/knowledge_extraction/json_response_parser.py

import json
from typing import Any, Dict, List
from src.modules.logging_setup import logger

def extract_json_from_response(response: str) -> Any:
    try:
        # Find the first occurrence of '{' and the last occurrence of '}'
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end != -1:
            json_str = response[start:end]
            return json.loads(json_str)
        else:
            raise ValueError("No valid JSON found in the response")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON: {e}")
        return None

def handle_extraction_error(e: Exception, error_message: str) -> Dict[str, Any]:
    logger.error(f"{error_message}: {e}")
    return {}

def parse_list_response(response: str) -> List[str]:
    try:
        data = extract_json_from_response(response)
        if isinstance(data, list):
            return data
        else:
            logger.error(f"Expected a list, but got: {type(data)}")
            return []
    except Exception as e:
        logger.error(f"Error parsing list response: {e}")
        return []

def parse_dict_response(response: str) -> Dict[str, Any]:
    try:
        data = extract_json_from_response(response)
        if isinstance(data, dict):
            return data
        else:
            logger.error(f"Expected a dictionary, but got: {type(data)}")
            return {}
    except Exception as e:
        logger.error(f"Error parsing dictionary response: {e}")
        return {}
