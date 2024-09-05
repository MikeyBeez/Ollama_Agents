# src/modules/context_management.py

from typing import List, Dict, Any, Sequence
from rich.console import Console
from src.modules.logging_setup import logger
from src.modules.memory_search import search_memories
from src.modules.save_history import chat_history
from src.modules.ddg_search import DDGSearch
from src.modules.errors import DataProcessingError, ModelInferenceError
from src.modules.ollama_client import process_prompt
from config import DEFAULT_MODEL

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

def build_context(model_name: str = DEFAULT_MODEL) -> str:
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

def rank_bullet_points(bullet_points: List[str], model_name: str = DEFAULT_MODEL) -> Sequence[str]:
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

def query_response(query_type: str, context: str, model_name: str = DEFAULT_MODEL) -> str:
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
