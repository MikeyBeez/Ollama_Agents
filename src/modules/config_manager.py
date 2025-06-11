# src/modules/config_manager.py

import os
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file

        # Basic configuration
        self.AGENT_NAME = os.getenv("AGENT_NAME", "MemoryAgent")
        self.USER_NAME = os.getenv("USER_NAME", "User")
        self.MODEL_NAME = os.getenv("MODEL_NAME", "llama2")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

        # Memory-specific configuration
        self.MEMORY_STORAGE_PATH = os.getenv("MEMORY_STORAGE_PATH", "/users/bard/mcp/chat_history/data")
        self.MEMORY_INDEX_NAME = os.getenv("MEMORY_INDEX_NAME", "memory_index")
        self.MAX_SUMMARY_LENGTH = int(os.getenv("MAX_SUMMARY_LENGTH", "200"))
        self.MAX_TOPICS_PER_CONV = int(os.getenv("MAX_TOPICS_PER_CONV", "5"))

        # Ollama configuration
        self.OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")

        # Logging configuration
        self.LOG_FILE = os.getenv("LOG_FILE", "logs/ollama_agents.log")