# src/modules/save_history.py

from datetime import datetime
from pathlib import Path
from config import MEMORY_LENGTH, DATA_DIR, CHAT_HISTORY_FILE
from .file_utils import read_json_file, write_json_file, ensure_directory_exists
from .logging_setup import logger

class ChatHistory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatHistory, cls).__new__(cls)
            cls._instance.max_length = MEMORY_LENGTH
            cls._instance.history = []
            cls._instance.file_path = CHAT_HISTORY_FILE
            cls._instance.load_history()
        return cls._instance

    def add_entry(self, prompt, response):
        self.history.append({"prompt": prompt, "response": response})
        if len(self.history) > self.max_length:
            self.history.pop(0)
        self.save_history()
        logger.info(f"Added new entry to chat history. Total entries: {len(self.history)}")

    def get_history(self):
        return self.history

    def save_history(self):
        write_json_file(self.file_path, self.history)
        logger.info(f"Saved chat history to {self.file_path}")

    def load_history(self):
        if self.file_path.exists():
            loaded_history = read_json_file(self.file_path)
            self.history = [
                {"prompt": entry["prompt"], "response": entry["response"]}
                for entry in loaded_history
                if isinstance(entry, dict) and "prompt" in entry and "response" in entry
            ][-self.max_length:]
            logger.info(f"Loaded {len(self.history)} entries from chat history")
        else:
            logger.warning(f"Chat history file not found at {self.file_path}")

chat_history = ChatHistory()

def save_memory(memory_type, content, username, model_name, metadata=None):
    ensure_directory_exists(DATA_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{memory_type}.json"
    data = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "model_name": model_name,
        "type": memory_type,
        "content": content,
        "access_count": 0,
        "permanent_marker": 0
    }
    if metadata:
        data.update(metadata)
    file_path = DATA_DIR / filename
    write_json_file(file_path, data)
    logger.info(f"Saved {memory_type} memory: {filename}")

def save_interaction(prompt, response, username, model_name):
    save_memory("interaction", {"prompt": prompt, "response": response}, username, model_name)
    logger.debug(f"Saved interaction for user {username}")

def save_document_chunk(chunk_id, chunk_content, username, model_name):
    save_memory("document_chunk", chunk_content, username, model_name, {"chunk_id": chunk_id})
    logger.debug(f"Saved document chunk {chunk_id} for user {username}")

def get_chat_history():
    return chat_history.get_history()
