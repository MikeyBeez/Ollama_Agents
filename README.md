# Ollama_Agents: Your Personal AI Assistant Builder 🤖

Welcome to Ollama_Agents! This repository allows you to create spectacular AI agents using Ollama. It's like having a LEGO set for AI - mix, match, and build your dream assistants! 🧱✨

## 🚀 What's New?

- 🎭 Multi-agent system: Interact with multiple AI personalities
- 🔀 Easy agent selection from the main menu
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
9. 🎭 Multi-Agent System: Interact with multiple AI personalities in one session.

## 🛠️ Getting Started

### Prerequisites

- Python 3.8 or higher
- Conda (for managing virtual environments)
- Ollama (for running local language models)

### Setting Up the Environment

1. Fork and clone this repository:
   ```bash
   git clone https://github.com/yourusername/Ollama_Agents.git
   cd Ollama_Agents
   ```

2. Create and activate a conda virtual environment:
   ```bash
   conda create -n Ollama_Agents python=3.8
   conda activate Ollama_Agents
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your PYTHONPATH:
   ```bash
   export PYTHONPATH=/path/to/your/Ollama_Agents:$PYTHONPATH
   ```

### Installing Ollama

1. Visit the [Ollama website](https://ollama.com/) and follow the installation instructions for your operating system.

2. Once installed, run Ollama and download a model (e.g., llama3.1:latest):
   ```bash
   ollama run llama3.1:latest
   ```

### Configuration

1. Customize your AI in `config.py`.

2. Set up your API keys and other configurations in a `.env` file (use `.env.example` as a template).

### Running the Application

Run the main script:
```bash
python -m src.main
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

## 🎭 Multi-Agent System

Our new multi-agent system allows you to interact with different AI personalities:

1. Run the main script: `python -m src.main`
2. Choose the multi-agent option from the menu.
3. Select an agent to chat with (e.g., Alice, Bob, or Charlie).
4. Chat with the selected agent.
5. Type 'back' to return to the agent selection menu.

## 🤝 Contributing

Got ideas? We love them! 💡 Submit a pull request or open an issue. Let's build the future of AI together!

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Built with ❤️ and ☕ by the Ollama_Agents team. Let's make AI magic happen! ✨
