import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modules.banner import setup_console, print_welcome_banner, print_separator
from src.modules.input import get_user_input
from src.modules.ollama_client import process_prompt
from config import USER_NAME, DEFAULT_MODEL, AGENT_NAME

def main():
    # Set up the console
    console = setup_console()

    # Print the welcome banner
    print_welcome_banner(console, USER_NAME)

    # Print a separator
    print_separator(console)

    # Main input loop
    while True:
        user_input = get_user_input()
        if user_input is None:
            break
        elif user_input == 'CONTINUE':
            continue
        else:
            # Add a new line after user input
            #console.print()
            # Print a separator
            print_separator(console)

            # Assemble context with AGENT_NAME
            full_prompt = f"You are {AGENT_NAME}, an AI assistant. {user_input}"

            # Process the prompt with Ollama
            console.print(f"[bold blue]{AGENT_NAME}>[/bold blue] ", end="")
            response = process_prompt(full_prompt, DEFAULT_MODEL, USER_NAME)
            
            # Print the response in yellow
            console.print()  # New line after response

        # Print a separator after each interaction
        print_separator(console)

    console.print("[bold red]Goodbye![/bold red]")

if __name__ == "__main__":
    main()
