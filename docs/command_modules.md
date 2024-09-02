# 📚 Ollama_Agents: Command Modules Documentation

## 1. 📄 document_commands.py

### Purpose:
This module handles all document-related operations in Ollama_Agents, including file selection, document chunking, embedding generation, and document uploading.

### Functions:

#### `pick_file() -> str`
- Allows the user to interactively select a file from their file system.
- Returns the path of the selected file or None if the selection is cancelled.

#### `chunk_document(file_path: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]`
- Splits a document into smaller chunks for processing.
- Ensures chunks end at sentence boundaries for context preservation.
- Returns a list of text chunks.

#### `generate_embeddings(text: str, model: str) -> List[float]`
- Generates embeddings for a given text using the specified model.
- Returns a list of floats representing the embedding.

#### `upload_document(command: str) -> str`
- Main function for document upload process.
- Handles file selection, chunking, embedding generation, and storage.
- Returns 'CONTINUE' to indicate completion.

#### `print_chunk_history(command: str = '') -> str`
- Displays the current chunk history.
- Returns 'CONTINUE' after printing.

### Code Separation:
By isolating document-related operations in this module, we achieve:
- Clear separation of concerns for document handling.
- Easier maintenance and updates of document processing logic.
- Modular design allowing for easy extension of document-related features.

## 2. 🛠️ basic_commands.py

### Purpose:
This module implements core slash commands and basic utility functions for Ollama_Agents.

### Functions:

#### `get_ollama_models() -> List[str]`
- Retrieves a list of available Ollama models.
- Returns a list of model names.

#### `change_model_command(command: str) -> str`
- Allows the user to change the current Ollama model.
- Updates the config file with the new model selection.
- Returns 'CONTINUE' after model change.

#### `update_config_model(new_model: str)`
- Updates the `config.py` file with the new model selection.

#### `duck_duck_go_search(command: str) -> str`
- Performs a web search using DuckDuckGo.
- Returns 'CONTINUE' after displaying search results.

### Code Separation:
Separating these basic commands into their own module provides:
- A centralized location for core utility functions.
- Easier management of basic system-wide commands.
- Improved readability by keeping the main application logic cleaner.

## 3. 🧵 fabric_commands.py

### Purpose:
This module integrates Fabric pattern functionality into Ollama_Agents, allowing for enhanced AI interactions using predefined patterns.

### Functions:

#### `get_fabric_patterns() -> List[str]`
- Retrieves a list of available Fabric patterns.
- Returns a list of pattern names.

#### `fabric_command(command: str) -> str`
- Main function for executing Fabric patterns.
- Allows user to select a pattern and provide input.
- Processes the input using the selected Fabric pattern.
- Saves the output as a new memory.
- Returns 'CONTINUE' after pattern execution.

### Code Separation:
By isolating Fabric-related functionality in this module:
- We maintain a clear boundary for Fabric pattern integration.
- It's easier to extend or modify Fabric-related features without affecting other parts of the system.
- We keep the main application logic clean and focused on core functionality.

## 🔄 How This Separation Enhances the Project

1. **Modularity**: Each module focuses on a specific set of related functions, making the codebase more modular and easier to understand.

2. **Maintainability**: Changes to one aspect (e.g., document handling) can be made without affecting other parts of the system.

3. **Scalability**: New features or commands can be added by creating new modules or extending existing ones without cluttering the main application logic.

4. **Readability**: Developers can quickly locate specific functionality by referring to the appropriate module.

5. **Testing**: Separating functionality into distinct modules makes it easier to write and maintain unit tests for each component.

6. **Collaboration**: Different team members can work on different modules simultaneously with reduced risk of conflicts.

7. **Flexibility**: This structure allows for easy swapping or upgrading of components (e.g., changing the document processing logic) without major system-wide changes.

By organizing the code in this way, Ollama_Agents maintains a clean, extensible, and maintainable architecture that can easily adapt to future enhancements and requirements.
