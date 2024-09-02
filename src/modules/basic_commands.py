# src/modules/basic_commands.py

import subprocess
from rich.console import Console
from rich.prompt import IntPrompt
import os
from src.modules.logging_setup import logger
from src.modules.ddg_search import DDGSearch
from src.modules.errors import APIConnectionError

console = Console()
ddg_search = DDGSearch()

def get_ollama_models():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            models = [line.split()[0] for line in result.stdout.strip().split('\n')[1:]]
            logger.info(f"Retrieved {len(models)} Ollama models")
            return models
        else:
            logger.error(f"Error fetching Ollama models: {result.stderr}")
            console.print("Error fetching Ollama models", style="bold red")
            return []
    except Exception as e:
        logger.exception(f"Exception while fetching Ollama models: {str(e)}")
        console.print(f"Error: {str(e)}", style="bold red")
        return []

def change_model_command(command: str) -> str:
    models = get_ollama_models()
    if not models:
        logger.warning("No models available for selection")
        console.print("No models available", style="bold red")
        return 'CONTINUE'

    logger.info(f"Displaying {len(models)} available models for selection")
    console.print("Available models:", style="bold blue")
    for i, model in enumerate(models, 1):
        console.print(f"{i}. {model}")

    choice = IntPrompt.ask("Enter the number of the model you want to use", default=1)
    if 1 <= choice <= len(models):
        new_model = models[choice - 1]
        update_config_model(new_model)
        logger.info(f"Model changed to: {new_model}")
        console.print(f"Model changed to: {new_model}", style="bold green")
    else:
        logger.warning(f"Invalid model choice: {choice}")
        console.print("Invalid choice. Model unchanged.", style="bold yellow")

    return 'CONTINUE'

def update_config_model(new_model: str):
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.py')
    with open(config_path, 'r') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.startswith('DEFAULT_MODEL ='):
            lines[i] = f'DEFAULT_MODEL = "{new_model}"\n'
            break

    with open(config_path, 'w') as file:
        file.writelines(lines)

    logger.info(f"Updated config.py with new model: {new_model}")

def duck_duck_go_search(command: str) -> str:
    query = command.split(maxsplit=1)[1] if len(command.split()) > 1 else ""
    if not query:
        logger.warning("Empty search query received")
        console.print("Please provide a search query.", style="bold yellow")
        return 'CONTINUE'

    try:
        logger.info(f"Performing DuckDuckGo search for query: '{query[:50]}...'")
        results = ddg_search.run_search(query)
        if results:
            console.print("Search Results:", style="bold green")
            for i, result in enumerate(results[:5], 1):  # Display top 5 results
                console.print(f"{i}. {result}", style="cyan")
            logger.info(f"Displayed {len(results[:5])} search results")
        else:
            console.print("No results found.", style="bold yellow")
            logger.info("No search results found")
    except APIConnectionError as e:
        logger.error(f"API Connection error during search: {str(e)}")
        console.print(f"Error connecting to DuckDuckGo: {str(e)}", style="bold red")
    except Exception as e:
        logger.exception(f"Unexpected error during search: {str(e)}")
        console.print(f"An unexpected error occurred: {str(e)}", style="bold red")

    return 'CONTINUE'
