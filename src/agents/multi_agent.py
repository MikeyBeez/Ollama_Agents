# src/agents/multi_agent.py

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import logging
from rich.console import Console
from src.modules.banner import setup_console, print_welcome_banner, print_separator
from src.modules.input import get_user_input
from src.modules.ollama_client import process_prompt
from src.modules.save_history import ChatHistory
from src.modules.assemble import assemble_prompt_with_history
from config import LOG_LEVEL, LOG_FILE, DEFAULT_MODEL

logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Agent:
    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.chat_history = ChatHistory()

    def process_input(self, user_input):
        current_prompt = f"You are {self.name}, an AI assistant. {user_input}"
        full_prompt = assemble_prompt_with_history(current_prompt)
        response = process_prompt(full_prompt, self.model, self.name)
        self.chat_history.add_entry(user_input, response)
        return response

def run():
    console = setup_console()
    print_welcome_banner(console, "Multi-Agent System")
    print_separator(console)

    agents = [
        Agent("Alice", DEFAULT_MODEL),
        Agent("Bob", DEFAULT_MODEL),
        Agent("Charlie", DEFAULT_MODEL)
    ]

    while True:
        console.print("Select an agent (1-3) or 'q' to quit:", style="bold cyan")
        for i, agent in enumerate(agents, 1):
            console.print(f"{i}. {agent.name}", style="yellow")

        choice = get_user_input()

        if choice is None or choice.lower() == 'q':
            break

        try:
            agent_index = int(choice) - 1
            if 0 <= agent_index < len(agents):
                current_agent = agents[agent_index]
                console.print(f"Chatting with {current_agent.name}. Type 'back' to switch agents.", style="bold green")

                while True:
                    user_input = get_user_input()
                    if user_input is None or user_input.lower() == 'back':
                        break
                    response = current_agent.process_input(user_input)
                    console.print(f"{current_agent.name}: {response}", style="bold magenta")
            else:
                console.print("Invalid agent selection.", style="bold red")
        except ValueError:
            console.print("Invalid input. Please enter a number or 'q'.", style="bold red")

    console.print("[bold red]Goodbye![/bold red]")

def main():
    run()

if __name__ == "__main__":
    main()
