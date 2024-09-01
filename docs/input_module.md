# 🎛️ Input Module

The Input Module handles user input and command processing for the AI assistant.

## 🌟 Key Features

- 💬 Interactive command-line interface using `prompt_toolkit`
- 📜 Command history management
- 🏷️ Tab completion for commands
- 🎨 Customizable prompt style
- 🚫 Graceful handling of exit commands and interrupts

## 🔧 Main Functions

- 🔤 `get_user_input()`: Captures and processes user input
- ⚡ `handle_slash_command(command)`: Processes slash commands

## 🚀 Usage

This module is primarily used in the main application loop to capture user input and route it to the appropriate handler.

## 🧪 Testing

The input module is thoroughly tested in `test_input.py`, covering:

- Normal input processing
- Handling of exit commands
- Processing of help commands
- Keyboard interrupt handling
- EOF handling

To run tests specific to this module:

```bash
python -m unittest src/tests/test_input.py
```

## 🔍 Key Considerations

- Ensure that all new commands are added to the completion list
- Keep the command processing logic in sync with the slash_commands module
- Consider adding more sophisticated input validation if needed
