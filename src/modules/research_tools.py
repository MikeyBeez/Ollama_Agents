# src/modules/research_tools.py

import json
from typing import List, Dict, Any
from src.modules.ddg_search import DDGSearch
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from src.modules.errors import ModelInferenceError, DataProcessingError

ddg_search = DDGSearch()

def conduct_research(user_input: str, topic: str, depth: int, model_name: str) -> str:
    try:
        logger.info(f"Conducting research on topic: {topic}")
        search_results = ddg_search.run_search(f"{topic} {user_input}")

        research_prompt = f"""Based on the following search results about "{topic}" related to the query "{user_input}":
        {' '.join(search_results[:5])}

        Provide a comprehensive summary of the most relevant information.
        Use a research depth of {depth} out of 5, where 5 is the most in-depth.
        Include key facts, different perspectives, and any recent developments.
        If there are conflicting views, present them objectively.
        """

        research_summary = process_prompt(research_prompt, model_name, "Researcher")
        logger.info("Research completed successfully")
        return research_summary
    except Exception as e:
        logger.error(f"Error in conduct_research: {str(e)}")
        raise DataProcessingError(f"Error conducting research: {str(e)}")

def generate_search_queries(user_input: str, model_name: str) -> List[str]:
    try:
        logger.info(f"Generating search queries for: {user_input}")
        prompt = f"""Generate three distinct search queries to find comprehensive information about: {user_input}
        Provide your response as a JSON list of strings.
        """
        response = process_prompt(prompt, model_name, "QueryGenerator")
        queries = json.loads(response)
        logger.info(f"Generated queries: {queries}")
        return queries
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from response: {response}")
        raise ModelInferenceError(f"Error generating search queries: {str(e)}")
    except Exception as e:
        logger.error(f"Error in generate_search_queries: {str(e)}")
        raise DataProcessingError(f"Error generating search queries: {str(e)}")

def basic_research(input_text: str, model_name: str) -> List[str]:
    try:
        logger.info(f"Conducting basic research on: {input_text}")
        questions_prompt = f"""Generate two research questions for the following topic: {input_text}
        Provide your response as a JSON object with keys 'question1' and 'question2'.
        """
        questions_response = process_prompt(questions_prompt, model_name, "QuestionGenerator")
        questions = json.loads(questions_response)

        bullet_points = []
        for i, question_key in enumerate(['question1', 'question2'], 1):
            question = questions[question_key]
            logger.info(f"Researching question {i}: {question}")
            search_results = ddg_search.run_search(question)
            relevance_context = f"Question: {question}\nSearch Results: {' '.join(search_results[:3])}"

            relevance_prompt = f"Is the following information relevant to answering the question? Respond with 'yes' or 'no':\n{relevance_context}"
            relevance_response = process_prompt(relevance_prompt, model_name, "RelevanceChecker")

            if relevance_response.lower() == 'yes':
                summary_prompt = f"Summarize the following information to answer the question:\n{relevance_context}"
                bullet_point = process_prompt(summary_prompt, model_name, "Summarizer")
                bullet_points.append(bullet_point.strip())

        logger.info("Basic research completed successfully")
        return bullet_points
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON: {e}")
        raise ModelInferenceError(f"Error in basic research: {str(e)}")
    except Exception as e:
        logger.error(f"Error in basic research: {e}")
        raise DataProcessingError(f"Error in basic research: {str(e)}")

def conduct_comprehensive_research(user_input: str, topic: str, model_name: str) -> str:
    try:
        logger.info(f"Conducting comprehensive research on: {topic}")
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

        final_synthesis = process_prompt(synthesis_prompt, model_name, "ResearchSynthesizer")
        logger.info("Comprehensive research completed successfully")
        return final_synthesis
    except Exception as e:
        logger.error(f"Error in comprehensive research: {str(e)}")
        raise DataProcessingError(f"Error conducting comprehensive research: {str(e)}")

def analyze_credibility(source: str, model_name: str) -> Dict[str, Any]:
    try:
        logger.info(f"Analyzing credibility of source: {source}")
        credibility_prompt = f"""Analyze the credibility of the following source:
        {source}

        Provide your analysis as a JSON object with the following keys:
        - credibility_score: A float between 0 and 1, where 1 is most credible
        - reasoning: A brief explanation for the credibility score
        - potential_biases: A list of any potential biases identified
        """

        credibility_response = process_prompt(credibility_prompt, model_name, "CredibilityAnalyzer")
        credibility_analysis = json.loads(credibility_response)
        logger.info(f"Credibility analysis completed: {credibility_analysis}")
        return credibility_analysis
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from credibility response: {credibility_response}")
        raise ModelInferenceError(f"Error analyzing credibility: {str(e)}")
    except Exception as e:
        logger.error(f"Error in analyze_credibility: {str(e)}")
        raise DataProcessingError(f"Error analyzing credibility: {str(e)}")
