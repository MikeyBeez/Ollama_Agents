# src/modules/agent_tools.py

import json
from typing import List, Dict, Any, Callable, Tuple
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from rich.console import Console
from rich.panel import Panel

console = Console()

def analyze_user_input(user_input: str, model_name: str) -> Dict[str, Any]:
    """
    Analyze the user's input to determine its characteristics.
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

def generate_response(user_input: str, context: str, analysis: Dict[str, Any], agent_name: str, model_name: str) -> str:
    """
    Generate a response based on user input and context.
    """
    logger.info("Generating response based on user input and context")
    response_prompt = f"""Given the user query: "{user_input}"
    And this context: {context}
    And this analysis: {json.dumps(analysis)}

    Generate a helpful and informative response as {agent_name} that:
    1. Directly addresses the user's query and intention
    2. Incorporates relevant research findings
    3. Provides clear explanations or instructions as needed
    4. Acknowledges any limitations or uncertainties in the information
    5. Suggests areas for further research if applicable

    Ensure the response is accurate, ethical, and helpful.
    Limit your response to 200 words.
    """
    return process_prompt(response_prompt, model_name, "ResponseGenerator")

def update_bullet_points(response: str, model_name: str) -> List[str]:
    """
    Extract key points from a given response.
    """
    logger.info("Extracting bullet points from response")
    bullet_prompt = f"Extract 3-5 key points from this text as a bullet point list: {response}"
    bullets = process_prompt(bullet_prompt, model_name, "BulletPointExtractor")
    return [b.strip() for b in bullets.split('\n') if b.strip()]

def rank_bullet_points(bullet_points: List[str], model_name: str, max_points: int = 15) -> List[str]:
    """
    Rank and trim a list of bullet points.
    """
    logger.info(f"Ranking bullet points, keeping top {max_points}")
    if len(bullet_points) > max_points:
        rank_prompt = "Rank the following bullet points by importance and relevance:\n" + "\n".join(bullet_points)
        ranked = process_prompt(rank_prompt, model_name, "BulletPointRanker")
        return [b.strip() for b in ranked.split('\n') if b.strip()][:max_points]
    return bullet_points

def interactive_followup(context: str, model_name: str, process_func: Callable[[str], str]) -> str:
    """
    Generate follow-up questions and handle user interaction for further exploration.
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

def generate_search_queries(user_input: str, model_name: str) -> List[str]:
    """
    Generate search queries based on user input.
    """
    logger.info("Generating search queries")
    query_prompt = f"""Based on the following user input, generate 3 relevant search queries:
    "{user_input}"
    Provide your response as a comma-separated list of queries.
    """
    queries = process_prompt(query_prompt, model_name, "SearchQueryGenerator")
    return [q.strip() for q in queries.split(',') if q.strip()]

def summarize_search_results(results: List[str], model_name: str) -> str:
    """
    Summarize search results.
    """
    logger.info("Summarizing search results")
    summary_prompt = f"""Summarize the following search results:
    {' '.join(results)}
    Provide a concise summary that captures the main points and relevant information.
    """
    return process_prompt(summary_prompt, model_name, "SearchSummarizer")

def evaluate_response(response: str, user_input: str, model_name: str) -> Dict[str, Any]:
    """
    Evaluate the quality and relevance of a generated response.
    """
    logger.info("Evaluating response quality and relevance")
    eval_prompt = f"""Evaluate the following response to the user input:
    User Input: "{user_input}"
    Response: "{response}"

    Provide your evaluation in the following JSON format:
    {{
        "relevance": 0.0 to 1.0,
        "completeness": 0.0 to 1.0,
        "clarity": 0.0 to 1.0,
        "accuracy": 0.0 to 1.0,
        "suggestions": ["Suggestion 1", "Suggestion 2"]
    }}
    """
    eval_result = process_prompt(eval_prompt, model_name, "ResponseEvaluator")
    try:
        return json.loads(eval_result)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON: {eval_result}")
        return {
            "relevance": 0.5,
            "completeness": 0.5,
            "clarity": 0.5,
            "accuracy": 0.5,
            "suggestions": ["Unable to provide specific suggestions due to evaluation error."]
        }

def generate_examples(concept: str, model_name: str, num_examples: int = 3) -> List[str]:
    """
    Generate examples for a given concept.
    """
    logger.info(f"Generating {num_examples} examples for concept: {concept}")
    example_prompt = f"""Generate {num_examples} diverse examples that illustrate the concept of "{concept}".
    Provide your response as a numbered list.
    """
    examples = process_prompt(example_prompt, model_name, "ExampleGenerator")
    return [e.strip() for e in examples.split('\n') if e.strip()]

def explain_concept(concept: str, model_name: str, complexity: str = "medium") -> str:
    """
    Explain a concept at a specified complexity level.
    """
    logger.info(f"Explaining concept: {concept} at {complexity} complexity")
    explanation_prompt = f"""Explain the concept of "{concept}" at a {complexity} level of complexity.
    Provide a clear and concise explanation that is appropriate for the specified complexity level.
    """
    return process_prompt(explanation_prompt, model_name, "ConceptExplainer")

def generate_analogies(concept: str, model_name: str, num_analogies: int = 2) -> List[str]:
    """
    Generate analogies for a given concept.
    """
    logger.info(f"Generating {num_analogies} analogies for concept: {concept}")
    analogy_prompt = f"""Generate {num_analogies} analogies that help explain the concept of "{concept}".
    Provide your response as a numbered list.
    """
    analogies = process_prompt(analogy_prompt, model_name, "AnalogyGenerator")
    return [a.strip() for a in analogies.split('\n') if a.strip()]

def fact_check(statement: str, model_name: str) -> Dict[str, Any]:
    """
    Perform a fact check on a given statement.
    """
    logger.info(f"Fact-checking statement: {statement}")
    fact_check_prompt = f"""Fact-check the following statement:
    "{statement}"

    Provide your response in the following JSON format:
    {{
        "is_factual": true or false,
        "confidence": 0.0 to 1.0,
        "explanation": "Explanation of the fact-check result",
        "sources": ["Source 1", "Source 2"]
    }}
    """
    fact_check_result = process_prompt(fact_check_prompt, model_name, "FactChecker")
    try:
        return json.loads(fact_check_result)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON: {fact_check_result}")
        return {
            "is_factual": False,
            "confidence": 0.0,
            "explanation": "Unable to perform fact-check due to an error.",
            "sources": []
        }

def find_analogies(current_problem: str, knowledge_base: str, model_name: str) -> List[Dict[str, str]]:
    """
    Find analogies between the current problem and situations in the knowledge base.
    """
    logger.info(f"Finding analogies for problem: {current_problem[:50]}...")
    analogy_prompt = f"""Given the current problem:
    "{current_problem}"

    And the following knowledge base:
    {knowledge_base}

    Find 3 analogous situations or concepts from the knowledge base that could help in understanding or solving the current problem.
    For each analogy, explain how it relates to the current problem and how it might be useful.

    Provide your response in the following JSON format:
    [
        {{
            "analogy": "Description of the analogous situation",
            "relation": "Explanation of how it relates to the current problem",
            "potential_use": "How this analogy might be useful in addressing the current problem"
        }},
        ...
    ]
    """
    analogy_result = process_prompt(analogy_prompt, model_name, "AnalogyFinder")
    try:
        return json.loads(analogy_result)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON: {analogy_result}")
        return []

def detect_contradictions(information_set: List[str], model_name: str) -> List[Dict[str, Any]]:
    """
    Detect contradictions within a set of information.
    """
    logger.info("Detecting contradictions in information set")
    contradiction_prompt = f"""Analyze the following set of information for any contradictions:
    {json.dumps(information_set)}

    Identify any statements that contradict each other. For each contradiction found, provide the conflicting statements and an explanation of the contradiction.

    Provide your response in the following JSON format:
    [
        {{
            "statement1": "First conflicting statement",
            "statement2": "Second conflicting statement",
            "explanation": "Explanation of why these statements contradict each other"
        }},
        ...
    ]
    """
    contradiction_result = process_prompt(contradiction_prompt, model_name, "ContradictionDetector")
    try:
        return json.loads(contradiction_result)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON: {contradiction_result}")
        return []

def resolve_contradictions(contradictions: List[Dict[str, Any]], model_name: str) -> List[Dict[str, Any]]:
    """
    Attempt to resolve detected contradictions.
    """
    logger.info("Resolving contradictions")
    resolution_prompt = f"""Given the following contradictions:
    {json.dumps(contradictions)}

    For each contradiction, provide a possible resolution or explanation that might reconcile the conflicting information.
    If a resolution is not possible, explain why and suggest how to proceed given the contradictory information.

    Provide your response in the following JSON format:
    [
        {{
            "contradiction": {{
                "statement1": "First conflicting statement",
                "statement2": "Second conflicting statement"
            }},
            "resolution": "Proposed resolution or explanation to reconcile the contradiction",
            "confidence": 0.0 to 1.0,
            "next_steps": "Suggested actions or further research if needed"
        }},
        ...
    ]
    """
    resolution_result = process_prompt(resolution_prompt, model_name, "ContradictionResolver")
    try:
        return json.loads(resolution_result)
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON: {resolution_result}")
        return []
