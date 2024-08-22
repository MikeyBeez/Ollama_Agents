# src/modules/input.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from config import USER_NAME
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style

def get_help():
    return """
Available commands:
/h or /help - Show this help message
/e or /exit - Exit the program
/q or /quit - Exit the program
"""

def get_user_input():
    prompt = f"{USER_NAME}> "
    history_file = os.path.expanduser("~/.input_history")

    completer_words = ['/h', '/help', '/e', '/exit', '/q', '/quit']
    completer = WordCompleter(completer_words, ignore_case=True)

    kb = KeyBindings()

    @kb.add('c-c')
    @kb.add('c-d')
    def _(event):
        " Pressing Ctrl-C or Ctrl-D will exit the user interface. "
        event.app.exit()

    # Define the style for the prompt
    style = Style.from_dict({
        'prompt': 'ansigreen bold',
    })

    session = PromptSession(
        history=FileHistory(history_file),
        auto_suggest=AutoSuggestFromHistory(),
        completer=completer,
        complete_while_typing=True,
        enable_history_search=True,
        vi_mode=True,
        key_bindings=kb,
        style=style,  # Add the style to the PromptSession
        message=[('class:prompt', prompt)]  # Use the styled prompt
    )

    try:
        user_input = session.prompt()

        if user_input.lower() in ['/e', '/exit', '/q', '/quit']:
            print("Exiting program.")
            return None
        elif user_input.lower() in ['/h', '/help']:
            print(get_help())
            return 'CONTINUE'

        return user_input

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        return None
    except EOFError:
        print("\nEOF detected. Exiting program.")
        return None

# Example usage
if __name__ == "__main__":
    print("Type /h or /help for available commands.")
    while True:
        result = get_user_input()
        if result is None:
            break
        elif result == 'CONTINUE':
            continue
        print(f"You entered: {result}")
