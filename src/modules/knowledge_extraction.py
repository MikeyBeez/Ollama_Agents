# /Users/bard/Code/Ollama_Agents/src/modules/knowledge_extraction.py

from typing import List, Dict, Any
from src.modules.logging_setup import logger
from .knowledge_extraction.named_entity_recognizer import extract_named_entities
from .knowledge_extraction.entity_relationship_extractor import extract_entities_and_relationships
from .knowledge_extraction.query_topic_analyzer import analyze_query_topic
from .knowledge_extraction.text_sentiment_analyzer import analyze_sentiment

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

def extract_key_concepts_wrapper(text: str) -> List[str]:
    """Wrapper function for extract_key_concepts"""
    return extract_key_concepts(text)

def extract_named_entities_wrapper(text: str) -> List[Dict[str, str]]:
    """Wrapper function for extract_named_entities"""
    return extract_named_entities(text)

def extract_entities_and_relationships_wrapper(text: str) -> Dict[str, List[Dict[str, str]]]:
    """Wrapper function for extract_entities_and_relationships"""
    return extract_entities_and_relationships(text)

def analyze_query_topic_wrapper(text: str) -> Dict[str, Any]:
    """Wrapper function for analyze_query_topic"""
    return analyze_query_topic(text)

def analyze_sentiment_wrapper(text: str) -> Dict[str, Any]:
    """Wrapper function for analyze_sentiment"""
    return analyze_sentiment(text)
