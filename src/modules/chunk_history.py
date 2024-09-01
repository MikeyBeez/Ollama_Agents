# src/modules/chunk_history.py

from typing import List
from collections import deque
import json
from pathlib import Path
from config import CHUNK_LENGTH

class ChunkHistory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChunkHistory, cls).__new__(cls)
            cls._instance.chunks = deque(maxlen=CHUNK_LENGTH)
            cls._instance.file_path = Path.home() / ".ollama_agents_chunk_history.json"
            cls._instance.load_history()
        return cls._instance

    def add_chunk(self, chunk: str):
        self.chunks.append(chunk)
        self.save_history()

    def get_chunks(self) -> List[str]:
        return list(self.chunks)

    def assemble_chunks(self) -> str:
        return "\n\n".join(self.chunks)

    def save_history(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(list(self.chunks), f, ensure_ascii=False, indent=2)

    def load_history(self):
        if self.file_path.exists():
            with open(self.file_path, 'r', encoding='utf-8') as f:
                loaded_chunks = json.load(f)
                self.chunks = deque(loaded_chunks, maxlen=CHUNK_LENGTH)

# Create a singleton instance
chunk_history = ChunkHistory()

def add_to_chunk_history(chunk: str):
    chunk_history.add_chunk(chunk)

def get_chunk_history() -> List[str]:
    return chunk_history.get_chunks()

def assemble_chunks() -> str:
    return chunk_history.assemble_chunks()
