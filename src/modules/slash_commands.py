from typing import Optional, Callable, Dict
from src.modules.assemble import get_chat_history, truncate_chat_history
from rich.console import Console
from rich.text import Text

console = Console()

def get_help() -> str:
    help_text = """
Available commands:
/h or /help - Show this help message
/e or /exit - Exit the program
/q or /quit - Exit the program
/hi - Show chat history
/tr n - Truncate chat history to last n entries
"""
    console.print(help_text, style="bold green")
    return 'CONTINUE'

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
    
    console.print(f"\nTotal entries in chat history: {len(history)}", style="bold cyan")
    
    return 'CONTINUE'

def exit_program() -> str:
    console.print("Exiting program.", style="bold red")
    return 'EXIT'

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

SLASH_COMMANDS: Dict[str, Callable[[], str]] = {
    '/h': get_help,
    '/help': get_help,
    '/e': exit_program,
    '/exit': exit_program,
    '/q': exit_program,
    '/quit': exit_program,
    '/hi': print_history,
    '/tr': truncate_history,
}

def handle_slash_command(command: str) -> str:
    cmd_function = SLASH_COMMANDS.get(command.split()[0].lower())
    if cmd_function:
        return cmd_function(command) if cmd_function == truncate_history else cmd_function()
    console.print(f"Unknown command: {command}", style="bold red")
    return 'CONTINUE'
