# src/main.py

import os
import sys
import importlib
from rich.console import Console
from rich.prompt import Prompt

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modules.banner import setup_console, print_welcome_banner, print_separator
from src.modules.logging_setup import logger
from src.modules.errors import OllamaAgentsError, ConfigurationError, InputError
from config import AGENT_NAME

console = Console()

def list_agents():
    agents_dir = os.path.join(os.path.dirname(__file__), 'agents')
    agent_files = [f[:-3] for f in os.listdir(agents_dir) if f.endswith('.py') and f != '__init__.py']
    return agent_files

def load_agent(agent_name):
    try:
        module = importlib.import_module(f'src.agents.{agent_name}')
        return getattr(module, 'main', None)
    except ImportError as e:
        logger.error(f"Failed to import agent module {agent_name}: {str(e)}")
        raise ConfigurationError(f"Agent {agent_name} could not be loaded") from e

def main():
    logger.info("Main application started")
    console.print("Ollama_Agents application starting...", style="bold green")

    try:
        setup_console()
        print_welcome_banner(console, "AI Agents")
        print_separator(console)

        agents = list_agents()
        logger.info(f"Available agents: {agents}")

        while True:
            try:
                console.print("Available agents:", style="bold cyan")
                for i, agent in enumerate(agents, 1):
                    console.print(f"{i}. {agent}", style="yellow")
                console.print("q. Quit", style="yellow")

                choice = Prompt.ask(
                    "Select an agent or 'q' to quit",
                    choices=[str(i) for i in range(1, len(agents)+1)] + ['q'],
                    default="q"
                )

                if choice.lower() == 'q':
                    logger.info("User chose to quit")
                    break

                agent_index = int(choice) - 1
                if 0 <= agent_index < len(agents):
                    agent_name = agents[agent_index]
                    logger.info(f"User selected agent: {agent_name}")

                    agent_main = load_agent(agent_name)
                    if agent_main:
                        agent_main()
                    else:
                        raise ConfigurationError(f"No main function found in {agent_name}")

                else:
                    raise InputError("Invalid agent selection.")

            except ValueError:
                logger.warning("Invalid input received")
                console.print("Invalid input. Please enter a number or 'q'.", style="bold red")
            except InputError as e:
                logger.warning(f"Input error: {str(e)}")
                console.print(f"Input error: {str(e)}", style="bold red")
            except ConfigurationError as e:
                logger.error(f"Configuration error: {str(e)}")
                console.print(f"Configuration error: {str(e)}", style="bold red")
            except OllamaAgentsError as e:
                logger.error(f"Ollama Agents error: {str(e)}")
                console.print(f"An error occurred: {str(e)}", style="bold red")
            except Exception as e:
                logger.exception(f"Unexpected error: {str(e)}")
                console.print("An unexpected error occurred. Please check the logs.", style="bold red")

    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        console.print("\nProgram interrupted by user.", style="bold yellow")
    except Exception as e:
        logger.critical(f"Critical error occurred: {str(e)}", exc_info=True)
        console.print("A critical error occurred. The application will now exit.", style="bold red")
    finally:
        console.print("[bold red]Goodbye![/bold red]")
        logger.info("Ollama_Agents application shutting down")

if __name__ == "__main__":
    main()
