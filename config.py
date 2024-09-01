# config.py

import os
from pathlib import Path

# User and Agent configuration
# These settings define the names used for the user and AI agent in the system
USER_NAME = os.getenv("AI_USER_NAME", "MikeBee")
AGENT_NAME = os.getenv("AI_AGENT_NAME", "Otto")

# Model configuration
# Specify the default language model and embedding model to be used
DEFAULT_MODEL = "llama3.1:latest"
EMBEDDING_MODEL = os.getenv("AI_EMBEDDING_MODEL", "nomic-embed-text")

# Memory configuration
# These settings control how the system manages and processes memory
MEMORY_LENGTH = int(os.getenv("AI_MEMORY_LENGTH", "15"))  # Number of interactions to keep in short-term memory
CHUNK_SIZE = int(os.getenv("AI_CHUNK_SIZE", "5000"))  # Size of text chunks for processing
CHUNK_OVERLAP = int(os.getenv("AI_CHUNK_OVERLAP", "200"))  # Overlap between chunks to maintain context
CHUNK_LENGTH = int(os.getenv("AI_CHUNK_LENGTH", "10"))  # Number of chunks to keep in memory

# Path configuration
# Define important directories and files used by the system
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "json_history"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"

# Ensure directories exist
# Create necessary directories if they don't already exist
DATA_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

# File paths
# Specify locations for important files
CHAT_HISTORY_FILE = Path.home() / ".ollama_agents_chat_history.json"

# Search configuration
# Parameters for memory search functionality
DEFAULT_TOP_K = int(os.getenv("AI_DEFAULT_TOP_K", "5"))  # Number of top results to return in memory search
DEFAULT_SIMILARITY_THRESHOLD = float(os.getenv("AI_DEFAULT_SIMILARITY_THRESHOLD", "0.0"))  # Minimum similarity score for search results

# Logging configuration
# Settings for system logging
LOG_LEVEL = os.getenv("AI_LOG_LEVEL", "INFO")  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_FILE = PROJECT_ROOT / "logs" / "ollama_agents.log"  # Path to log file

# Ensure log directory exists
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
