# src/agents/simple_agent.py

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.logging_setup import logger
from src.modules.errors import InputError, APIConnectionError
from src.modules.ollama_client import process_prompt
from src.modules.input import get_user_input
from src.modules.slash_commands import handle_slash_command
from rich.console import Console
from config import DEFAULT_MODEL, AGENT_NAME

console = Console()

def run_simple_agent():
    logger.info(f"Starting {AGENT_NAME} simple agent")
    console.print(f"[bold green]Hello! I'm {AGENT_NAME}, your simple AI assistant. I'll give short answers.[/bold green]")

    try:
        while True:
            try:
                user_input = get_user_input()
                if user_input is None:
                    break
                if user_input == 'CONTINUE':
                    continue

                if user_input.startswith('/'):
                    result = handle_slash_command(user_input)
                    if result == 'EXIT':
                        break
                    elif result != 'CONTINUE':
                        console.print(result)
                    continue

                logger.info(f"User input: {user_input}")

                prompt = f"You are a simple AI assistant named {AGENT_NAME}. Give a short and concise answer to: {user_input}"
                response = process_prompt(prompt, DEFAULT_MODEL, "SimpleAgent")

                console.print(f"[bold magenta]{AGENT_NAME}: [/bold magenta]{response}")
                logger.info(f"Agent response: {response}")

            except InputError as e:
                logger.warning(f"Input error: {str(e)}")
                console.print(f"Input error: {str(e)}", style="bold red")
            except APIConnectionError as e:
                logger.error(f"API error: {str(e)}")
                console.print(f"API error: {str(e)}", style="bold red")

    except KeyboardInterrupt:
        logger.info("Agent interaction interrupted by user")
    except Exception as e:
        logger.exception(f"Unexpected error in {AGENT_NAME} agent: {str(e)}")
        console.print("An unexpected error occurred. Please check the logs.", style="bold red")
    finally:
        logger.info(f"{AGENT_NAME} agent shutting down")
        console.print(f"[bold green]Goodbye! {AGENT_NAME} signing off.[/bold green]")

def main():
    run_simple_agent()

if __name__ == "__main__":
    main()
