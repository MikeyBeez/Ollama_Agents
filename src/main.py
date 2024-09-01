# src/main.py

import os
import importlib
from rich.console import Console
from rich.prompt import IntPrompt
from src.modules.input import get_user_input
from src.modules.banner import setup_console, print_welcome_banner, print_separator

def list_agents():
    agents_dir = os.path.join(os.path.dirname(__file__), 'agents')
    agent_files = [f[:-3] for f in os.listdir(agents_dir) if f.endswith('.py') and f != '__init__.py']
    return agent_files

def load_agent(agent_name):
    module = importlib.import_module(f'src.agents.{agent_name}')
    return getattr(module, 'main', None)

def main():
    console = Console()
    setup_console()
    print_welcome_banner(console, "AI Agents")
    print_separator(console)

    agents = list_agents()

    while True:
        console.print("Available agents:", style="bold cyan")
        for i, agent in enumerate(agents, 1):
            console.print(f"{i}. {agent}", style="yellow")
        console.print("q. Quit", style="yellow")

        choice = get_user_input()

        if choice is None or choice.lower() == 'q':
            break

        if choice == 'CONTINUE':
            continue

        try:
            agent_index = int(choice) - 1
            if 0 <= agent_index < len(agents):
                agent_name = agents[agent_index]
                agent_main = load_agent(agent_name)
                if agent_main:
                    agent_main()
                else:
                    console.print(f"Error: No main function found in {agent_name}", style="bold red")
            else:
                console.print("Invalid agent selection.", style="bold red")
        except ValueError:
            console.print("Invalid input. Please enter a number or 'q'.", style="bold red")

    console.print("[bold red]Goodbye![/bold red]")

if __name__ == "__main__":
    main()
