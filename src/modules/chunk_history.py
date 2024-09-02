# src/modules/chunk_history.py

from typing import List
from collections import deque
import json
from pathlib import Path
from config import CHUNK_LENGTH
from src.modules.logging_setup import logger
from src.modules.errors import FileOperationError

class ChunkHistory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChunkHistory, cls).__new__(cls)
            cls._instance.chunks = deque(maxlen=CHUNK_LENGTH)
            cls._instance.file_path = Path.home() / ".ollama_agents_chunk_history.json"
            cls._instance.load_history()
            logger.info("ChunkHistory instance created")
        return cls._instance

    def add_chunk(self, chunk: str):
        logger.info("Adding new chunk to history")
        self.chunks.append(chunk)
        self.save_history()
        logger.debug(f"Added chunk (first 50 chars): {chunk[:50]}...")
        logger.debug(f"Total chunks in history: {len(self.chunks)}")

    def get_chunks(self) -> List[str]:
        logger.info("Retrieving all chunks from history")
        logger.debug(f"Returning {len(self.chunks)} chunks")
        return list(self.chunks)

    def assemble_chunks(self) -> str:
        logger.info("Assembling all chunks into a single string")
        assembled = "\n\n".join(self.chunks)
        logger.debug(f"Assembled chunks (total length: {len(assembled)})")
        return assembled

    def save_history(self):
        logger.info(f"Saving chunk history to file: {self.file_path}")
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(list(self.chunks), f, ensure_ascii=False, indent=2)
            logger.debug(f"Successfully saved {len(self.chunks)} chunks to file")
        except IOError as e:
            logger.error(f"Error saving chunk history to file: {self.file_path}. Error: {str(e)}")
            raise FileOperationError(f"Failed to save chunk history to {self.file_path}: {str(e)}")

    def load_history(self):
        logger.info(f"Loading chunk history from file: {self.file_path}")
        if self.file_path.exists():
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    loaded_chunks = json.load(f)
                self.chunks = deque(loaded_chunks, maxlen=CHUNK_LENGTH)
                logger.debug(f"Successfully loaded {len(self.chunks)} chunks from file")
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from file: {self.file_path}. Error: {str(e)}")
                raise FileOperationError(f"Failed to decode JSON from {self.file_path}: {str(e)}")
            except IOError as e:
                logger.error(f"Error reading chunk history file: {self.file_path}. Error: {str(e)}")
                raise FileOperationError(f"Failed to read chunk history from {self.file_path}: {str(e)}")
        else:
            logger.warning(f"Chunk history file not found: {self.file_path}")

# Create a singleton instance
chunk_history = ChunkHistory()
logger.info("ChunkHistory singleton instance created")

def add_to_chunk_history(chunk: str):
    logger.info("Adding chunk to history via global function")
    chunk_history.add_chunk(chunk)

def get_chunk_history() -> List[str]:
    logger.info("Retrieving chunk history via global function")
    return chunk_history.get_chunks()

def assemble_chunks() -> str:
    logger.info("Assembling chunks via global function")
    return chunk_history.assemble_chunks()
