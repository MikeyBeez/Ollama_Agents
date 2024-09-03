# src/agents/debate_agent.py

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from rich.console import Console
from rich.panel import Panel
from config import DEFAULT_MODEL

console = Console()

class DebateAgent:
    def __init__(self, model=DEFAULT_MODEL):
        self.model = model
        self.debate_log = []

    def generate_response(self, prompt, perspective):
        full_prompt = f"You are debating the topic: '{prompt}'. Argue from the {perspective} perspective. Keep your response concise."
        response = process_prompt(full_prompt, self.model, f"Debater ({perspective})")
        self.debate_log.append((perspective, response))
        return response

    def judge_debate(self, topic):
        judge_prompt = f"""You are a judge evaluating a debate on the topic: '{topic}'.
        Here's a summary of the debate:
        {self.format_debate_log()}

        Please provide:
        1. The winner of the debate
        2. The best points made by each side
        3. A brief explanation of your decision

        Keep your response concise and well-structured."""

        judgement = process_prompt(judge_prompt, self.model, "Judge")
        return judgement

    def format_debate_log(self):
        return "\n".join([f"{perspective.capitalize()}: {response}" for perspective, response in self.debate_log])

    def debate(self, topic, turns):
        logger.info(f"Starting debate on topic: {topic} for {turns} turns")
        console.print(Panel(f"Debate Topic: {topic}", style="bold magenta"))

        for i in range(turns):
            perspective = "pro" if i % 2 == 0 else "con"
            response = self.generate_response(topic, perspective)

            console.print(Panel(response, title=f"Turn {i+1}: {perspective.capitalize()} Argument",
                                border_style="green" if perspective == "pro" else "red"))

        console.print(Panel("Debate concluded. The judge will now evaluate.", style="bold yellow"))

        judgement = self.judge_debate(topic)
        console.print(Panel(judgement, title="Judge's Decision", border_style="bold blue"))

def run():
    agent = DebateAgent()
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
