import json
import os
from datetime import datetime
from pathlib import Path
from config import MEMORY_LEGNTH  # Note: There's a typo in the config, it should be MEMORY_LENGTH

class ChatHistory:
    def __init__(self, max_length):
        self.max_length = max_length
        self.history = []

    def add_entry(self, entry):
        self.history.append(entry)
        if len(self.history) > self.max_length:
            self.history.pop(0)

    def get_history(self):
        return self.history

# Create a singleton instance of ChatHistory
chat_history = ChatHistory(MEMORY_LEGNTH)

def save_interaction(prompt, response, username, model_name):
    # Create the data directory if it doesn't exist
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data" / "json_history"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.json"

    # Prepare the data to be saved
    data = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "model_name": model_name,
        "prompt": prompt,
        "response": response,
    }

    # Save the data as a JSON file
    file_path = data_dir / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Add the entry to the chat history
    chat_history.add_entry(data)

def get_chat_history():
    return chat_history.get_history()
