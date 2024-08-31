import json
import os
from datetime import datetime
from pathlib import Path
from config import MEMORY_LENGTH

class ChatHistory:
    _instance = None

    def __new__(cls, max_length):
        if cls._instance is None:
            cls._instance = super(ChatHistory, cls).__new__(cls)
            cls._instance.max_length = max_length
            cls._instance.history = []
            cls._instance.file_path = Path.home() / ".ai_functions_chat_history.json"
            cls._instance.load_history()
        return cls._instance

    def add_entry(self, prompt, response):
        self.history.append({"prompt": prompt, "response": response})
        if len(self.history) > self.max_length:
            self.history.pop(0)
        self.save_history()

    def get_history(self):
        return self.history

    def save_history(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def load_history(self):
        if self.file_path.exists():
            with open(self.file_path, 'r', encoding='utf-8') as f:
                loaded_history = json.load(f)
                # Ensure all entries are in the correct format
                self.history = [
                    {"prompt": entry["prompt"], "response": entry["response"]}
                    for entry in loaded_history
                    if isinstance(entry, dict) and "prompt" in entry and "response" in entry
                ]
            self.history = self.history[-self.max_length:]

# Create a singleton instance of ChatHistory
chat_history = ChatHistory(MEMORY_LENGTH)

def save_memory(memory_type, content, username, model_name, metadata=None):
    # Create the data directory if it doesn't exist
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data" / "json_history"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{memory_type}.json"

    # Prepare the data to be saved
    data = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "model_name": model_name,
        "type": memory_type,
        "content": content,
    }
    if metadata:
        data.update(metadata)

    # Save the data as a JSON file
    file_path = data_dir / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Add the entry to the chat history
    if memory_type == "interaction":
        chat_history.add_entry(content["prompt"], content["response"])

def save_interaction(prompt, response, username, model_name):
    save_memory("interaction", {"prompt": prompt, "response": response}, username, model_name)

def save_document_chunk(chunk_id, chunk_content, username, model_name):
    save_memory("document_chunk", chunk_content, username, model_name, {"chunk_id": chunk_id})

def get_chat_history():
    return chat_history.get_history()
