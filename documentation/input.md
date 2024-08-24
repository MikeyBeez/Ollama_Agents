# Documentation for input.py Module

## Overview

The `input.py` module provides an enhanced user input interface for command-line applications. It leverages the `prompt_toolkit` library to offer a rich, interactive prompt with features like command history, auto-suggestion, and command completion.

## Key Features

1. Customized prompt with the user's name
2. Command history persistence
3. Auto-suggestions based on command history
4. Tab completion for predefined commands
5. Vi editing mode
6. Custom key bindings (Ctrl-C and Ctrl-D for exit)
7. Styled prompt for better visibility

## Functions

### `get_help()`

Returns a string containing help information about available commands.

### `get_user_input()`

The main function that sets up and manages the interactive prompt. It returns:
- The user's input as a string
- `None` if the user chooses to exit
- `'CONTINUE'` if the user requests help

## Implementation Details

### Setup

1. The module uses a relative import to access the `USER_NAME` from a `config.py` file.
2. It imports various components from the `prompt_toolkit` library.

### Prompt Configuration

1. **History**: Uses `FileHistory` to persist command history across sessions.
2. **Auto-suggest**: Implements `AutoSuggestFromHistory` for suggestions based on previous commands.
3. **Completion**: Uses `WordCompleter` for tab completion of predefined commands.
4. **Key Bindings**: Custom `KeyBindings` allow exiting the program with Ctrl-C or Ctrl-D.
5. **Styling**: Applies a custom style to make the prompt green and bold.

### Command Processing

- The function checks for specific commands:
  - `/e`, `/exit`, `/q`, `/quit`: Exit the program
  - `/h`, `/help`: Display help information

### Error Handling

- Catches `KeyboardInterrupt` and `EOFError` to handle user interruptions gracefully.

## Benefits of prompt_toolkit

1. **Enhanced User Experience**: Provides a more interactive and user-friendly command-line interface.
2. **Improved Productivity**: Features like history, auto-suggest, and completion help users work more efficiently.
3. **Customizability**: Allows for easy styling and behavior modifications to suit specific needs.
4. **Cross-Platform Compatibility**: Works consistently across different operating systems.
5. **Vi Editing Mode**: Familiar keybindings for users accustomed to Vi/Vim editors.
6. **Robust Input Handling**: Manages various input scenarios and edge cases effectively.

## Usage

The module can be run standalone for testing or imported into other Python scripts to provide an enhanced input mechanism. When run directly, it enters a loop that continuously prompts for user input until an exit command is given.

## Conclusion

This module significantly improves upon the standard Python `input()` function by providing a feature-rich, user-friendly interface for command-line input. It's particularly useful for CLI applications that require frequent user interaction or command entry.
