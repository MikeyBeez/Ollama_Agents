from typing import Callable, Dict
from rich.console import Console
from src.modules.command_functions import print_history, truncate_history, memory_search, change_model_command, duck_duck_go_search
from src.modules.command_functions_2 import upload_document, print_chunk_history

console = Console()

def get_help() -> str:
    help_text = """
Available commands:
/h or /help - Show this help message
/e or /exit - Exit the program
/q or /quit - Exit the program
/hi - Show chat history
/ch - Show chunk history
/tr n - Truncate chat history to last n entries
/ms n m query - Search memories and process query
  n: Number of top results (default: 3)
  m: Minimum similarity percentage (default: 60)
  query: Your question or prompt
  Example: /ms 5 70 Who was Bach?
/cm - Change the current Ollama model
/s query - Search DuckDuckGo for the given query
/upload - Upload and process a document
"""
    console.print(help_text, style="bold purple")
    return 'CONTINUE'

def exit_program() -> str:
    console.print("Exiting program.", style="bold red")
    return 'EXIT'

SLASH_COMMANDS: Dict[str, Callable[[], str]] = {
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
    '/cm': change_model_command,
    '/s': duck_duck_go_search,
    '/upload': upload_document,
}

def handle_slash_command(command: str) -> str:
    cmd_parts = command.split()
    cmd = cmd_parts[0].lower()
    cmd_function = SLASH_COMMANDS.get(cmd)

    if cmd_function:
        if cmd in ['/tr', '/ms', '/cm', '/s', '/upload']:
            return cmd_function(command)
        else:
            return cmd_function()
    else:
        console.print(f"Unknown command: {command}", style="bold red")
        return 'CONTINUE'
