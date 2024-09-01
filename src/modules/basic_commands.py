import subprocess
from rich.console import Console
from rich.prompt import IntPrompt
import os

console = Console()

def get_ollama_models():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            models = [line.split()[0] for line in result.stdout.strip().split('\n')[1:]]
            return models
        else:
            console.print("Error fetching Ollama models", style="bold red")
            return []
    except Exception as e:
        console.print(f"Error: {str(e)}", style="bold red")
        return []

def change_model_command(command: str) -> str:
    models = get_ollama_models()
    if not models:
        console.print("No models available", style="bold red")
        return 'CONTINUE'

    console.print("Available models:", style="bold blue")
    for i, model in enumerate(models, 1):
        console.print(f"{i}. {model}")

    choice = IntPrompt.ask("Enter the number of the model you want to use", default=1)
    if 1 <= choice <= len(models):
        new_model = models[choice - 1]
        update_config_model(new_model)
        console.print(f"Model changed to: {new_model}", style="bold green")
    else:
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

def duck_duck_go_search(command: str) -> str:
    # Existing duck_duck_go_search function...
    pass
