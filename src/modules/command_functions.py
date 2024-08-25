import os
import requests
import logging
from rich.console import Console
from rich.text import Text
from src.modules.assemble import get_chat_history, truncate_chat_history, add_to_chat_history, assemble_prompt_with_history
from src.modules.memory_search import search_memories
from src.modules.ollama_client import process_prompt, OllamaClient
from src.modules.ddg_search import DDGSearch
from config import AGENT_NAME, DEFAULT_MODEL, USER_NAME
import config

console = Console()
logger = logging.getLogger(__name__)
ddg_search = DDGSearch()

def print_history() -> str:
    history = get_chat_history()
    if not history:
        console.print("No chat history available.", style="bold green")
        return 'CONTINUE'

    history_text = Text()
    for i, (prompt, response) in enumerate(history):
        history_text.append(f"\n--- Entry {i+1} ---\n", style="bold green")
        history_text.append(f"User: {prompt}\n", style="bold green")
        history_text.append(f"Assistant: {response}\n", style="bold green")

    console.print("Chat History:", style="bold green")
    console.print(history_text)
    
    console.print(f"\nTotal entries in chat history: {len(history)}", style="bold purple")
    
    return 'CONTINUE'

def truncate_history(command: str) -> str:
    try:
        n = int(command.split()[1])
        if n < 0:
            raise ValueError("Number of entries must be non-negative")
        truncate_chat_history(n)
        console.print(f"Chat history truncated to last {n} entries.", style="bold green")
    except IndexError:
        console.print("Error: Please provide the number of entries to keep. Usage: /tr n", style="bold red")
    except ValueError as e:
        console.print(f"Error: {str(e)}. Please provide a valid non-negative integer.", style="bold red")
    return 'CONTINUE'

def memory_search(command: str) -> str:
    try:
        parts = command.split(maxsplit=3)
        n = 3  # default number of results
        m = 0.6  # default similarity threshold (60%)
        
        if len(parts) < 4:
            raise ValueError("Insufficient arguments")
        
        n = int(parts[1])
        m = float(parts[2])
        query = parts[3]
        
        if n <= 0 or m < 0 or m > 1:
            raise ValueError("Invalid parameters")
        
        console.print(f"Searching for top {n} memories with similarity above {m*100}%", style="bold yellow")
        memories = search_memories(query, top_k=n, similarity_threshold=m)
        
        if not memories:
            console.print("No relevant memories found. Proceeding with the query without additional context.", style="bold yellow")
            context = query
        else:
            console.print(f"Found {len(memories)} relevant memories:", style="bold green")
            console.print("Please be patient. Memory search takes a little while.", style="bold cyan")
            context = "Relevant past interactions:\n\n"
            for i, memory in enumerate(memories, 1):
                context += f"Memory {i} (Similarity: {memory['similarity']:.2%}):\n"
                context += f"User: {memory['prompt']}\n"
                context += f"Assistant: {memory['response']}\n\n"
            context += f"Now, please answer the following question: {query}"

        # Assemble the full prompt with the context
        full_prompt = f"You are {AGENT_NAME}, an AI assistant. {context}"
        assembled_prompt = assemble_prompt_with_history(full_prompt)

        # Process the prompt with Ollama
        console.print(f"[bold blue]{AGENT_NAME}>[/bold blue] ", end="")
        console.print()
        response = process_prompt(assembled_prompt, DEFAULT_MODEL, USER_NAME)

        # Add the interaction to chat history
        add_to_chat_history(query, response)

        console.print("\nMemory search and response added to chat history.", style="bold green")
        
    except ValueError as e:
        console.print(f"Error: {str(e)}. Usage: /ms n m query (where n is the number of memories, m is the similarity threshold between 0 and 1, and query is your question)", style="bold red")
    except Exception as e:
        console.print(f"An error occurred: {str(e)}", style="bold red")
    
    return 'CONTINUE'

def get_ollama_models():
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = response.json().get('models', [])
            return [model['name'] for model in models]
        else:
            logger.error(f"Failed to fetch Ollama models. Status code: {response.status_code}")
            return []
    except requests.RequestException as e:
        logger.error(f"Error fetching Ollama models: {e}")
        return []

def update_config_model(new_model):
    config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.py')
    with open(config_path, 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        if line.startswith('DEFAULT_MODEL'):
            lines[i] = f'DEFAULT_MODEL = "{new_model}"\n'
            break
    with open(config_path, 'w') as file:
        file.writelines(lines)
    # Update the runtime configuration
    config.DEFAULT_MODEL = new_model

def change_model_command(command: str) -> str:
    models = get_ollama_models()
    if not models:
        console.print("No Ollama models found or unable to fetch models.", style="bold red")
        return 'CONTINUE'
    console.print("Available Ollama models:", style="bold blue")
    for i, model in enumerate(models, 1):
        console.print(f"[{i}] {model}", style="cyan")
    while True:
        choice = console.input("Enter the number of the model you want to use (or 'q' to quit): ")
        if choice.lower() == 'q':
            return 'CONTINUE'
        try:
            choice = int(choice)
            if 1 <= choice <= len(models):
                new_model = models[choice - 1]
                update_config_model(new_model)
                # Note: We don't reinitialize OllamaClient here as it's handled differently in this structure
                console.print(f"Model changed to: {new_model}", style="bold green")
                return 'CONTINUE'
            else:
                console.print("Invalid number. Please try again.", style="bold red")
        except ValueError:
            console.print("Invalid input. Please enter a number or 'q'.", style="bold red")

def duck_duck_go_search(command: str) -> str:
    try:
        query = command.split(maxsplit=1)[1]
        console.print(f"Searching DuckDuckGo for: {query}", style="bold yellow")
        results = ddg_search.run_search(query)
        
        if not results:
            console.print("No results found.", style="bold red")
            return 'CONTINUE'
        
        result_text = "\n".join(results)
        console.print("Search Results:", style="bold green")
        console.print(result_text, style="cyan")
        
        # Add the search query and results to chat history
        add_to_chat_history(f"DuckDuckGo Search: {query}", result_text)
        console.print("\nSearch results added to chat history.", style="bold green")
        
    except IndexError:
        console.print("Error: Please provide a search query. Usage: /s your search query", style="bold red")
    except Exception as e:
        console.print(f"An error occurred: {str(e)}", style="bold red")
    
    return 'CONTINUE'
