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

class CommandExecutionError(OllamaAgentsError):
    """Raised when there's an error executing a command"""

class LogicProcessingError(OllamaAgentsError):
    """Raised when there's an error in the logic processing steps"""

class ModelInferenceError(OllamaAgentsError):
    """Raised when there's an error during model inference"""

class DataProcessingError(OllamaAgentsError):
    """Raised when there's an error processing data"""
