from rich.console import Console
from rich.panel import Panel
from rich.align import Align
import logging


def setup_console():
    logging.debug("Setting up console")
    return Console()


def print_welcome_banner(console, username):
    logging.debug(f"Printing welcome banner for user: {username}")
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


def print_separator(console):
    console.print("\n", end="")  # Start a new line
    f1 = "[bold dark_blue]~[/]"
    f2 = "[bold yellow]*[/]"
    separator = (f1 + f2) * 76
    console.print(separator + "\n")  # End with another new line

