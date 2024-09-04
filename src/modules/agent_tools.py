import json
from typing import Dict, Any, List
from rich.console import Console
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from src.modules.memory_search import search_memories
from src.modules.save_history import chat_history
from src.modules.ddg_search import DDGSearch

console = Console()
ddg_search = DDGSearch()

def analyze_input(user_input: str, model_name: str) -> Dict[str, Any]:
    analysis_prompt = f"""Analyze the following user input:
    "{user_input}"
    Provide a JSON output with the following fields:
    - input_type: The type of input (question, command, statement, etc.)
    - topics: Main topics or keywords
    - complexity: Low, medium, or high
    - sentiment: Positive, negative, or neutral
    - requires_search: true if web search might be helpful, false otherwise
    - requires_memory: true if searching past interactions might be helpful, false otherwise"""

    analysis_result = process_prompt(analysis_prompt, model_name, "Analyzer")
    try:
        return json.loads(analysis_result)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse analysis result: {analysis_result}")
        return {}

def gather_context(user_input: str, analysis: Dict[str, Any], context: str, agent_name: str) -> str:
    if analysis.get('requires_memory', False):
        memories = search_memories(user_input, top_k=3, similarity_threshold=0.7)
        memory_context = "\n".join([f"Memory: {m['content']}" for m in memories])
        context += f"\nRelevant memories:\n{memory_context}"

    if analysis.get('requires_search', False) and "Search results for" not in context:
        search_query = refine_search_query(user_input, analysis)
        search_results = ddg_search.run_search(search_query)
        filtered_results = filter_search_results(user_input, search_results)
        context += f"\nWeb search results:\n{filtered_results}"

    recent_history = chat_history.get_history()[-3:]
    history_context = "\n".join([f"User: {h['prompt']}\n{agent_name}: {h['response']}" for h in recent_history])
    context += f"\nRecent conversation:\n{history_context}"

    return context

def refine_search_query(user_input: str, analysis: Dict[str, Any]) -> str:
    refine_prompt = f"""Given the user query: '{user_input}'
    and this analysis: {json.dumps(analysis)}
    Generate a concise and specific web search query to find relevant information.
    Query:"""

    return process_prompt(refine_prompt, DEFAULT_MODEL, "QueryRefiner").strip()

def filter_search_results(query: str, results: List[str]) -> str:
    result_text = "\n".join(results[:5])
    filter_prompt = f"""Given the query: '{query}' and these search results:
    {result_text}

    Provide a concise summary of the most relevant information:"""

    return process_prompt(filter_prompt, DEFAULT_MODEL, "ResultFilter")

def generate_response(user_input: str, context: str, analysis: Dict[str, Any], agent_name: str, model_name: str) -> str:
    response_prompt = f"""As {agent_name}, respond to the user's input:
    "{user_input}"

    Consider this context:
    {context}

    And this analysis:
    {json.dumps(analysis)}

    Generate a comprehensive and informative response that:
    1. Directly addresses the user's query
    2. Incorporates relevant research findings
    3. Provides clear explanations and examples
    4. Offers practical advice or next steps
    5. Acknowledges any limitations or uncertainties

    If you need more information to provide a complete answer, ask a clarifying question instead of giving a full response:"""

    return process_prompt(response_prompt, model_name, "ResponseGenerator")

def needs_clarification(response: str) -> bool:
    return '?' in response and len(response.split()) < 20

def refine_response(user_input: str, initial_response: str, context: str, model_name: str) -> str:
    refine_prompt = f"""Given the user's input: "{user_input}"
    And the initial response: "{initial_response}"
    And this context: {context}

    Refine the response to ensure it is:
    1. Comprehensive and informative
    2. Directly addressing the user's input
    3. Factually accurate and up-to-date
    4. Coherent and well-structured
    5. Empathetic and appropriate in tone
    6. Not repetitive

    Provide only the refined response, without repeating the original input or initial response:"""

    return process_prompt(refine_prompt, model_name, "ResponseRefiner")

def evaluate_step(content: str, step_name: str, model_name: str) -> str:
    critique_prompt = f"""As a critic, evaluate the following {step_name}:
    {content}

    Provide a critique highlighting strengths, weaknesses, and areas for improvement:"""

    critique = process_prompt(critique_prompt, model_name, "Critic")

    contrary_prompt = f"""As a devil's advocate, provide a contrary perspective to the following {step_name}:
    {content}

    Offer alternative viewpoints or potential issues that may have been overlooked:"""

    contrary_view = process_prompt(contrary_prompt, model_name, "DevilsAdvocate")

    judge_prompt = f"""As an impartial judge, evaluate the original {step_name}, the critique, and the contrary perspective:

    Original:
    {content}

    Critique:
    {critique}

    Contrary Perspective:
    {contrary_view}

    Provide a balanced judgment, highlighting what to keep, what to discard, and any necessary adjustments:"""

    judgment = process_prompt(judge_prompt, model_name, "Judge")

    console.print(f"[bold yellow]Critique of {step_name}:[/bold yellow]\n{critique}")
    console.print(f"[bold red]Contrary perspective on {step_name}:[/bold red]\n{contrary_view}")
    console.print(f"[bold green]Judgment on {step_name}:[/bold green]\n{judgment}")

    return judgment
