# src/modules/assemble.py

import json
from typing import List, Tuple
from pathlib import Path
from config import MEMORY_LENGTH
from src.modules.chunk_history import assemble_chunks
from src.modules.save_history import get_chat_history
from src.modules.logging_setup import logger

def assemble_prompt_with_history(current_prompt: str) -> str:
    logger.info("Assembling prompt with history")
    chat_history = get_chat_history()
    logger.debug(f"Retrieved {len(chat_history)} entries from chat history")

    history_prompts = [f"User: {entry['prompt']}\nAssistant: {entry['response']}" for entry in chat_history]
    history_prompts_str = "\n\n".join(history_prompts)
    logger.debug(f"Assembled history prompts (first 100 chars): {history_prompts_str[:100]}...")

    chunk_history_str = assemble_chunks()
    logger.debug(f"Assembled chunk history (first 100 chars): {chunk_history_str[:100]}...")

    assembled_prompt = f"{history_prompts_str}\n\nChunk History:\n{chunk_history_str}\n\nUser: {current_prompt}\nAssistant:"
    logger.info(f"Final assembled prompt length: {len(assembled_prompt)} characters")
    return assembled_prompt

def get_chat_history_tuples() -> List[Tuple[str, str]]:
    logger.info("Retrieving chat history as tuples")
    chat_history = get_chat_history()
    history_tuples = [(entry['prompt'], entry['response']) for entry in chat_history]
    logger.debug(f"Retrieved {len(history_tuples)} history tuples")
    return history_tuples

def truncate_chat_history(n: int):
    logger.info(f"Truncating chat history to last {n} entries")
    from src.modules.save_history import chat_history
    original_length = len(chat_history.history)
    chat_history.history = chat_history.history[-n:] if n > 0 else []
    chat_history.save_history()
    logger.info(f"Chat history truncated from {original_length} to {len(chat_history.history)} entries")

# The following functions are kept for backwards compatibility
# and to ensure we don't remove any functionality

def add_to_chat_history(prompt: str, response: str):
    logger.info("Adding new entry to chat history")
    from src.modules.save_history import save_interaction
    save_interaction(prompt, response, "User", "DefaultModel")
    logger.debug(f"Added chat history entry - Prompt: '{prompt[:50]}...', Response: '{response[:50]}...'")

def save_chat_history():
    logger.info("Saving chat history")
    from src.modules.save_history import chat_history
    chat_history.save_history()
    logger.debug(f"Saved {len(chat_history.history)} entries to chat history")

def load_chat_history():
    logger.info("Loading chat history")
    from src.modules.save_history import chat_history
    chat_history.load_history()
    logger.debug(f"Loaded {len(chat_history.history)} entries from chat history")
