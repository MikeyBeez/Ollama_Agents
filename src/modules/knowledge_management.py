# src/modules/knowledge_management.py

import json
from typing import List, Tuple, Dict, Any
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from src.modules.errors import ModelInferenceError, DataProcessingError

def classify_query_topic(query: str, model_name: str) -> Tuple[str, float]:
    """
    Classify the given query into a topic and provide a confidence score.

    Args:
    query (str): The user's query to classify.
    model_name (str): The name of the model to use for classification.

    Returns:
    Tuple[str, float]: A tuple containing the classified topic and the confidence score.
    """
    logger.info(f"Classifying query topic: {query[:50]}...")  # Log only first 50 chars for brevity
    classification_prompt = f"""
    Classify the following query into a general topic area: "{query}"

    Provide your response in the following JSON format:
    {{
        "topic": "The most relevant topic",
        "confidence": 0.95
    }}

    Ensure the confidence is a float between 0 and 1.
    """
    try:
        response = process_prompt(classification_prompt, model_name, "TopicClassifier")
        result = json.loads(response)
        return result['topic'], result['confidence']
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON from classify_query_topic: {str(e)}")
        raise ModelInferenceError(f"Failed to parse topic classification result: {str(e)}")
    except KeyError as e:
        logger.error(f"Missing key in topic classification result: {str(e)}")
        raise DataProcessingError(f"Invalid topic classification result: {str(e)}")

def determine_research_depth(query: str, model_name: str) -> int:
    """
    Determine the appropriate research depth for a given query.

    Args:
    query (str): The user's query to analyze.
    model_name (str): The name of the model to use for analysis.

    Returns:
    int: A number between 1 and 5 indicating the research depth.
    """
    logger.info(f"Determining research depth for query: {query[:50]}...")
    depth_prompt = f"On a scale of 1 to 5, how deep should the research go for this query: '{query}'? Respond with ONLY a single integer between 1 and 5."
    try:
        response = process_prompt(depth_prompt, model_name, "ResearchDepthDeterminer")
        depth = int(response.strip())
        return max(1, min(depth, 5))
    except ValueError as e:
        logger.error(f"Error parsing research depth: {str(e)}")
        return 3  # Default to medium depth if there's an error

def process_query(user_input: str, model_name: str) -> Dict[str, Any]:
    """
    Process a user query to extract topic, confidence, and research depth.

    Args:
    user_input (str): The user's input query.
    model_name (str): The name of the model to use for processing.

    Returns:
    Dict[str, Any]: A dictionary containing topic, confidence, and depth.
    """
    logger.info(f"Processing query: {user_input[:50]}...")
    topic, confidence = classify_query_topic(user_input, model_name)
    depth = determine_research_depth(user_input, model_name)
    return {
        "topic": topic,
        "confidence": confidence,
        "depth": depth
    }

def assess_source_credibility(source: str, model_name: str) -> float:
    """
    Assess the credibility of a given source.

    Args:
    source (str): The source text to assess.
    model_name (str): The name of the model to use for assessment.

    Returns:
    float: A credibility score between 0 and 1.
    """
    logger.info("Assessing source credibility")
    credibility_prompt = f"""Assess the credibility of this source on a scale of 0 to 1:
    {source}

    Respond with ONLY a number between 0 and 1, where 0 is not credible at all and 1 is extremely credible.
    """
    try:
        credibility_response = process_prompt(credibility_prompt, model_name, "CredibilityAssessor")
        credibility_score = float(credibility_response.strip())
        return max(0, min(credibility_score, 1))
    except ValueError as e:
        logger.error(f"Error parsing credibility score: {str(e)}")
        return 0.5  # Default to neutral credibility if there's an error

def update_knowledge_base(new_info: str, topic: str, model_name: str) -> None:
    """
    Update the knowledge base with new information on a given topic.

    Args:
    new_info (str): The new information to add to the knowledge base.
    topic (str): The topic related to the new information.
    model_name (str): The name of the model to use for updating.
    """
    logger.info(f"Updating knowledge base for topic: {topic}")
    update_prompt = f"Incorporate this new information into the knowledge base for the topic '{topic}': {new_info}"
    process_prompt(update_prompt, model_name, "KnowledgeBaseUpdater")

def extract_key_concepts(text: str, model_name: str) -> List[str]:
    """
    Extract key concepts from a given text.

    Args:
    text (str): The text to extract concepts from.
    model_name (str): The name of the model to use for extraction.

    Returns:
    List[str]: A list of key concepts extracted from the text.
    """
    logger.info("Extracting key concepts from text")
    extraction_prompt = f"Extract the key concepts from the following text as a comma-separated list: {text}"
    try:
        concepts = process_prompt(extraction_prompt, model_name, "ConceptExtractor")
        return [concept.strip() for concept in concepts.split(',')]
    except Exception as e:
        logger.error(f"Error extracting key concepts: {str(e)}")
        return []

def generate_follow_up_questions(context: str, model_name: str) -> List[str]:
    """
    Generate follow-up questions based on the given context.

    Args:
    context (str): The context to base the questions on.
    model_name (str): The name of the model to use for generation.

    Returns:
    List[str]: A list of generated follow-up questions.
    """
    logger.info("Generating follow-up questions")
    question_prompt = f"Based on the following context, generate 3 relevant follow-up questions:\n\n{context}"
    try:
        questions = process_prompt(question_prompt, model_name, "QuestionGenerator")
        return [q.strip() for q in questions.split('\n') if q.strip()]
    except Exception as e:
        logger.error(f"Error generating follow-up questions: {str(e)}")
        return []

def summarize_topic(topic: str, context: str, model_name: str) -> str:
    """
    Generate a summary of a given topic based on the provided context.

    Args:
    topic (str): The topic to summarize.
    context (str): The context information about the topic.
    model_name (str): The name of the model to use for summarization.

    Returns:
    str: A summary of the topic.
    """
    logger.info(f"Summarizing topic: {topic}")
    summary_prompt = f"""Summarize the following information about the topic '{topic}':

    {context}

    Provide a concise summary that captures the key points and main ideas.
    """
    try:
        summary = process_prompt(summary_prompt, model_name, "TopicSummarizer")
        return summary
    except Exception as e:
        logger.error(f"Error summarizing topic: {str(e)}")
        return f"Unable to summarize topic '{topic}' due to an error."
