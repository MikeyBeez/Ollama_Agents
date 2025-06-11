# src/modules/knowledge_extraction/entity_relationship_extractor.py

from typing import Dict, List
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from .extraction_constants import APPROVED_ENTITY_LABELS, APPROVED_RELATIONSHIPS
from .json_response_parser import extract_json_from_response, handle_extraction_error

def extract_entities_and_relationships(text: str) -> Dict[str, List[Dict[str, str]]]:
    prompt = f"""
    Extract entities and relationships from the following text:
    "{text}"

    Provide your response as a JSON object with the following structure:
    {{
        "entities": [
            {{"text": "entity text", "label": "ENTITY_LABEL"}},
            ...
        ],
        "relationships": [
            {{"subject": "subject entity", "relationship": "RELATIONSHIP_TYPE", "object": "object entity"}},
            ...
        ]
    }}

    Use only the following entity labels: {', '.join(APPROVED_ENTITY_LABELS)}
    Use only the following relationship types: {', '.join(APPROVED_RELATIONSHIPS)}
    """

    try:
        response = process_prompt(prompt, "llama3.1:latest", "EntityRelationshipExtractor")
        logger.debug(f"Raw response from Ollama: {response}")

        result = extract_json_from_response(response)

        entities = [
            e for e in result.get('entities', [])
            if isinstance(e, dict) and 'text' in e and 'label' in e and e['label'] in APPROVED_ENTITY_LABELS
        ]
        relationships = [
            r for r in result.get('relationships', [])
            if isinstance(r, dict) and 'subject' in r and 'relationship' in r and 'object' in r
            and r['relationship'] in APPROVED_RELATIONSHIPS
        ]

        return {"entities": entities, "relationships": relationships}
    except Exception as e:
        return handle_extraction_error(e, "Error in extract_entities_and_relationships")
