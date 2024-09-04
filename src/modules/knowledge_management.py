# src/modules/knowledge_management.py

from src.modules.logging_setup import logger
from src.modules.ollama_client import process_prompt
from src.modules.errors import ModelInferenceError, DataProcessingError

def classify_query_topic(query: str, model_name: str) -> str:
    try:
        classification_prompt = f"Classify the following query into a general topic area: {query}"
        return process_prompt(classification_prompt, model_name, "TopicClassifier")
    except Exception as e:
        raise ModelInferenceError(f"Error classifying query topic: {str(e)}")

def determine_research_depth(query: str, model_name: str) -> int:
    try:
        depth_prompt = f"On a scale of 1 to 5, how deep should the research go for this query: '{query}'? Respond with ONLY a single integer between 1 and 5."
        response = process_prompt(depth_prompt, model_name, "ResearchDepthDeterminer")
        depth = int(response.strip().split()[0])
        if 1 <= depth <= 5:
            return depth
        else:
            logger.warning(f"Invalid research depth: {depth}. Defaulting to 3.")
            return 3
    except Exception as e:
        logger.error(f"Error determining research depth: {str(e)}")
        return 3  # Default to medium depth if there's an error

def update_knowledge_base(new_info: str, topic: str, model_name: str) -> None:
    try:
        update_prompt = f"Incorporate this new information into the knowledge base for the topic '{topic}': {new_info}"
        process_prompt(update_prompt, model_name, "KnowledgeBaseUpdater")
    except Exception as e:
        raise DataProcessingError(f"Error updating knowledge base: {str(e)}")

def assess_source_credibility(source: str, model_name: str) -> float:
    try:
        credibility_prompt = f"Assess the credibility of this source on a scale of 0 to 1: {source}"
        credibility_score = float(process_prompt(credibility_prompt, model_name, "CredibilityAssessor"))
        return credibility_score
    except Exception as e:
        raise ModelInferenceError(f"Error assessing source credibility: {str(e)}")
