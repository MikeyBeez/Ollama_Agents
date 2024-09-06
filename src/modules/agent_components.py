# src/modules/agent_components.py

from typing import Dict, Any, List, Tuple
from rich.console import Console
from rich.prompt import Prompt
from src.modules.logging_setup import logger
from src.modules.ollama_client import process_prompt
from src.modules.ddg_search import DDGSearch
from src.modules.save_history import chat_history
from src.modules.kb_graph import update_knowledge_graph, get_related_nodes
from src.modules.errors import InputError, DataProcessingError

console = Console()
ddg_search = DDGSearch()

def get_user_input(config: Dict[str, Any]) -> str:
    """
    Get input from the user.

    Args:
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        str: User input string.
    """
    try:
        return Prompt.ask(f"{config['USER_NAME']}> ")
    except KeyboardInterrupt:
        logger.info("Input interrupted by user")
        return "/q"

def analyze_input(user_input: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze the user input to determine its characteristics.

    Args:
        user_input (str): The user's input string.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        Dict[str, Any]: Analysis results including input type, topics, complexity, etc.
    """
    analysis_prompt = f"""Analyze the following user input:
    "{user_input}"
    Provide your response in the following JSON format:
    {{
        "input_type": "The type of input (question, command, statement, etc.)",
        "topics": ["Main topic 1", "Main topic 2"],
        "complexity": "Low, medium, or high",
        "sentiment": "Positive, negative, or neutral",
        "requires_research": true or false
    }}
    """
    analysis_result = process_prompt(analysis_prompt, config['DEFAULT_MODEL'], "InputAnalyzer")
    try:
        return eval(analysis_result)  # Note: In production, use json.loads() instead of eval()
    except Exception as e:
        logger.error(f"Failed to parse input analysis: {e}")
        return {
            "input_type": "unknown",
            "topics": [],
            "complexity": "medium",
            "sentiment": "neutral",
            "requires_research": True
        }

def gather_context(user_input: str, analysis: Dict[str, Any], config: Dict[str, Any]) -> str:
    """
    Gather context for the user input.

    Args:
        user_input (str): The user's input string.
        analysis (Dict[str, Any]): The analysis of the user input.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        str: Gathered context string.
    """
    context = f"User Input: {user_input}\n\nAnalysis: {analysis}\n\n"

    # Add recent conversation history
    recent_history = chat_history.get_history()[-3:]
    context += "Recent Conversation:\n" + "\n".join([f"User: {h['prompt']}\nAssistant: {h['response']}" for h in recent_history])

    # Add relevant knowledge graph information
    kg_nodes = get_related_nodes(user_input)
    if kg_nodes:
        context += "\n\nRelevant Knowledge:\n" + "\n".join([f"{node[0]} - {node[1]} - {node[2]}" for node in kg_nodes])

    return context

def retrieve_relevant_knowledge(context: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Retrieve relevant knowledge based on the context.

    Args:
        context (str): The gathered context.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        List[Dict[str, Any]]: List of relevant knowledge items.
    """
    # This is a placeholder. In a real implementation, this would query a knowledge base or perform a search.
    search_results = ddg_search.run_search(context[:100])  # Use first 100 chars of context as search query
    return [{"source": "web", "content": result} for result in search_results[:3]]

def generate_response(user_input: str, context: str, knowledge: List[Dict[str, Any]], config: Dict[str, Any]) -> str:
    """
    Generate a response based on user input, context, and relevant knowledge.

    Args:
        user_input (str): The user's input string.
        context (str): The gathered context.
        knowledge (List[Dict[str, Any]]): List of relevant knowledge items.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        str: Generated response string.
    """
    response_prompt = f"""Given the user query: "{user_input}"
    And this context: {context}
    And this relevant knowledge: {knowledge}

    Generate a helpful and informative response as {config['AGENT_NAME']} that:
    1. Directly addresses the user's query and intention
    2. Incorporates relevant research findings
    3. Provides clear explanations or instructions as needed
    4. Acknowledges any limitations or uncertainties in the information
    5. Suggests areas for further research if applicable

    Ensure the response is accurate, ethical, and helpful.
    """
    return process_prompt(response_prompt, config['DEFAULT_MODEL'], "ResponseGenerator")

def update_agent_knowledge(response: str, context: str, config: Dict[str, Any]) -> None:
    """
    Update the agent's knowledge based on the interaction.

    Args:
        response (str): The generated response.
        context (str): The interaction context.
        config (Dict[str, Any]): Configuration dictionary.
    """
    update_knowledge_graph(f"{context}\n\nResponse: {response}")
    chat_history.add_entry(context.split('\n')[0], response)  # Add to chat history

def generate_follow_up_questions(context: str, config: Dict[str, Any]) -> List[str]:
    """
    Generate follow-up questions based on the context.

    Args:
        context (str): The interaction context.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        List[str]: List of generated follow-up questions.
    """
    question_prompt = f"Based on the following context, generate 3 relevant follow-up questions:\n\n{context}"
    questions = process_prompt(question_prompt, config['DEFAULT_MODEL'], "QuestionGenerator")
    return [q.strip() for q in questions.split('\n') if q.strip()]

def assess_response_quality(response: str, context: str, config: Dict[str, Any]) -> Tuple[float, str]:
    """
    Assess the quality of the generated response.

    Args:
        response (str): The generated response.
        context (str): The interaction context.
        config (Dict[str, Any]): Configuration dictionary.

    Returns:
        Tuple[float, str]: Quality score (0-1) and explanation.
    """
    assessment_prompt = f"""Assess the quality of this response:
    Context: {context}
    Response: {response}

    Provide a quality score between 0 and 1, and a brief explanation.
    Format your response as: (score, "explanation")
    """
    result = process_prompt(assessment_prompt, config['DEFAULT_MODEL'], "QualityAssessor")
    try:
        return eval(result)  # Note: In production, use a more secure method to parse this
    except Exception as e:
        logger.error(f"Failed to parse quality assessment: {e}")
        return (0.5, "Failed to assess quality")
