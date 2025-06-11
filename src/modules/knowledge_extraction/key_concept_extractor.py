# src/modules/knowledge_extraction/key_concept_extractor.py

from typing import List
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from .json_response_parser import parse_list_response, extract_json_from_response

def extract_key_concepts(text: str) -> List[str]:
    prompt = f"""
    Extract the top 3 key concepts from the following text:
    "{text}"

    Provide your response as a JSON array of strings.
    """

    try:
        response = process_prompt(prompt, "llama3.1:latest", "KeyConceptExtractor")
        logger.debug(f"Raw response from KeyConceptExtractor: {response}")

        # Add this line to see what extract_json_from_response returns
        extracted_json = extract_json_from_response(response)
        logger.debug(f"Extracted JSON: {extracted_json}")

        concepts = parse_list_response(response)
        logger.debug(f"Parsed concepts: {concepts}")

        result = [concept.lower() for concept in concepts if isinstance(concept, str)][:3]
        logger.debug(f"Final result: {result}")

        return result
    except Exception as e:
        logger.error(f"Error extracting key concepts: {e}")
        logger.exception(e)  # This will log the full stack trace
        return []
