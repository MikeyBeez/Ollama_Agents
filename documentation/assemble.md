# 🧩 Assemble Module

## Overview

The Assemble Module (`assemble.py`) manages the chat history and context assembly for the AI assistant.

## Key Features

1. **Chat History Management**: Stores and retrieves conversation history.
2. **Context Assembly**: Combines chat history with current prompts for context-aware responses.
3. **Persistence**: Saves and loads chat history to/from disk.

## Main Class

### `ChatHistory`

This class manages the chat history with methods to:
- Add new entries
- Retrieve the full history
- Assemble prompts with historical context
- Truncate history
- Save and load history from disk

## Key Functions

- `add_to_chat_history(prompt: str, response: str)`
- `assemble_prompt_with_history(current_prompt: str) -> str`
- `get_chat_history() -> List[Tuple[str, str]]`
- `truncate_chat_history(n: int)`
- `save_chat_history()`
- `load_chat_history()`

## Why a Separate Module?

The assemble module is separated to:
1. Centralize all history and context management.
2. Provide a clean interface for other modules to interact with chat history.
3. Allow for easy modification of how context is assembled and managed.

## What Makes It Special?

- Implements a singleton pattern for global access to chat history.
- Provides methods for easy manipulation of chat history.
- Ensures persistence of conversations across sessions.

This module is crucial for maintaining context in conversations, allowing the AI to provide more coherent and contextually relevant responses.
