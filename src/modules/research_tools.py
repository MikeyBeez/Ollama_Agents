# src/modules/research_tools.py

from typing import List
from rich.console import Console
from src.modules.logging_setup import logger
from src.modules.ollama_client import process_prompt
from src.modules.ddg_search import DDGSearch
from src.modules.errors import DataProcessingError
from src.modules.context_management import announce_step, query_response, bullet_manager

console = Console()
ddg_search = DDGSearch()

def generate_search_queries(user_input: str, model_name: str) -> List[str]:
    try:
        prompt = f"Generate two distinct search queries to find information about: {user_input}"
        response = process_prompt(prompt, model_name, "QueryGenerator")
        return response.split('\n')
    except Exception as e:
        raise ModelInferenceError(f"Error generating search queries: {str(e)}")

def basic_research(input_text: str, model_name: str) -> List[str]:
    try:
        announce_step("Starting Basic Research")

        questions = json.loads(query_response("research questions", input_text, model_name))

        bullet_points = []
        for i, question_key in enumerate(['question1', 'question2'], 1):
            announce_step(f"Processing Research Question {i}")
            console.print(f"[bold cyan]Research Question {i}:[/bold cyan] {questions[question_key]}")

            search_results = ddg_search.run_search(questions[question_key])
            console.print(f"[bold cyan]Search Results for Question {i}:[/bold cyan]")
            for result in search_results[:3]:
                console.print(result)

            relevance_context = f"Input: {input_text}\nSearch Results: {' '.join(search_results[:3])}"
            if query_response("relevance check", relevance_context, model_name).lower() == 'yes':
                bullet_point = query_response("bullet point", f"Input: {input_text}\nSearch Results: {' '.join(search_results[:3])}", model_name)
                bullet_points.append(bullet_point.strip())

        announce_step("Basic Research Completed")
        return bullet_points
    except Exception as e:
        raise DataProcessingError(f"Error in basic research: {str(e)}")

def conduct_comprehensive_research(user_input: str, topic: str, model_name: str) -> str:
    try:
        research_aspects = [
            "Latest developments and breakthroughs",
            "Expert opinions and consensus",
            "Potential applications and use cases",
            "Challenges and limitations",
            "Future prospects and predictions"
        ]

        comprehensive_results = []

        for aspect in research_aspects:
            console.print(f"[bold cyan]Researching: {aspect}[/bold cyan]")
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
        return final_synthesis
    except Exception as e:
        raise DataProcessingError(f"Error in comprehensive research: {str(e)}")
