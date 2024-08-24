import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.modules.banner import setup_console, print_welcome_banner, print_separator
from src.modules.input import get_user_input
from src.modules.ollama_client import process_prompt
from src.modules.assemble import add_to_chat_history, assemble_prompt_with_history, save_chat_history, load_chat_history
from config import USER_NAME, DEFAULT_MODEL, AGENT_NAME

def main():
    # Set up the console
    console = setup_console()

    # Print the welcome banner
    print_welcome_banner(console, USER_NAME)

    # Load chat history
    load_chat_history()

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
            # Print a separator
            print_separator(console)

            # Assemble context with AGENT_NAME and chat history
            current_prompt = f"You are {AGENT_NAME}, an AI assistant. {user_input}"
            full_prompt = assemble_prompt_with_history(current_prompt)

            # Process the prompt with Ollama
            console.print(f"[bold blue]{AGENT_NAME}>[/bold blue] ", end="")
            console.print()
            response = process_prompt(full_prompt, DEFAULT_MODEL, USER_NAME)
 
            # Add the current prompt and response to the chat history
            add_to_chat_history(user_input, response)

            # Print the response in yellow
            console.print()  # New line after response

        # Print a separator after each interaction
        print_separator(console)

    # Save chat history before exiting
    save_chat_history()
    console.print("[bold red]Goodbye![/bold red]")

if __name__ == "__main__":
    main()
