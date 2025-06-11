# src/modules/knowledge_extraction/named_entity_recognizer.py

from typing import List, Dict
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from .json_response_parser import parse_list_response, extract_json_from_response
from .extraction_constants import APPROVED_ENTITY_LABELS

def extract_named_entities(text: str) -> List[Dict[str, str]]:
    prompt = f"""
    Extract named entities from the following text:
    "{text}"

    Provide your response as a JSON array of objects with the following structure:
    [
        {{"text": "entity text", "label": "ENTITY_LABEL"}},
        ...
    ]

    Use only the following entity labels: {', '.join(APPROVED_ENTITY_LABELS)}
    """

    try:
        response = process_prompt(prompt, "llama3.1:latest", "NamedEntityRecognizer")
        logger.debug(f"Raw response from NamedEntityRecognizer: {response}")

        # Add this line to see what extract_json_from_response returns
        extracted_json = extract_json_from_response(response)
        logger.debug(f"Extracted JSON: {extracted_json}")

        entities = parse_list_response(response)
        logger.debug(f"Parsed entities: {entities}")

        result = [e for e in entities if isinstance(e, dict) and 'text' in e and 'label' in e and e['label'] in APPROVED_ENTITY_LABELS]
        logger.debug(f"Final result: {result}")

        return result
    except Exception as e:
        logger.error(f"Error extracting named entities: {e}")
        logger.exception(e)  # This will log the full stack trace
        return []
