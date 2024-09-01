# src/agents/one_agent.py

import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from config import USER_NAME, AGENT_NAME, DEFAULT_MODEL, LOG_LEVEL, LOG_FILE
import logging
from src.modules.banner import setup_console, print_welcome_banner, print_separator
from src.modules.input import get_user_input
from src.modules.ollama_client import process_prompt
from src.modules.save_history import chat_history
from src.modules.assemble import assemble_prompt_with_history

# Setup logging
logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run():
    console = setup_console()
    print_welcome_banner(console, USER_NAME)
    print_separator(console)

    while True:
        user_input = get_user_input()
        if user_input is None:
            break
        elif user_input == 'CONTINUE':
            continue
        else:
            print_separator(console)
            current_prompt = f"You are {AGENT_NAME}, an AI assistant. {user_input}"
            full_prompt = assemble_prompt_with_history(current_prompt)
            response = process_prompt(full_prompt, DEFAULT_MODEL, USER_NAME)
            chat_history.add_entry(user_input, response)
        print_separator(console)

    console.print("[bold red]Goodbye![/bold red]")

def main():
    run()

if __name__ == "__main__":
    main()
