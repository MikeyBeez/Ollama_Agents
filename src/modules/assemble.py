import json
from typing import List, Tuple
from pathlib import Path

class ChatHistory:
    def __init__(self, max_length: int = 15):
        self.history: List[Tuple[str, str]] = []
        self.max_length = max_length
        self.file_path = Path.home() / ".ai_functions_chat_history.json"

    def add_entry(self, prompt: str, response: str):
        self.history.append((prompt, response))
        if len(self.history) > self.max_length:
            self.history.pop(0)

    def assemble_prompt_with_history(self, current_prompt: str) -> str:
        history_prompts = [f"User: {prompt}\nAssistant: {response}" for prompt, response in self.history]
        history_prompts_str = "\n\n".join(history_prompts)
        assembled_prompt = f"{history_prompts_str}\n\nUser: {current_prompt}\nAssistant:"
        return assembled_prompt

    def get_history(self) -> List[Tuple[str, str]]:
        return self.history

    def truncate(self, n: int):
        self.history = self.history[-n:] if n > 0 else []

    def save_history(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.history, f)

    def load_history(self):
        if self.file_path.exists():
            with open(self.file_path, 'r') as f:
                self.history = json.load(f)
            self.history = self.history[-self.max_length:]  # Ensure we don't exceed max_length

# Create a singleton instance of ChatHistory
chat_history = ChatHistory()

# Export the functions to be used in other modules
def add_to_chat_history(prompt: str, response: str):
    chat_history.add_entry(prompt, response)

def assemble_prompt_with_history(current_prompt: str) -> str:
    return chat_history.assemble_prompt_with_history(current_prompt)

def get_chat_history() -> List[Tuple[str, str]]:
    return chat_history.get_history()

def truncate_chat_history(n: int):
    chat_history.truncate(n)

def save_chat_history():
    chat_history.save_history()

def load_chat_history():
    chat_history.load_history()
