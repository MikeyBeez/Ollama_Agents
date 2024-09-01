# 🧩 Assemble Module

The Assemble Module manages chat history and context assembly for the AI assistant.

## 🌟 Key Features

- 📚 Maintains chat history
- 🔗 Assembles context for AI prompts
- 🧠 Manages memory chunks

## 🔧 Main Functions

- 🔄 `assemble_prompt_with_history(current_prompt)`: Combines chat history with the current prompt
- ➕ `add_to_chat_history(prompt, response)`: Adds new interactions to the chat history

## 🚀 Usage

This module is used to provide context to the AI model, ensuring coherent and contextually relevant responses.

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
