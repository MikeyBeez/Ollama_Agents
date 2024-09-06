# src/modules/meta_processes.py

from functools import wraps
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import Callable, Any

console = Console()

def debug_panel(func: Callable) -> Callable:
    """
    A decorator that wraps a function with rich panels showing entry and exit.

    Args:
    func (Callable): The function to be decorated.

    Returns:
    Callable: The wrapped function.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        module_name = func.__module__

        # Entry panel
        entry_message = Text()
        entry_message.append("Entering: ", style="bold cyan")
        entry_message.append(f"{module_name}.{func_name}", style="bold green")
        console.print(Panel(entry_message, border_style="green", expand=False))

        try:
            # Call the function
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            # Error panel
            error_message = Text()
            error_message.append("Error in: ", style="bold red")
            error_message.append(f"{module_name}.{func_name}", style="bold green")
            error_message.append(f"\n{str(e)}", style="red")
            console.print(Panel(error_message, border_style="red", expand=False))
            raise
        finally:
            # Exit panel
            exit_message = Text()
            exit_message.append("Exiting: ", style="bold cyan")
            exit_message.append(f"{module_name}.{func_name}", style="bold green")
            console.print(Panel(exit_message, border_style="yellow", expand=False))

    return wrapper

def print_step(message: str) -> None:
    """
    Print a step message in a rich panel.

    Args:
    message (str): The message to be printed.
    """
    console.print(Panel(message, border_style="blue", expand=False))

def print_result(title: str, content: Any) -> None:
    """
    Print a result in a rich panel.

    Args:
    title (str): The title of the result.
    content (Any): The content to be printed.
    """
    console.print(Panel(f"{title}:\n{content}", border_style="magenta", expand=False))

def print_error(message: str) -> None:
    """
    Print an error message in a rich panel.

    Args:
    message (str): The error message to be printed.
    """
    console.print(Panel(f"Error: {message}", border_style="red", expand=False))
