# src/modules/slash_commands.py

from typing import Callable, Dict
from rich.console import Console
from src.modules.basic_commands import change_model_command, duck_duck_go_search
from src.modules.document_commands import upload_document, print_chunk_history
from src.modules.fabric_commands import fabric_command
from src.modules.memory_commands import print_history, truncate_history, memory_search, memory_search_long

console = Console()

def get_help(command: str = '') -> str:
    help_text = """
    Available commands:
    /h or /help - Show this help message
    /e or /exit - Exit the program
    /q or /quit - Exit the program
    /hi - Show chat history
    /ch - Show chunk history
    /tr n - Truncate chat history to last n entries
    /ms n m query - Search memories and process query (short version)
    /msl n m query - Search memories and process query (long version)
    /cm - Change the current Ollama model
    /s query - Search DuckDuckGo for the given query
    /upload - Upload and process a document
    /fabric - Run a Fabric pattern with interactive pattern selection
    """
    console.print(help_text, style="bold purple")
    return 'CONTINUE'

def exit_program(command: str = '') -> str:
    console.print("Exiting program.", style="bold red")
    return 'EXIT'

SLASH_COMMANDS: Dict[str, Callable[[str], str]] = {
    '/h': get_help,
    '/help': get_help,
    '/e': exit_program,
    '/exit': exit_program,
    '/q': exit_program,
    '/quit': exit_program,
    '/hi': print_history,
    '/ch': print_chunk_history,
    '/tr': truncate_history,
    '/ms': memory_search,
    '/msl': memory_search_long,
    '/cm': change_model_command,
    '/s': duck_duck_go_search,
    '/upload': upload_document,
    '/fabric': fabric_command,
}

def handle_slash_command(command: str) -> str:
    cmd_parts = command.split()
    cmd = cmd_parts[0].lower()
    cmd_function = SLASH_COMMANDS.get(cmd)

    if cmd_function:
        return cmd_function(command)
    else:
        console.print(f"Unknown command: {command}", style="bold red")
        return 'CONTINUE'
