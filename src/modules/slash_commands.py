# src/modules/slash_commands.py

from typing import Callable, Dict
from rich.console import Console
from rich.panel import Panel
from src.modules.basic_commands import change_model_command, duck_duck_go_search
from src.modules.document_commands import upload_document, print_chunk_history
from src.modules.fabric_commands import fabric_command
from src.modules.memory_commands import print_history, truncate_history, memory_search, memory_search_long
from src.modules.logging_setup import logger
from src.modules.ollama_client import process_prompt
from src.modules.errors import CommandExecutionError
from config import TERMINAL_APP, DEFAULT_BROWSER, DEFAULT_MODEL
import webbrowser
import pyautogui
import subprocess
import datetime
import wikipedia
from difflib import get_close_matches

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
    /assistant <command> - Execute various assistant commands (e.g., open websites, look up information)
    /as <command> - Execute various assistant commands (e.g., open websites, look up information)
    """
    console.print(help_text, style="bold purple")
    logger.info("Help command executed")
    return 'CONTINUE'

def exit_program(command: str = '') -> str:
    console.print("Exiting program.", style="bold red")
    logger.info("Exit command received")
    return 'EXIT'

def assistant_command(command: str) -> str:
    logger.info(f"Executing assistant command: {command}")
    command = command.lower().replace('/assistant', '').replace('/as', '').strip()

    try:
        if 'open reddit' in command:
            url = 'https://www.reddit.com/'
            webbrowser.get(DEFAULT_BROWSER).open(url)
            console.print("Opening Reddit", style="bold green")
        elif 'open youtube' in command:
            url = 'https://www.youtube.com/'
            webbrowser.get(DEFAULT_BROWSER).open(url)
            console.print("Opening YouTube", style="bold green")
        elif 'time' in command:
            now = datetime.datetime.now()
            time_answer = f'The time is {now.strftime("%I:%M %p")}'
            console.print(Panel(time_answer, title="Current Time", border_style="bold blue"))
        elif 'look up' in command or 'lookup' in command:
            query = command.replace('look up', '').replace('lookup', '').strip()
            try:
                result = wikipedia.summary(query, sentences=2)
                console.print(Panel(result, title=f"Wikipedia: {query}", border_style="bold green"))
            except wikipedia.exceptions.DisambiguationError as e:
                console.print(f"Multiple results found. Please be more specific. Options: {e.options[:5]}", style="bold yellow")
            except wikipedia.exceptions.PageError:
                console.print(f"No results found for '{query}'", style="bold red")
        elif 'wikipedia' in command:
            query = command.replace('wikipedia', '').strip()
            try:
                result = wikipedia.summary(query, sentences=2)
                console.print(Panel(result, title=f"Wikipedia: {query}", border_style="bold green"))
                page = wikipedia.page(query)
                url = page.url
                webbrowser.open(url)
                console.print(f"Opened Wikipedia page: {url}", style="bold blue")
            except wikipedia.exceptions.DisambiguationError as e:
                console.print(f"Multiple results found. Please be more specific. Options: {e.options[:5]}", style="bold yellow")
            except wikipedia.exceptions.PageError:
                console.print(f"No results found for '{query}'", style="bold red")
            except Exception as e:
                console.print(f"An error occurred: {str(e)}", style="bold red")
        elif 'maximize' in command:
            pyautogui.hotkey('winleft', 'up')
            console.print("Window maximized", style="bold green")
        elif 'minimize' in command:
            pyautogui.hotkey('winleft', 'down')
            console.print("Window minimized", style="bold green")
        elif 'terminal' in command:
            subprocess.Popen(TERMINAL_APP)
            console.print(f"Opening terminal", style="bold green")
        else:
            response = process_prompt(f"Assistant command: {command}", DEFAULT_MODEL, "User")
            console.print(Panel(response, title="AI Assistant", border_style="bold magenta"))
    except Exception as e:
        logger.error(f"Error in assistant command: {str(e)}", exc_info=True)
        raise CommandExecutionError(f"Failed to execute assistant command: {str(e)}")

    return 'CONTINUE'

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
    '/assistant': assistant_command,
    '/as': assistant_command,
}

def handle_slash_command(command: str) -> str:
    cmd_parts = command.split()
    cmd = cmd_parts[0].lower()
    cmd_function = SLASH_COMMANDS.get(cmd)

    if cmd_function:
        logger.info(f"Executing command: {cmd}")
        try:
            return cmd_function(command)
        except CommandExecutionError as e:
            logger.error(f"Command execution error: {str(e)}")
            console.print(f"Error executing command: {str(e)}", style="bold red")
            return 'CONTINUE'
        except Exception as e:
            logger.exception(f"Unexpected error in command execution: {str(e)}")
            console.print("An unexpected error occurred. Please check the logs.", style="bold red")
            return 'CONTINUE'
    else:
        close_matches = get_close_matches(cmd, SLASH_COMMANDS.keys(), n=1, cutoff=0.6)
        if close_matches:
            logger.warning(f"Unknown command received: {command}. Did you mean {close_matches[0]}?")
            console.print(f"Unknown command: {command}. Did you mean {close_matches[0]}?", style="bold yellow")
        else:
            logger.warning(f"Unknown command received: {command}")
            console.print(f"Unknown command: {command}", style="bold red")
        return 'CONTINUE'
