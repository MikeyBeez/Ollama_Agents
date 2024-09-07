# src/agents/advanced_research_agent.py

from typing import Dict, Any, List
import json
from src.modules.logging_setup import logger
from src.modules.ddg_search import DDGSearch
from src.modules.save_history import chat_history
from src.modules.input import get_user_input
from src.modules.agent_tools import analyze_user_input, generate_response, update_bullet_points, rank_bullet_points, interactive_followup
from src.modules.knowledge_management import process_query, assess_source_credibility, update_knowledge_base, extract_key_concepts, summarize_topic
from src.modules.context_management import gather_context, update_context
from src.modules.research_tools import conduct_comprehensive_research
from rich.console import Console
from rich.panel import Panel
from config import DEFAULT_MODEL, AGENT_NAME

console = Console()

class AdvancedResearchAgent:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
        self.context = ""
        self.conversation_history = []
        self.bullet_points = []
        self.ddg_search = DDGSearch()

    def run(self):
        console.print(f"[bold green]{AGENT_NAME} initialized. Type 'exit' to quit.[/bold green]")

        while True:
            user_input = get_user_input()
            if user_input.lower() == 'exit':
                break

            try:
                response = self.process_input(user_input)
                console.print(f"[bold magenta]{AGENT_NAME}:[/bold magenta] {response}")
            except Exception as e:
                logger.error(f"Error processing input: {str(e)}")
                console.print(f"[bold red]Error:[/bold red] {str(e)}")

        console.print(f"[bold red]{AGENT_NAME} shutting down. Goodbye![/bold red]")

    def process_input(self, user_input: str) -> str:
        try:
            input_analysis = analyze_user_input(user_input, self.model_name)
            query_info = process_query(user_input, self.model_name)

            self.context = gather_context(user_input, query_info['topic'], self.conversation_history, self.bullet_points, AGENT_NAME)

            research_results = conduct_comprehensive_research(user_input, query_info['topic'], self.model_name)
            self.context = update_context(self.context, research_results, self.model_name)

            response = generate_response(user_input, self.context, input_analysis, AGENT_NAME, self.model_name)

            credibility = assess_source_credibility(response, self.model_name)
            update_knowledge_base(response, query_info['topic'], self.model_name)

            new_bullets = update_bullet_points(response, self.model_name)
            self.bullet_points.extend(new_bullets)
            self.bullet_points = rank_bullet_points(self.bullet_points, self.model_name)

            key_concepts = extract_key_concepts(response, self.model_name)
            topic_summary = summarize_topic(query_info['topic'], self.context, self.model_name)

            self.conversation_history.append((user_input, response))
            chat_history.add_entry(user_input, response)

            followup = interactive_followup(self.context, self.model_name, self.process_input)
            if followup != "No follow-up question selected.":
                response += f"\n\n{followup}"

            return response
        except Exception as e:
            logger.error(f"Error in process_input: {str(e)}")
            return f"I apologize, but an error occurred while processing your input: {str(e)}"

def main():
    agent = AdvancedResearchAgent()
    agent.run()

if __name__ == "__main__":
    main()
