# src/modules/query_processing.py

import json
from typing import List
from rich.console import Console
from src.modules.logging_setup import logger
from src.modules.ollama_client import process_prompt
from src.modules.errors import InputError, ModelInferenceError
from src.modules.context_management import announce_step, query_response, build_context
from src.modules.research_tools import basic_research

console = Console()

def process_user_input(user_input: str) -> str:
    try:
        console.print(f"[bold cyan]User Input:[/bold cyan] {user_input}")
        return user_input
    except Exception as e:
        raise InputError(f"Error processing user input: {str(e)}")

def evaluate(user_input: str, context: str, model_name: str) -> str:
    try:
        while True:
            announce_step("Self-Evaluation")

            evaluation_prompt = f"""Given the original input: '{user_input}' and the current context:
            {context}

            Evaluate your understanding and answer these questions:
            1. Are you confused about any aspect of the query or context?
            2. Do you need any clarification from the user?
            3. Can you provide a comprehensive answer based on the current information?

            Respond in JSON format with keys: 'confused' (boolean), 'questions' (list of strings), 'can_answer' (boolean)."""

            evaluation_response = process_prompt(evaluation_prompt, model_name, "SelfEvaluator")

            try:
                evaluation = json.loads(evaluation_response)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse evaluation JSON: {evaluation_response}")
                evaluation = {"confused": False, "questions": [], "can_answer": True}

            if evaluation.get('confused', False) or evaluation.get('questions', []):
                announce_step("Requesting User Clarification")
                questions = evaluation.get('questions', ["Can you provide more information or clarify your question?"])
                console.print("[bold cyan]I need some clarification:[/bold cyan]")
                for i, question in enumerate(questions, 1):
                    console.print(f"{i}. {question}")

                user_clarification = console.input("[bold green]Your response: [/bold green]")
                context += f"\nUser Clarification: {user_clarification}"

                new_query = query_response("research query", f"Original input: {user_input}\nUser clarification: {user_clarification}", model_name)
                basic_research(new_query, model_name)
                context = build_context(model_name)

            elif evaluation.get('can_answer', True):
                announce_step("Generating Answer")
                answer = query_response("final answer", f"Original input: {user_input}\nContext: {context}", model_name)
                return answer

            else:
                announce_step("Insufficient Information")
                console.print("[bold yellow]I don't have enough information to answer the question. Let me do more research.[/bold yellow]")
                new_query = query_response("additional research query", f"Original input: {user_input}\nCurrent context: {context}", model_name)
                basic_research(new_query, model_name)
                context = build_context(model_name)

    except Exception as e:
        logger.error(f"Error in evaluation process: {str(e)}")
        return f"I encountered an error while processing your request. Please try rephrasing your question or asking something else."

def format_response(response: str, format_type: str, model_name: str) -> str:
    try:
        format_prompt = f"Format the following response as a {format_type}: {response}"
        return process_prompt(format_prompt, model_name, "ResponseFormatter")
    except Exception as e:
        raise ModelInferenceError(f"Error formatting response: {str(e)}")

def process_user_feedback(feedback: str, original_response: str, model_name: str) -> str:
    try:
        feedback_prompt = f"Given the original response: '{original_response}' and user feedback: '{feedback}', provide an improved response."
        return process_prompt(feedback_prompt, model_name, "FeedbackProcessor")
    except Exception as e:
        raise ModelInferenceError(f"Error processing user feedback: {str(e)}")
