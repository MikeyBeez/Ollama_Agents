# src/main.py
import sys
import os
from modules.input import get_user_input

# Add the project root to the Python path


def main():
    print("Type /h or /help for available commands.")
    while True:
        user_input = get_user_input()
        if user_input is None:
            print("Exiting program.")
            break
        elif user_input == 'CONTINUE':
            continue
        print(f"You entered: {user_input}")


if __name__ == "__main__":
    main()
