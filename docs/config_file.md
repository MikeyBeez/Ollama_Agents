# Configuration File Documentation

## Overview

The `config.py` file serves as the central configuration hub for the Ollama_Agents project. It uses environment variables and the `pathlib` library to manage settings and paths, providing flexibility and portability across different environments.

## Key Components

### Environment Variables

The configuration uses `os.getenv()` to read environment variables, allowing for easy customization without modifying the code. For example:

```python
USER_NAME = os.getenv("AI_USER_NAME", "MikeBee")
```

This line sets `USER_NAME` to the value of the `AI_USER_NAME` environment variable if it exists, otherwise defaulting to "MikeBee".

### Pathlib Usage

The `pathlib` library is used for cross-platform path handling. For example:

```python
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "json_history"
```

This creates platform-independent paths, ensuring consistency across different operating systems.

## Configuration Sections

### User and Agent Configuration
- `USER_NAME`: Name of the user interacting with the system
- `AGENT_NAME`: Name of the AI agent

### Model Configuration
- `DEFAULT_MODEL`: Specifies the default language model
- `EMBEDDING_MODEL`: Specifies the model used for generating embeddings

### Memory Configuration
- `MEMORY_LENGTH`: Number of interactions to keep in short-term memory
- `CHUNK_SIZE`: Size of text chunks for processing
- `CHUNK_OVERLAP`: Overlap between chunks to maintain context
- `CHUNK_LENGTH`: Number of chunks to keep in memory

### Path Configuration
- `PROJECT_ROOT`: Root directory of the project
- `DATA_DIR`: Directory for storing JSON history files
- `EMBEDDINGS_DIR`: Directory for storing embedding files
- `CHAT_HISTORY_FILE`: Path to the chat history file

### Search Configuration
- `DEFAULT_TOP_K`: Number of top results to return in memory search
- `DEFAULT_SIMILARITY_THRESHOLD`: Minimum similarity score for search results

### Logging Configuration
- `LOG_LEVEL`: Sets the logging level
- `LOG_FILE`: Path to the log file

## Directory Creation

The configuration file ensures that necessary directories exist:

```python
DATA_DIR.mkdir(parents=True, exist_ok=True)
EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)
```

This automatically creates the required directories if they don't exist.

## Usage

To use these configurations in other parts of the project, simply import the required variables:

```python
from config import USER_NAME, DEFAULT_MODEL, DATA_DIR
```

## Customization

To customize the configuration:

1. Set environment variables before running the application, or
2. Modify the default values in the `config.py` file

For example, to change the user name:

```bash
export AI_USER_NAME="JohnDoe"
```

Or in the `config.py` file:

```python
USER_NAME = os.getenv("AI_USER_NAME", "JohnDoe")
```

## Best Practices

- Use environment variables for sensitive or frequently changing values
- Keep the `config.py` file under version control, but don't commit sensitive information
- Use `.env` files for local development and CI/CD pipelines for production environments
