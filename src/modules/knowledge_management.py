# src/modules/knowledge_management.py

import json
import re
from typing import List, Tuple, Dict, Any
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from src.modules.errors import ModelInferenceError, DataProcessingError

def classify_query_topic(query: str, model_name: str) -> Tuple[str, float]:
    """
    Classify the given query into a topic and provide a confidence score.
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
        # Parse only the first valid JSON object
        json_start = response.find('{')
        json_end = response.find('}', json_start) + 1
        if json_start != -1 and json_end != -1:
            result = json.loads(response[json_start:json_end])
            return result['topic'], result['confidence']
        else:
            raise json.JSONDecodeError("No valid JSON found in response", response, 0)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON from classify_query_topic: {str(e)}")
        raise ModelInferenceError(f"Failed to parse topic classification result: {str(e)}")
    except KeyError as e:
        logger.error(f"Missing key in topic classification result: {str(e)}")
        raise DataProcessingError(f"Invalid topic classification result: {str(e)}")

def determine_research_depth(query: str, model_name: str) -> int:
    """
    Determine the appropriate research depth for a given query.
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
    """
    logger.info("Assessing source credibility")
    credibility_prompt = f"""Assess the credibility of this source on a scale of 0 to 1:
    {source}

    Respond with ONLY a number between 0 and 1, where 0 is not credible at all and 1 is extremely credible.
    If you cannot assess the credibility, respond with 0.5.
    """
    try:
        credibility_response = process_prompt(credibility_prompt, model_name, "CredibilityAssessor")
        score_match = re.search(r'\b(\d+(\.\d+)?)\b', credibility_response)
        if score_match:
            credibility_score = float(score_match.group(1))
            return max(0, min(credibility_score, 1))
        else:
            logger.warning(f"Could not extract numeric score from: {credibility_response}")
            return 0.5  # Default to neutral credibility if no score found
    except ValueError as e:
        logger.error(f"Error parsing credibility score: {str(e)}")
        return 0.5  # Default to neutral credibility if there's an error

def update_knowledge_base(new_info: str, topic: str, model_name: str) -> None:
    """
    Update the knowledge base with new information on a given topic.
    """
    logger.info(f"Updating knowledge base for topic: {topic}")
    update_prompt = f"Incorporate this new information into the knowledge base for the topic '{topic}': {new_info}"
    process_prompt(update_prompt, model_name, "KnowledgeBaseUpdater")

def extract_key_concepts(text: str, model_name: str) -> List[str]:
    """
    Extract key concepts from a given text.
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

def identify_knowledge_gaps(topic: str, current_knowledge: str, model_name: str) -> List[str]:
    """
    Identify gaps in the current knowledge about a given topic.
    """
    logger.info(f"Identifying knowledge gaps for topic: {topic}")
    gap_prompt = f"""Given the following current knowledge about the topic '{topic}':

    {current_knowledge}

    Identify and list potential gaps in this knowledge or areas that require further research.
    Provide your response as a bullet-point list.
    """
    try:
        gaps = process_prompt(gap_prompt, model_name, "KnowledgeGapIdentifier")
        return [gap.strip() for gap in gaps.split('\n') if gap.strip()]
    except Exception as e:
        logger.error(f"Error identifying knowledge gaps: {str(e)}")
        return []

def compare_information(info1: str, info2: str, model_name: str) -> Dict[str, Any]:
    """
    Compare two pieces of information and identify similarities and differences.
    """
    logger.info("Comparing information")
    compare_prompt = f"""Compare the following two pieces of information:

    Information 1:
    {info1}

    Information 2:
    {info2}

    Identify the key similarities and differences. Provide your response in the following JSON format:
    {{
        "similarities": ["Similarity 1", "Similarity 2"],
        "differences": ["Difference 1", "Difference 2"],
        "conflicting_points": ["Conflict 1", "Conflict 2"]
    }}
    """
    try:
        comparison = process_prompt(compare_prompt, model_name, "InformationComparer")
        return json.loads(comparison)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON from information comparison: {str(e)}")
        return {"similarities": [], "differences": [], "conflicting_points": []}

def validate_information(info: str, model_name: str) -> Dict[str, Any]:
    """
    Validate a piece of information and assess its reliability.
    """
    logger.info("Validating information")
    validation_prompt = f"""Validate the following information and assess its reliability:

    {info}

    Provide your assessment in the following JSON format:
    {{
        "reliability_score": 0.0 to 1.0,
        "potential_biases": ["Bias 1", "Bias 2"],
        "fact_check_needed": ["Fact 1", "Fact 2"],
        "supporting_evidence": ["Evidence 1", "Evidence 2"],
        "contradicting_evidence": ["Contradiction 1", "Contradiction 2"]
    }}
    """
    try:
        validation = process_prompt(validation_prompt, model_name, "InformationValidator")
        return json.loads(validation)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON from information validation: {str(e)}")
        return {
            "reliability_score": 0.5,
            "potential_biases": [],
            "fact_check_needed": [],
            "supporting_evidence": [],
            "contradicting_evidence": []
        }

def generate_knowledge_tree(topic: str, model_name: str) -> Dict[str, Any]:
    """
    Generate a knowledge tree for a given topic.
    """
    logger.info(f"Generating knowledge tree for topic: {topic}")
    tree_prompt = f"""Generate a knowledge tree for the topic '{topic}'.
    The tree should have main branches (key aspects of the topic) and sub-branches (details or sub-topics).
    Provide your response in the following JSON format:
    {{
        "topic": "Main Topic",
        "branches": [
            {{
                "name": "Branch 1",
                "sub_branches": ["Sub-branch 1", "Sub-branch 2"]
            }},
            {{
                "name": "Branch 2",
                "sub_branches": ["Sub-branch 1", "Sub-branch 2"]
            }}
        ]
    }}
    """
    try:
        tree = process_prompt(tree_prompt, model_name, "KnowledgeTreeGenerator")
        return json.loads(tree)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON from knowledge tree generation: {str(e)}")
        return {"topic": topic, "branches": []}

def evaluate_knowledge_consistency(statements: List[str], model_name: str) -> Dict[str, Any]:
    """
    Evaluate the consistency of a set of knowledge statements.
    """
    logger.info("Evaluating knowledge consistency")
    consistency_prompt = f"""Evaluate the consistency of the following statements:

    {json.dumps(statements, indent=2)}

    Identify any inconsistencies or contradictions. Provide your evaluation in the following JSON format:
    {{
        "consistency_score": 0.0 to 1.0,
        "inconsistencies": [
            {{
                "statements": ["Statement 1", "Statement 2"],
                "explanation": "Explanation of the inconsistency"
            }}
        ],
        "fully_consistent_statements": ["Statement 1", "Statement 2"]
    }}
    """
    try:
        evaluation = process_prompt(consistency_prompt, model_name, "ConsistencyEvaluator")
        return json.loads(evaluation)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON from consistency evaluation: {str(e)}")
        return {
            "consistency_score": 0.5,
            "inconsistencies": [],
            "fully_consistent_statements": []
        }
