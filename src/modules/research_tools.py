# src/modules/research_tools.py

import json
from typing import List, Dict, Any
from src.modules.ddg_search import DDGSearch
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from src.modules.errors import ModelInferenceError, DataProcessingError

ddg_search = DDGSearch()

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
        return json.loads(response)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from response: {e}")
        return [user_input]  # Fallback to the original input
    except Exception as e:
        logger.error(f"Error in generate_search_queries: {e}")
        return [user_input]  # Fallback to the original input

def conduct_search(query: str) -> List[str]:
    """
    Conduct a web search using the provided query.

    Args:
    query (str): The search query.

    Returns:
    List[str]: A list of search results.
    """
    logger.info(f"Conducting search for query: {query[:50]}...")
    try:
        return ddg_search.run_search(query)
    except Exception as e:
        logger.error(f"Error in conduct_search: {e}")
        return []

def summarize_search_results(results: List[str], model_name: str) -> str:
    """
    Summarize a list of search results.

    Args:
    results (List[str]): The list of search results to summarize.
    model_name (str): The name of the model to use for summarization.

    Returns:
    str: A summary of the search results.
    """
    logger.info("Summarizing search results")
    summary_prompt = f"""Summarize the following search results into a coherent paragraph:
    {' '.join(results[:5])}
    """
    try:
        return process_prompt(summary_prompt, model_name, "ResultSummarizer")
    except Exception as e:
        logger.error(f"Error in summarize_search_results: {e}")
        return "Unable to summarize search results due to an error."

def conduct_research(user_input: str, topic: str, depth: int, model_name: str) -> str:
    """
    Conduct research on a given topic based on user input and specified depth.

    Args:
    user_input (str): The user's original query.
    topic (str): The main topic of research.
    depth (int): The depth of research (1-5).
    model_name (str): The name of the model to use for research.

    Returns:
    str: A comprehensive research summary.
    """
    logger.info(f"Conducting research on topic: {topic}, depth: {depth}")
    search_results = conduct_search(f"{topic} {user_input}")
    research_prompt = f"""Based on the following search results about "{topic}" related to the query "{user_input}":
    {' '.join(search_results[:5])}

    Provide a comprehensive summary of the most relevant information.
    Use a research depth of {depth} out of 5, where 5 is the most in-depth.
    Include key facts, different perspectives, and any recent developments.
    If there are conflicting views, present them objectively.
    """
    try:
        return process_prompt(research_prompt, model_name, "Researcher")
    except Exception as e:
        logger.error(f"Error in conduct_research: {e}")
        return "Unable to conduct research due to an error."

def analyze_research_gaps(research_summary: str, model_name: str) -> List[str]:
    """
    Analyze the research summary to identify gaps or areas needing further investigation.

    Args:
    research_summary (str): The summary of conducted research.
    model_name (str): The name of the model to use for analysis.

    Returns:
    List[str]: A list of identified research gaps or areas for further investigation.
    """
    logger.info("Analyzing research gaps")
    gap_prompt = f"""Based on the following research summary, identify any gaps or areas that need further investigation:
    {research_summary}

    List the gaps or areas as bullet points.
    """
    try:
        gaps = process_prompt(gap_prompt, model_name, "GapAnalyzer")
        return [gap.strip() for gap in gaps.split('\n') if gap.strip()]
    except Exception as e:
        logger.error(f"Error in analyze_research_gaps: {e}")
        return []

def verify_information(claim: str, model_name: str) -> Dict[str, Any]:
    """
    Attempt to verify a given claim using available information.

    Args:
    claim (str): The claim to verify.
    model_name (str): The name of the model to use for verification.

    Returns:
    Dict[str, Any]: A dictionary containing verification results.
    """
    logger.info(f"Verifying claim: {claim[:50]}...")
    verify_prompt = f"""Verify the following claim and provide your assessment:
    "{claim}"

    Respond in the following JSON format:
    {{
        "verified": true/false,
        "confidence": 0.85,
        "explanation": "Explanation of the verification result",
        "sources": ["Source 1", "Source 2"]
    }}
    """
    try:
        response = process_prompt(verify_prompt, model_name, "ClaimVerifier")
        return json.loads(response)
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON in verify_information: {e}")
        return {"verified": False, "confidence": 0, "explanation": "Error in verification process", "sources": []}
    except Exception as e:
        logger.error(f"Error in verify_information: {e}")
        return {"verified": False, "confidence": 0, "explanation": "Error in verification process", "sources": []}

def perform_research(user_input: str, topic: str, model_name: str) -> str:
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
        search_results = conduct_search(search_query)

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
        logger.error(f"Error in perform_research: {e}")
        return "Unable to synthesize research results due to an error."

def conduct_basic_research(input_text: str, model_name: str) -> List[str]:
    """
    Conduct basic research on a given input text.

    Args:
    input_text (str): The text to research.
    model_name (str): The name of the model to use for research.

    Returns:
    List[str]: A list of research findings.
    """
    logger.info(f"Conducting basic research on: {input_text[:50]}...")
    search_results = conduct_search(input_text)
    research_prompt = f"""Based on the following search results about "{input_text}":
    {' '.join(search_results[:5])}

    Provide a list of 3-5 key findings or pieces of information.
    Format each finding as a separate item in a Python list.
    """
    try:
        findings = process_prompt(research_prompt, model_name, "BasicResearcher")
        return eval(findings)  # This should return a list of strings
    except Exception as e:
        logger.error(f"Error in conduct_basic_research: {e}")
        return ["Unable to conduct basic research due to an error."]
