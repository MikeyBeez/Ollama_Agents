# AI_Functions: Your Personal AI Assistant Builder 🤖

Welcome to AI_Functions! This repository allows you to create a spectacular AI agent using Ollama. It's like having a LEGO set for AI - mix, match, and build your dream assistant! 🧱✨

## 🚀 What's New?

- 🎨 Colorful command-line interface
- 🧠 Enhanced memory management
- 🔍 Integrated DuckDuckGo search capabilities
- 🛠️ Improved modular design for easy customization
- 🔎 Memory search commands: `/ms` and `/msl`
- 🧵 New `/fabric` command for using Fabric patterns
- 📂 Refactored command structure for better organization
- 🧪 Comprehensive test suite added

## 🌟 Key Features

1. 📚 Modular Architecture: Each function is in a separate module, making it easy to add, remove, or modify features.
2. 💬 Interactive CLI: Built with `prompt_toolkit` for a sci-fi movie-worthy experience!
3. 🔐 Secure Configuration: Customize your AI's personality in `config.py`.
4. 🧪 Comprehensive Testing: Because quality is our superpower!
5. 🌐 Web Search Integration: Your AI can now search the web using DuckDuckGo.
6. 📜 Chat History: Never forget a conversation with built-in history management.
7. 🧠 Memory Search: Quickly retrieve and utilize relevant information from past interactions and uploaded documents.
8. 🧵 Fabric Integration: Use Fabric patterns for enhanced AI interactions.

## 🛠️ Getting Started

### Prerequisites

- Python 3.8 or higher
- Conda (for managing virtual environments)
- Ollama (for running local language models)

### Setting Up the Environment

1. Fork and clone this repository:
   ```bash
   git clone https://github.com/yourusername/AI_Functions.git
   cd AI_Functions
   ```

2. Create and activate a conda virtual environment:
   ```bash
   conda create -n ai_functions python=3.8
   conda activate ai_functions
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Installing Ollama

1. Visit the [Ollama website](https://ollama.com/) and follow the installation instructions for your operating system.

2. Once installed, run Ollama and download a model (e.g., llama2):
   ```bash
   ollama run llama2
   ```

### Configuration

1. Customize your AI in `config.py`.

2. Set up your API keys and other configurations in a `.env` file (use `.env.example` as a template). Currently only Ollama is supported.

### Running the Application

Run the main script:
```bash
python src/main.py
```

## 🧪 Running Tests

Ensure your AI is in top shape:

```bash
python -m unittest discover src/tests
```

## 📘 Module Documentation

- 🎛️ [Input Module](docs/input_module.md)
- 🤖 [Ollama Client](docs/ollama_client.md)
- 🧩 [Assemble Module](docs/assemble_module.md)
- 🎨 [Banner Module](docs/banner_module.md)
- 🔍 [DuckDuckGo Search](docs/ddg_search_module.md)
- 🏗️ [Architecture Guide](docs/architecture_guide.md)

## 🔍 Memory Search Commands

- `/ms n m query`: Search memories and process query (short version, only shows answer)
- `/msl n m query`: Search memories and process query (long version, shows memories and answer)
  - `n`: Number of top results to retrieve
  - `m`: Minimum similarity threshold (0-1)
  - `query`: Your question or prompt
  Example: `/ms 5 0.7 Who was Alan Turing?`

## 🧵 Fabric Command

Use the `/fabric` command to interact with Fabric patterns:

1. Type `/fabric` in the chat interface.
2. Select a pattern from the list provided.
3. Enter the input text for the selected pattern.
4. The AI will process your input using the chosen Fabric pattern and return the result.

## 📂 File Structure

The project structure has been updated to include a comprehensive test suite and consolidated documentation:

```
AI_Functions/
├── src/
│   ├── modules/
│   │   ├── __init__.py
│   │   ├── assemble.py
│   │   ├── banner.py
│   │   ├── basic_commands.py
│   │   ├── chunk_history.py
│   │   ├── ddg_search.py
│   │   ├── document_commands.py
│   │   ├── fabric_commands.py
│   │   ├── file_utils.py
│   │   ├── input.py
│   │   ├── memory_commands.py
│   │   ├── memory_search.py
│   │   ├── ollama_client.py
│   │   ├── save_history.py
│   │   └── slash_commands.py
│   ├── tests/
│   │   ├── test_file_utils.py
│   │   ├── test_input.py
│   │   ├── test_memory_search.py
│   │   ├── test_ollama_client.py
│   │   └── test_save_history.py
│   └── main.py
├── docs/
│   ├── architecture_guide.md
│   ├── assemble_module.md
│   ├── banner_module.md
│   ├── ddg_search_module.md
│   ├── input_module.md
│   └── ollama_client.md
├── config.py
├── requirements.txt
└── README.md
```
## 📚 Additional Documentation

To provide a deeper understanding of AI_Functions, we've expanded our documentation. These additional resources offer insights into the system's architecture, module interactions, and design principles.

### 🏗️ Architecture Guide

For a comprehensive overview of AI_Functions' structure and design, refer to our [Architecture Guide](docs/architecture_guide.md). This document covers:

- 🔍 High-level system overview
- 🧩 Detailed module descriptions and interactions
- 🔄 Data flow through the system
- 🛠️ Key design patterns and principles used
- 🚀 Scalability and future expansion considerations

The architecture guide is essential reading for developers looking to understand, modify, or extend AI_Functions.

### 🧠 Core Components

Detailed documentation for each core component is available:

- [Input Module](docs/input_module.md): Handles user input processing and command routing
- [Ollama Client](docs/ollama_client.md): Manages communication with the Ollama AI model
- [Memory Search](docs/memory_search.md): Implements advanced memory retrieval functionality
- [Document Processing](docs/document_processing.md): Covers document upload and chunking processes

### 🛠️ Development Guides

For contributors and developers:

- [Setup Guide](docs/setup_guide.md): Detailed instructions for setting up the development environment
- [Testing Strategy](docs/testing_strategy.md): Overview of our testing approach and guidelines for writing tests
- [Contribution Guidelines](docs/contributing.md): How to contribute to AI_Functions effectively

### 🔄 Workflow Diagrams

Visual representations of key processes:

- [User Interaction Workflow](docs/diagrams/user_interaction_workflow.png)
- [Memory Search Process](docs/diagrams/memory_search_process.png)
- [Document Upload and Processing](docs/diagrams/document_processing_workflow.png)

These diagrams provide a clear visual understanding of the system's operations.

### 📘 API Documentation

For those integrating with AI_Functions:

- [API Reference](docs/api_reference.md): Detailed documentation of public APIs and integration points

### 🔮 Future Roadmap

Explore our plans for future development:

- [Roadmap](docs/roadmap.md): Upcoming features, improvements, and long-term vision for AI_Functions

We encourage all users, developers, and contributors to explore these resources. They are designed to provide a comprehensive understanding of AI_Functions, from high-level architecture to specific implementation details.
```

## 🤝 Contributing

Got ideas? We love them! 💡 Submit a pull request or open an issue. Let's build the future of AI together!

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Built with ❤️ and ☕ by the AI_Functions team. Let's make AI magic happen! ✨
