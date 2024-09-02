# src/modules/banner.py

from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from src.modules.logging_setup import logger

def setup_console():
    logger.info("Setting up console")
    console = Console()
    logger.debug("Console setup complete")
    return console

def print_welcome_banner(console, username):
    logger.info(f"Printing welcome banner for user: {username}")
    print("                      ***")
    print("                      ***")
    print("                      ***")
    print("                      ***")
    print("                      ***")
    print("                      ***")
    print("                      ***")
    banner = f"""
    [bold yellow] ██████  ████████ ████████  ██████ [/bold yellow]
    [bold red]██    ██    ██       ██    ██    ██[/bold red]
    [bold green]██    ██    ██       ██    ██    ██[/bold green]
    [bold blue]██    ██    ██       ██    ██    ██[/bold blue]
    [bold magenta]██    ██    ██       ██    ██    ██[/bold magenta]
    [bold cyan] ██████     ██       ██     ██████ [/bold cyan]

    [bold white]Your Personal AI :) [/bold white]

    [bold green]Welcome, {username}![/bold green]

    [bold red]Enter /help to get help. [/bold red]
    """
    console.print(Panel(Align.center(banner), border_style="bold white", expand=False))
    logger.debug("Welcome banner printed")

def print_separator(console):
    logger.info("Printing separator")
    console.print("\n", end="")  # Start a new line
    f1 = "[bold dark_blue]~[/]"
    f2 = "[bold yellow]*[/]"
    separator = (f1 + f2) * 76
    console.print(separator + "\n")  # End with another new line
    logger.debug("Separator printed")

def print_custom_banner(console, text, style="bold green"):
    logger.info(f"Printing custom banner: '{text[:50]}...'")  # Log only first 50 characters
    console.print(Panel(Align.center(text), border_style=style, expand=False))
    logger.debug("Custom banner printed")

def print_error_message(console, message):
    logger.info(f"Printing error message: '{message[:50]}...'")  # Log only first 50 characters
    console.print(Panel(Align.center(message), border_style="bold red", expand=False))
    logger.debug("Error message printed")

def print_success_message(console, message):
    logger.info(f"Printing success message: '{message[:50]}...'")  # Log only first 50 characters
    console.print(Panel(Align.center(message), border_style="bold green", expand=False))
    logger.debug("Success message printed")
