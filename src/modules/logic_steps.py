# src/modules/logic_steps.py

import json
from typing import List, Dict, Any
from rich.console import Console
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from src.modules.memory_search import search_memories
from src.modules.save_history import chat_history
from src.modules.ddg_search import DDGSearch
from src.modules.errors import LogicProcessingError, ModelInferenceError, DataProcessingError, InputError

console = Console()
ddg_search = DDGSearch()

def print_separator(console):
    console.print("\n" + "-" * 50 + "\n")

def announce_step(message: str):
    print_separator(console)
    console.print(f"[bold blue]{message}[/bold blue]")

class BulletPointManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BulletPointManager, cls).__new__(cls)
            cls._instance.bullet_points = []
        return cls._instance

    def add_bullet_point(self, bullet_point: str):
        if bullet_point not in self.bullet_points:
            self.bullet_points.append(bullet_point)
            self._rank_and_trim()

    def _rank_and_trim(self):
        if len(self.bullet_points) > 15:
            ranked_points = rank_bullet_points(self.bullet_points)
            self.bullet_points = ranked_points[:15]

    def get_bullet_points(self) -> List[str]:
        return self.bullet_points

bullet_manager = BulletPointManager()

def handle_error(error: Exception, step: str) -> str:
    logger.error(f"Error in {step}: {str(error)}")
    return f"An error occurred during {step}. Please try again or rephrase your query."

def process_user_input(user_input: str) -> str:
    try:
        console.print(f"[bold cyan]User Input:[/bold cyan] {user_input}")
        return user_input
    except Exception as e:
        raise InputError(f"Error processing user input: {str(e)}")

def generate_search_queries(user_input: str, model_name: str) -> List[str]:
    try:
        prompt = f"Generate two distinct search queries to find information about: {user_input}"
        response = process_prompt(prompt, model_name, "QueryGenerator")
        return response.split('\n')
    except Exception as e:
        raise ModelInferenceError(f"Error generating search queries: {str(e)}")

def query_response(query_type: str, context: str, model_name: str) -> str:
    try:
        announce_step(f"Generating {query_type.capitalize()} Query")
        query = process_prompt(f"Generate a {query_type} based on this context: {context}", model_name, "QueryGenerator")
        console.print(f"[bold cyan]{query_type.capitalize()} Query:[/bold cyan] {query}")

        announce_step(f"Processing {query_type.capitalize()} Query")
        response = process_prompt(query, model_name, "QueryResponder")
        console.print(f"[bold cyan]Response:[/bold cyan] {response}")

        if query_type == "bullet point":
            bullet_manager.add_bullet_point(response)

        return response
    except Exception as e:
        raise ModelInferenceError(f"Error in query response for {query_type}: {str(e)}")

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

def rank_bullet_points(bullet_points: List[str]) -> List[str]:
    try:
        announce_step("Ranking Bullet Points")
        ranking_prompt = "Rank the following bullet points by relevance and importance:\n" + "\n".join(bullet_points)
        ranked_points = process_prompt(ranking_prompt, model_name, "BulletPointRanker").split("\n")
        console.print("[bold cyan]Ranked Bullet Points:[/bold cyan]")
        for i, point in enumerate(ranked_points, 1):
            console.print(f"{i}. {point}")
        return ranked_points
    except Exception as e:
        raise DataProcessingError(f"Error ranking bullet points: {str(e)}")

def build_context(model_name: str) -> str:
    try:
        announce_step("Building Context")
        bullet_points = bullet_manager.get_bullet_points()
        ranked_points = rank_bullet_points(bullet_points)

        context = []
        for point in ranked_points[:5]:  # Use top 5 bullet points
            response = query_response("elaborate on bullet point", point, model_name)
            context.append(response)

        return "\n".join(context)
    except Exception as e:
        raise DataProcessingError(f"Error building context: {str(e)}")

def process_user_feedback(feedback: str, original_response: str, model_name: str) -> str:
    try:
        feedback_prompt = f"Given the original response: '{original_response}' and user feedback: '{feedback}', provide an improved response."
        return process_prompt(feedback_prompt, model_name, "FeedbackProcessor")
    except Exception as e:
        raise ModelInferenceError(f"Error processing user feedback: {str(e)}")

def assess_source_credibility(source: str, model_name: str) -> float:
    try:
        credibility_prompt = f"Assess the credibility of this source on a scale of 0 to 1: {source}"
        credibility_score = float(process_prompt(credibility_prompt, model_name, "CredibilityAssessor"))
        return credibility_score
    except Exception as e:
        raise ModelInferenceError(f"Error assessing source credibility: {str(e)}")

def classify_query_topic(query: str, model_name: str) -> str:
    try:
        classification_prompt = f"Classify the following query into a general topic area: {query}"
        return process_prompt(classification_prompt, model_name, "TopicClassifier")
    except Exception as e:
        raise ModelInferenceError(f"Error classifying query topic: {str(e)}")

def determine_research_depth(query: str, model_name: str) -> int:
    try:
        depth_prompt = f"On a scale of 1 to 5, how deep should the research go for this query: '{query}'? Respond with ONLY a single integer between 1 and 5."
        response = process_prompt(depth_prompt, model_name, "ResearchDepthDeterminer")
        depth = int(response.strip().split()[0])
        if 1 <= depth <= 5:
            return depth
        else:
            logger.warning(f"Invalid research depth: {depth}. Defaulting to 3.")
            return 3
    except Exception as e:
        logger.error(f"Error determining research depth: {str(e)}")
        return 3  # Default to medium depth if there's an error

def format_response(response: str, format_type: str, model_name: str) -> str:
    try:
        format_prompt = f"Format the following response as a {format_type}: {response}"
        return process_prompt(format_prompt, model_name, "ResponseFormatter")
    except Exception as e:
        raise ModelInferenceError(f"Error formatting response: {str(e)}")

def update_knowledge_base(new_info: str, topic: str, model_name: str) -> None:
    try:
        update_prompt = f"Incorporate this new information into the knowledge base for the topic '{topic}': {new_info}"
        process_prompt(update_prompt, model_name, "KnowledgeBaseUpdater")
    except Exception as e:
        raise DataProcessingError(f"Error updating knowledge base: {str(e)}")

def gather_context(user_input: str, topic: str, current_context: str, agent_name: str) -> str:
    try:
        memories = search_memories(user_input, top_k=3, similarity_threshold=0.7)
        memory_context = "\n".join([f"Memory: {m['content']}" for m in memories])

        search_query = f"{topic} {user_input}"
        search_results = ddg_search.run_search(search_query)
        search_context = "\n".join(search_results[:3])

        recent_history = chat_history.get_history()[-3:]
        history_context = "\n".join([f"User: {h['prompt']}\n{agent_name}: {h['response']}" for h in recent_history])

        new_context = f"{current_context}\n\nRelevant memories:\n{memory_context}\n\nWeb search results:\n{search_context}\n\nRecent conversation:\n{history_context}"
        return new_context
    except Exception as e:
        raise DataProcessingError(f"Error gathering context: {str(e)}")

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

def main_logic_flow(user_input: str, model_name: str) -> str:
    try:
        processed_input = process_user_input(user_input)
        topic = classify_query_topic(processed_input, model_name)
        research_depth = determine_research_depth(processed_input, model_name)

        context = gather_context(processed_input, topic, "", AGENT_NAME)
        research_results = conduct_comprehensive_research(processed_input, topic, model_name)
        context += f"\n\nResearch Results:\n{research_results}"

        response = evaluate(processed_input, context, model_name)

        formatted_response = format_response(response, "concise summary", model_name)
        update_knowledge_base(formatted_response, topic, model_name)

        return formatted_response
    except Exception as e:
        error_message = handle_error(e, "main logic flow")
        return error_message
