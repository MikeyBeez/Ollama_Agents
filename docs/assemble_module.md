# 🧩 Assemble Module

The Assemble Module manages chat history and context assembly for the AI assistant.

## 🌟 Key Features

- 📚 Maintains chat history
- 🔗 Assembles context for AI prompts
- 🧠 Manages memory chunks
- 🔀 Flexible prompt assembly options

## 🔧 Main Functions

- 🔄 `assemble_prompt_with_history(current_prompt: str, chat_history_only: bool = False) -> str`:
  Combines chat history (and optionally chunk history) with the current prompt.
  - `current_prompt`: The current user input or query.
  - `chat_history_only`: If True, only includes chat history in the assembled prompt. If False (default), includes both chat history and chunk history.

- ➕ `add_to_chat_history(prompt: str, response: str)`: Adds new interactions to the chat history.

- 📋 `get_chat_history_tuples() -> List[Tuple[str, str]]`: Retrieves chat history as a list of (prompt, response) tuples.

- ✂️ `truncate_chat_history(n: int)`: Truncates the chat history to the last n entries.

## 🚀 Usage

This module is used to provide context to the AI model, ensuring coherent and contextually relevant responses. The `chat_history_only` option allows for flexible prompt assembly based on specific use cases.

Example usage:
```python
from src.modules.assemble import assemble_prompt_with_history

# Assemble prompt with both chat and chunk history
full_prompt = assemble_prompt_with_history("What's the weather like today?")

# Assemble prompt with only chat history
chat_only_prompt = assemble_prompt_with_history("What's the weather like today?", chat_history_only=True)
```

## 🧪 Testing

While there's no dedicated test file for this module, its functionality is indirectly tested through the `test_save_history.py` file, which covers:

- Adding entries to chat history
- Saving and loading chat history
- Managing memory chunks

To run related tests:

```bash
python -m unittest src/tests/test_save_history.py
```

## 🔍 Key Considerations

- Optimize the history assembly process for performance with large histories
- Implement a strategy for managing very long conversations (e.g., summarization)
- Ensure proper synchronization if implementing concurrent access to chat history
- Consider the impact of including or excluding chunk history on the AI's responses
