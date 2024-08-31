# src/modules/assemble.py

import json
from typing import List, Tuple
from pathlib import Path
from config import MEMORY_LENGTH
from src.modules.chunk_history import assemble_chunks
from src.modules.save_history import get_chat_history

def assemble_prompt_with_history(current_prompt: str) -> str:
    chat_history = get_chat_history()
    history_prompts = [f"User: {entry['prompt']}\nAssistant: {entry['response']}" for entry in chat_history]
    history_prompts_str = "\n\n".join(history_prompts)
    chunk_history_str = assemble_chunks()
    assembled_prompt = f"{history_prompts_str}\n\nChunk History:\n{chunk_history_str}\n\nUser: {current_prompt}\nAssistant:"
    return assembled_prompt

def get_chat_history_tuples() -> List[Tuple[str, str]]:
    chat_history = get_chat_history()
    return [(entry['prompt'], entry['response']) for entry in chat_history]

def truncate_chat_history(n: int):
    from src.modules.save_history import chat_history
    chat_history.history = chat_history.history[-n:] if n > 0 else []
    chat_history.save_history()

# The following functions are kept for backwards compatibility
# and to ensure we don't remove any functionality

def add_to_chat_history(prompt: str, response: str):
    from src.modules.save_history import save_interaction
    save_interaction(prompt, response, "User", "DefaultModel")

def save_chat_history():
    from src.modules.save_history import chat_history
    chat_history.save_history()

def load_chat_history():
    from src.modules.save_history import chat_history
    chat_history.load_history()
