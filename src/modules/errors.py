# src/modules/errors.py

class OllamaAgentsError(Exception):
    """Base exception class for Ollama_Agents"""

class ConfigurationError(OllamaAgentsError):
    """Raised when there's a configuration issue"""

class APIConnectionError(OllamaAgentsError):
    """Raised when there's an issue connecting to an API"""

class InputError(OllamaAgentsError):
    """Raised when there's an issue with user input"""

class MemoryError(OllamaAgentsError):
    """Raised when there's an issue with memory operations"""

class FileOperationError(OllamaAgentsError):
    """Raised when there's an issue with file operations"""
