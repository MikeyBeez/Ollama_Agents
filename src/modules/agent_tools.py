# src/modules/agent_tools.py

import json
from typing import List, Dict, Any, Callable
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from rich.console import Console
from rich.panel import Panel

console = Console()

def update_bullet_points(response: str, model_name: str) -> List[str]:
    """
    Extract key points from a given response.

    Args:
    response (str): The text to extract bullet points from.
    model_name (str): The name of the model to use for extraction.

    Returns:
    List[str]: A list of extracted bullet points.
    """
    logger.info("Extracting bullet points from response")
    bullet_prompt = f"Extract 3-5 key points from this text as a bullet point list: {response}"
    bullets = process_prompt(bullet_prompt, model_name, "BulletPointExtractor")
    return [b.strip() for b in bullets.split('\n') if b.strip()]

def rank_bullet_points(bullet_points: List[str], model_name: str, max_points: int = 15) -> List[str]:
    """
    Rank and trim a list of bullet points.

    Args:
    bullet_points (List[str]): The list of bullet points to rank.
    model_name (str): The name of the model to use for ranking.
    max_points (int): The maximum number of points to keep after ranking.

    Returns:
    List[str]: A ranked and trimmed list of bullet points.
    """
    logger.info(f"Ranking bullet points, keeping top {max_points}")
    if len(bullet_points) > max_points:
        rank_prompt = "Rank the following bullet points by importance and relevance:\n" + "\n".join(bullet_points)
        ranked = process_prompt(rank_prompt, model_name, "BulletPointRanker")
        return [b.strip() for b in ranked.split('\n') if b.strip()][:max_points]
    return bullet_points

def generate_response(user_input: str, context: str, model_name: str) -> str:
    """
    Generate a response based on user input and context.

    Args:
    user_input (str): The user's query or input.
    context (str): The context for the response.
    model_name (str): The name of the model to use for response generation.

    Returns:
    str: The generated response.
    """
    logger.info("Generating response based on user input and context")
    response_prompt = f"""Given the user query: "{user_input}"
    And this context: {context}

    Generate a helpful and informative response that:
    1. Directly addresses the user's query and intention
    2. Incorporates relevant research findings
    3. Provides clear explanations or instructions as needed
    4. Acknowledges any limitations or uncertainties in the information
    5. Suggests areas for further research if applicable

    Ensure the response is accurate, ethical, and helpful.
    Limit your response to 200 words.
    """
    return process_prompt(response_prompt, model_name, "ResponseGenerator")

def analyze_user_input(user_input: str, model_name: str) -> Dict[str, Any]:
    """
    Analyze the user's input to determine its characteristics.

    Args:
    user_input (str): The user's query or input.
    model_name (str): The name of the model to use for analysis.

    Returns:
    Dict[str, Any]: A dictionary containing analysis results.
    """
    logger.info("Analyzing user input")
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
    analysis_result = process_prompt(analysis_prompt, model_name, "InputAnalyzer")
    try:
        return json.loads(analysis_result)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON: {analysis_result}")
        return {
            "input_type": "unknown",
            "topics": [],
            "complexity": "medium",
            "sentiment": "neutral",
            "requires_research": True
        }

def interactive_followup(context: str, model_name: str, process_func: Callable[[str], str]) -> str:
    """
    Generate follow-up questions and handle user interaction for further exploration.

    Args:
    context (str): The current context of the conversation.
    model_name (str): The name of the model to use for generating questions.
    process_func (Callable[[str], str]): A function to process user input (usually the agent's main process_input function).

    Returns:
    str: The response to the chosen follow-up question or user input.
    """
    logger.info("Generating follow-up questions and handling user interaction")

    # Generate follow-up questions
    question_prompt = f"Based on the following context, generate 3 relevant follow-up questions:\n\n{context}"
    questions = process_prompt(question_prompt, model_name, "QuestionGenerator").split('\n')

    # Display questions to the user
    console.print(Panel("📚 Based on our conversation, here are some follow-up questions you might find interesting:", border_style="cyan"))
    for i, question in enumerate(questions, 1):
        console.print(f"  {i}. {question.strip()}")
    console.print("You can choose a number, ask your own question, or press Enter to skip.")

    # Get user input
    user_choice = console.input("Your choice (number, question, or Enter to skip): ")

    if user_choice.strip() == "":
        return "No follow-up question selected."

    if user_choice.isdigit() and 1 <= int(user_choice) <= len(questions):
        chosen_question = questions[int(user_choice) - 1].strip()
    else:
        chosen_question = user_choice

    # Process the chosen or entered question
    console.print(Panel(f"Processing follow-up: {chosen_question}", border_style="yellow"))
    followup_response = process_func(chosen_question)

    return f"Follow-up: {chosen_question}\n\nResponse: {followup_response}"
