# src/agents/research_agent.py

import sys
import os
import json
import random

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from src.modules.ddg_search import DDGSearch
from rich.console import Console
from rich.panel import Panel
from config import DEFAULT_MODEL

console = Console()
ddg_search = DDGSearch()

class ResearchAgent:
    def __init__(self, model=DEFAULT_MODEL):
        self.model = model
        self.debate_log = []
        self.contenders = ["🦄 Captain Sparkle", "🐉 Dr. Grumpy Scales"]

    def generate_search_query(self, topic, perspective):
        prompt = f"""Generate a short, focused search query to find information supporting the {perspective} side of the debate topic: '{topic}'.
        Return your response in the following JSON format:
        {{
            "query": "Your search query here"
        }}
        """
        response = process_prompt(prompt, self.model, "Search Query Generator")
        try:
            query_json = json.loads(response)
            return query_json['query']
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON from response: {response}")
            return f"Error: Could not generate a valid search query for {topic} ({perspective})"

    def perform_search(self, query):
        try:
            results = ddg_search.run_search(query)
            return results[0] if results else "No search results found."
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return f"Search failed: {str(e)}"

    def generate_response(self, topic, perspective, search_result):
        contender = self.contenders[0] if perspective == "pro" else self.contenders[1]
        prompt = f"""You are {contender} debating the topic: '{topic}'.
        Argue from the {perspective} perspective.
        Use this search result for context if available: '{search_result}'
        If no search result is available, use your general knowledge.
        Keep your response concise and add relevant emojis for emphasis."""
        response = process_prompt(prompt, self.model, f"{contender} ({perspective})")
        self.debate_log.append((contender, perspective, response))
        return response

    def judge_debate(self, topic):
        judge_prompt = f"""You are Judge Wise Owl 🦉 evaluating a debate on the topic: '{topic}'.
        Here's a summary of the debate:
        {self.format_debate_log()}

        Please provide:
        1. The winner of the debate
        2. The best points made by each side
        3. A brief explanation of your decision
        4. Rate each contender's performance on a scale of 1-10

        Keep your response concise, well-structured, and use emojis for emphasis."""

        judgement = process_prompt(judge_prompt, self.model, "Judge Wise Owl 🦉")
        return judgement

    def format_debate_log(self):
        return "\n".join([f"{contender} ({perspective}): {response}" for contender, perspective, response in self.debate_log])

    def debate(self, topic, turns):
        logger.info(f"Starting research debate on topic: {topic} for {turns} turns")
        console.print(Panel(f"🔬 Research Debate Topic: {topic}", style="bold magenta"))

        for i in range(turns):
            perspective = "pro" if i % 2 == 0 else "con"
            contender = self.contenders[0] if perspective == "pro" else self.contenders[1]

            search_query = self.generate_search_query(topic, perspective)
            console.print(Panel(f"🔎 Search Query: {search_query}", style="cyan"))

            search_result = self.perform_search(search_query)
            console.print(Panel(f"📚 Search Result: {search_result}", style="yellow"))

            response = self.generate_response(topic, perspective, search_result)
            console.print(Panel(response, title=f"Turn {i+1}: {contender} ({perspective.capitalize()})",
                                border_style="green" if perspective == "pro" else "red"))

        console.print(Panel("🏁 Debate concluded. Judge Wise Owl 🦉 will now evaluate.", style="bold yellow"))

        judgement = self.judge_debate(topic)
        console.print(Panel(judgement, title="🏆 Judge Wise Owl's Decision", border_style="bold blue"))

def run():
    agent = ResearchAgent()
    topic = console.input("Enter a debate topic: ")
    while True:
        try:
            turns = int(console.input("Enter the number of debate turns: "))
            if turns > 0:
                break
            else:
                console.print("Please enter a positive number of turns.", style="bold red")
        except ValueError:
            console.print("Please enter a valid number.", style="bold red")

    agent.debate(topic, turns)

def main():
    run()

if __name__ == "__main__":
    main()
