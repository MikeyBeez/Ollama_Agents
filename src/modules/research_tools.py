# src/modules/research_tools.py

from typing import List, Dict, Any
from src.modules.logging_setup import logger
from src.modules.ddg_search import DDGSearch
from src.modules.ollama_client import process_prompt

ddg_search = DDGSearch()

def perform_research(query: str, topic: str, model_name: str) -> str:
    """
    Perform research on a given query and topic.

    Args:
    query (str): The user's query.
    topic (str): The main topic of the query.
    model_name (str): The name of the AI model to use.

    Returns:
    str: A summary of the research findings.
    """
    logger.info(f"Performing research on topic: {topic}")

    # Perform web search
    search_results = ddg_search.run_search(f"{topic} {query}")

    # Summarize search results
    summary_prompt = f"""Summarize the following search results related to the query "{query}" on the topic "{topic}":

    {' '.join(search_results[:5])}

    Provide a comprehensive summary that captures the key points and main ideas.
    """

    try:
        research_summary = process_prompt(summary_prompt, model_name, "ResearchSummarizer")
        logger.info("Research summary generated")
        return research_summary
    except Exception as e:
        logger.error(f"Error in perform_research: {str(e)}")
        return f"Unable to complete research due to an error: {str(e)}"

def generate_search_queries(user_input: str, model_name: str) -> List[str]:
    """
    Generate search queries based on user input.

    Args:
    user_input (str): The user's original query.
    model_name (str): The name of the model to use for query generation.

    Returns:
    List[str]: A list of generated search queries.
    """
    logger.info(f"Generating search queries for: {user_input[:50]}...")
    prompt = f"""Generate three distinct search queries to find comprehensive information about: {user_input}
    Provide your response as a JSON list of strings.
    """
    try:
        response = process_prompt(prompt, model_name, "QueryGenerator")
        return eval(response)  # This assumes the model returns a valid Python list
    except Exception as e:
        logger.error(f"Error in generate_search_queries: {e}")
        return [user_input]  # Fallback to the original input

def analyze_search_results(search_results: List[str], model_name: str) -> Dict[str, Any]:
    """
    Analyze search results to extract key information.

    Args:
    search_results (List[str]): List of search result snippets.
    model_name (str): The name of the model to use for analysis.

    Returns:
    Dict[str, Any]: A dictionary containing analyzed information.
    """
    logger.info("Analyzing search results")
    analysis_prompt = f"""Analyze the following search results and extract key information:

    {' '.join(search_results)}

    Provide your analysis in the following JSON format:
    {{
        "main_topics": ["Topic 1", "Topic 2", "Topic 3"],
        "key_facts": ["Fact 1", "Fact 2", "Fact 3"],
        "controversies": ["Controversy 1", "Controversy 2"],
        "additional_questions": ["Question 1", "Question 2"]
    }}
    """
    try:
        analysis_response = process_prompt(analysis_prompt, model_name, "ResultAnalyzer")
        return eval(analysis_response)  # This assumes the model returns a valid Python dictionary
    except Exception as e:
        logger.error(f"Error in analyze_search_results: {e}")
        return {
            "main_topics": [],
            "key_facts": [],
            "controversies": [],
            "additional_questions": []
        }

def basic_research(input_text: str, model_name: str) -> List[str]:
    """
    Conduct basic research on a given input text.

    Args:
    input_text (str): The text to research.
    model_name (str): The name of the model to use for research.

    Returns:
    List[str]: A list of research findings.
    """
    logger.info(f"Conducting basic research on: {input_text[:50]}...")
    search_results = ddg_search.run_search(input_text)
    research_prompt = f"""Based on the following search results about "{input_text}":
    {' '.join(search_results[:5])}

    Provide a list of 3-5 key findings or pieces of information.
    Format each finding as a separate item in a Python list.
    """
    try:
        findings = process_prompt(research_prompt, model_name, "BasicResearcher")
        return eval(findings)  # This should return a list of strings
    except Exception as e:
        logger.error(f"Error in basic_research: {e}")
        return ["Unable to conduct basic research due to an error."]

def conduct_comprehensive_research(user_input: str, topic: str, model_name: str) -> str:
    """
    Perform comprehensive research on a given topic based on user input.

    Args:
    user_input (str): The user's original query.
    topic (str): The main topic of research.
    model_name (str): The name of the model to use for research.

    Returns:
    str: A comprehensive research summary.
    """
    logger.info(f"Performing comprehensive research on: {topic}")
    research_aspects = [
        "Latest developments and breakthroughs",
        "Expert opinions and consensus",
        "Potential applications and use cases",
        "Challenges and limitations",
        "Future prospects and predictions"
    ]

    comprehensive_results = []

    for aspect in research_aspects:
        logger.info(f"Researching aspect: {aspect}")
        search_query = f"{topic} {aspect} {user_input}"
        search_results = ddg_search.run_search(search_query)

        aspect_prompt = f"""Based on the following search results about {aspect} related to "{topic}" and "{user_input}":
        {' '.join(search_results[:3])}

        Provide a concise summary of the most relevant information:"""

        aspect_summary = process_prompt(aspect_prompt, model_name, "AspectResearcher")
        comprehensive_results.append(f"{aspect}:\n{aspect_summary}")

    full_research = "\n\n".join(comprehensive_results)

    synthesis_prompt = f"""Synthesize the following research results into a coherent and comprehensive summary:
    {full_research}

    Provide a well-structured summary that covers all important aspects and highlights the most relevant information for the user's query: "{user_input}".
    """

    try:
        return process_prompt(synthesis_prompt, model_name, "ResearchSynthesizer")
    except Exception as e:
        logger.error(f"Error in conduct_comprehensive_research: {e}")
        return "Unable to synthesize research results due to an error."
