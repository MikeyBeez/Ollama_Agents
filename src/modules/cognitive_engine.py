# src/modules/cognitive_engine.py

from typing import Dict, Any, List
import json
from src.modules.logging_setup import logger
from src.modules.agent_tools import analyze_user_input, generate_response, update_bullet_points, rank_bullet_points
from src.modules.knowledge_management import process_query, assess_source_credibility, update_knowledge_base, extract_key_concepts, summarize_topic
from src.modules.context_management import gather_context, update_context
from src.modules.research_tools import perform_research
from src.modules.memory_search import search_memories
from src.modules.kb_graph import get_related_nodes
from src.modules.assemble import assemble_prompt_with_history
from src.modules.errors import ModelInferenceError, DataProcessingError

def process_query_and_generate_response(user_input: str, model_name: str, context: str, conversation_history: List[Dict[str, str]], bullet_points: List[str], agent_name: str) -> Dict[str, Any]:
    """
    Process a user query, conduct research, and generate a comprehensive response with associated metadata.

    This function serves as the cognitive engine of the AI assistant, coordinating various analytical and generative tasks
    to provide an informed and context-aware response to the user's input.

    Args:
    user_input (str): The user's input query.
    model_name (str): The name of the AI model to use.
    context (str): The current context of the conversation.
    conversation_history (List[Dict[str, str]]): The conversation history.
    bullet_points (List[str]): The current list of key points.
    agent_name (str): The name of the agent.

    Returns:
    Dict[str, Any]: A dictionary containing the response and associated metadata, including analysis results,
                    research findings, and updated context information.
    """
    try:
        logger.info("Starting cognitive processing for user query")

        # Analyze user input
        input_analysis = analyze_user_input(user_input, model_name)
        logger.info(f"Input analysis: {input_analysis}")

        # Process query
        query_info = process_query(user_input, model_name)
        logger.info(f"Query info: {query_info}")

        # Gather context
        context = gather_context(user_input, query_info['topic'], conversation_history, bullet_points, agent_name)

        # Perform memory search
        memory_results = search_memories(user_input, top_k=3)
        logger.info(f"Found {len(memory_results)} relevant memories")

        # Get knowledge graph relations
        kg_relations = get_related_nodes(query_info['topic'])
        logger.info(f"Found {len(kg_relations)} knowledge graph relations")

        # Conduct research
        research_results = perform_research(user_input, query_info['topic'], model_name)
        logger.info("Completed research")

        # Update context with research results
        context = update_context(context, research_results, model_name)

        # Assemble full prompt
        full_prompt = assemble_prompt_with_history(user_input)

        # Generate response
        response = generate_response(full_prompt, context, input_analysis, agent_name, model_name)

        # Assess source credibility
        credibility = assess_source_credibility(response, model_name)
        logger.info(f"Response credibility: {credibility}")

        # Update knowledge base
        update_knowledge_base(response, query_info['topic'], model_name)

        # Extract key concepts
        key_concepts = extract_key_concepts(response, model_name)
        logger.info(f"Extracted key concepts: {key_concepts}")

        # Update bullet points
        new_bullets = update_bullet_points(response, model_name)
        bullet_points.extend(new_bullets)
        bullet_points = rank_bullet_points(bullet_points, model_name)

        # Summarize topic
        topic_summary = summarize_topic(query_info['topic'], context, model_name)

        return {
            'response': response,
            'input_analysis': input_analysis,
            'query_info': query_info,
            'context': context,
            'credibility': credibility,
            'key_concepts': key_concepts,
            'bullet_points': bullet_points,
            'topic_summary': topic_summary,
            'memory_results': memory_results,
            'kg_relations': kg_relations
        }

    except Exception as e:
        logger.exception(f"Error in cognitive processing: {str(e)}")
        raise DataProcessingError(f"An error occurred during processing: {str(e)}")

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

def process_prompt(prompt: str, model_name: str, system_name: str) -> str:
    """
    Process a prompt using the specified model.
    """
    try:
        from src.modules.ollama_client import process_prompt as ollama_process_prompt
        return ollama_process_prompt(prompt, model_name, system_name)
    except Exception as e:
        logger.error(f"Error processing prompt: {str(e)}")
        raise ModelInferenceError(f"Failed to process prompt: {str(e)}")
