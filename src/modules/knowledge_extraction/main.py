# src/modules/knowledge_extraction/main.py

from typing import Dict, Any
from src.modules.logging_setup import logger
from .key_concept_extractor import extract_key_concepts
from .named_entity_recognizer import extract_named_entities
from .entity_relationship_extractor import extract_entities_and_relationships
from .query_topic_analyzer import analyze_query_topic
from .text_sentiment_analyzer import analyze_sentiment

def extract_knowledge(text: str) -> Dict[str, Any]:
    """
    Extract various types of knowledge from the given text.

    Args:
    text (str): The input text to extract knowledge from.

    Returns:
    Dict[str, Any]: A dictionary containing different types of extracted knowledge.
    """
    try:
        logger.info(f"Extracting knowledge from text: {text[:100]}...")  # Log first 100 chars

        knowledge = {
            "key_concepts": extract_key_concepts(text),
            "named_entities": extract_named_entities(text),
            "entities_and_relationships": extract_entities_and_relationships(text),
            "query_topic": analyze_query_topic(text),
            "sentiment": analyze_sentiment(text)
        }

        logger.info("Knowledge extraction completed successfully")
        logger.debug(f"Extracted knowledge: {knowledge}")

        return knowledge

    except Exception as e:
        logger.error(f"Error in knowledge extraction: {str(e)}")
        logger.exception(e)
        return {
            "error": f"Failed to extract knowledge: {str(e)}",
            "key_concepts": [],
            "named_entities": [],
            "entities_and_relationships": {"entities": [], "relationships": []},
            "query_topic": {},
            "sentiment": {}
        }
