# src/modules/cognitive_engine.py

from typing import Dict, Any, List, Tuple
from src.modules.agent_tools import analyze_user_input, update_bullet_points, rank_bullet_points, generate_response, interactive_followup
from src.modules.knowledge_management import process_query, assess_source_credibility, update_knowledge_base, extract_key_concepts, summarize_topic
from src.modules.context_management import gather_context, update_context
from src.modules.research_tools import perform_research
from src.modules.logging_setup import logger
from src.modules.meta_processes import debug_panel, print_step, print_result, print_error

@debug_panel
def process_query_and_generate_response(user_input: str, model_name: str, context: str, conversation_history: List[Tuple[str, str]], bullet_points: List[str], agent_name: str) -> Dict[str, Any]:
    """
    Process a user query, conduct research, and generate a comprehensive response with associated metadata.

    This function serves as the cognitive engine of the AI assistant, coordinating various analytical and generative tasks
    to provide an informed and context-aware response to the user's input.

    Args:
    user_input (str): The user's input query.
    model_name (str): The name of the AI model to use.
    context (str): The current context of the conversation.
    conversation_history (List[Tuple[str, str]]): The conversation history.
    bullet_points (List[str]): The current list of key points.
    agent_name (str): The name of the agent.

    Returns:
    Dict[str, Any]: A dictionary containing the response and associated metadata, including analysis results,
                    research findings, and updated context information.
    """
    try:
        print_step("Initiating cognitive processing for user query")

        print_step("Analyzing user input")
        input_analysis = analyze_user_input(user_input, model_name)
        print_result("Input Analysis", input_analysis)

        print_step("Processing query")
        query_info = process_query(user_input, model_name)
        print_result("Query Info", query_info)

        print_step("Gathering context")
        context = gather_context(user_input, query_info['topic'], conversation_history, bullet_points, agent_name)

        print_step("Performing research")
        research_results = perform_research(user_input, query_info['topic'], model_name)

        print_step("Updating context")
        context = update_context(context, research_results, model_name)

        print_step("Generating response")
        response = generate_response(user_input, context, model_name)

        print_step("Assessing source credibility")
        credibility = assess_source_credibility(response, model_name)
        print_result("Credibility Score", f"{credibility:.2f}/1.00")

        print_step("Updating knowledge base")
        update_knowledge_base(response, query_info['topic'], model_name)

        print_step("Extracting key concepts")
        key_concepts = extract_key_concepts(response, model_name)
        print_result("Key Concepts", ", ".join(key_concepts))

        print_step("Updating bullet points")
        new_bullets = update_bullet_points(response, model_name)
        bullet_points.extend(new_bullets)
        bullet_points = rank_bullet_points(bullet_points, model_name)

        print_step("Summarizing topic")
        topic_summary = summarize_topic(query_info['topic'], context, model_name)
        print_result("Topic Summary", topic_summary)

        print_step("Handling interactive follow-up")
        followup = interactive_followup(context, model_name, lambda x: process_query_and_generate_response(x, model_name, context, conversation_history, bullet_points, agent_name)['response'])
        if followup != "No follow-up question selected.":
            response += f"\n\n{followup}"

        return {
            'response': response,
            'input_analysis': input_analysis,
            'query_info': query_info,
            'context': context,
            'credibility': credibility,
            'key_concepts': key_concepts,
            'bullet_points': bullet_points,
            'topic_summary': topic_summary
        }

    except Exception as e:
        logger.exception(f"Error in cognitive processing: {str(e)}")
        print_error(f"An error occurred during processing: {str(e)}")
        return {
            'response': f"An error occurred during processing: {str(e)}",
            'error': str(e)
        }
