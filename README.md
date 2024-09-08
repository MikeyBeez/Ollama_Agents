# 🤖 Ollama_Agents: Your Advanced AI Assistant Builder with Graph Knowledgebase 🚀

Welcome to Ollama_Agents! This repository allows you to create sophisticated AI agents using Ollama, featuring a unique graph-based knowledgebase. It's like having a high-tech AI laboratory with a built-in brain! 🧠✨

## 🌟 What's New?

- 🕸️ Graph-based Knowledgebase: A novel approach using JSON for flexible, relational knowledge storage
- 🧠 Enhanced Debug Agent with detailed cognitive processing visualization
- 🌳 Dynamic Knowledge Tree generation and management
- 🔍 Improved memory search and context management
- 🧐 Fact-checking and source credibility assessment
- 🎭 Multi-agent system with easy switching between agents
- 🔀 Interactive follow-up question handling
- 🎨 Rich, colorful command-line interface with progress tracking
- 🛠️ Modular design with improved error handling and logging

## 🖥️ Development Environment

This project is being developed on an M1 Mac Mini with 16GB of RAM, ensuring optimal performance for AI agent creation and testing.

## 🚀 Key Features

1. 📊 Graph Knowledgebase: Utilizes a JSON-based graph structure for flexible and relational knowledge representation
2. 📚 Modular Architecture: Each function is in a separate module for easy customization and extension
3. 💬 Interactive CLI: Built with `rich` for a cinematic experience!
4. 🔐 Secure Configuration: Customize your AI's personality and behavior in `config.py`
5. 🧪 Comprehensive Testing: Because quality is our superpower!
6. 🌐 Web Search Integration: Your AI can search the web using DuckDuckGo
7. 📜 Advanced Chat History: Never forget a conversation with built-in history management and analysis
8. 🧠 Sophisticated Memory Search: Quickly retrieve and utilize relevant information from past interactions and uploaded documents
9. 🧵 Fabric Integration: Use Fabric patterns for enhanced AI interactions
10. 🎭 Multi-Agent System: Interact with multiple AI personalities in one session
11. 🤖 Debug Mode: Visualize the agent's thought process and decision-making in real-time
12. 🌳 Knowledge Tree: Dynamic generation and visualization of knowledge structures
13. 🧐 Fact-Checking: Verify information and assess source credibility
14. 👤 User Profiling: Adapt responses based on user expertise and interests

## 💡 Why JSON-based Graph Knowledgebase?

Our unique approach of using a JSON-based graph structure for the knowledgebase offers several advantages:

1. 🔄 Flexibility: Easily adapt and evolve the knowledge structure as your AI learns
2. 🔗 Rich Relationships: Capture complex relationships between concepts more intuitively than in traditional vector databases
3. 🚀 Performance: Efficient querying and updating of interconnected information
4. 🧩 Simplicity: No need for complex vector database setups or maintenance
5. 📦 Portability: JSON format allows for easy data transfer and backup
6. 🔍 Interpretability: Graph structure provides clear visibility into the AI's knowledge connections

This approach allows Ollama_Agents to have a more nuanced and context-aware understanding, leading to more intelligent and adaptive responses.

## 🛠️ Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Ollama

### Setting Up the Environment

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/Ollama_Agents.git
   cd Ollama_Agents
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
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

2. Once installed, run Ollama and download a model (e.g., llama2:latest):
   ```bash
   ollama run llama2:latest
   ```

### Configuration

1. Customize your AI in `config.py`.

2. Set up your API keys and other configurations in a `.env` file (use `.env.example` as a template).

### Running the Application

Run the main script:
```bash
python -m src.main
```

## 📘 Module Documentation

Detailed documentation for each module can be found in the `docs/` directory. This includes information on both standard and advanced (adv_) modules:

### Core Modules
- [Input Module](docs/input_module.md)
- [Ollama Client](docs/ollama_client.md)
- [Assemble Module](docs/assemble_module.md)
- [Banner Module](docs/banner_module.md)
- [DuckDuckGo Search](docs/ddg_search_module.md)

### Advanced (adv_) Modules
- [Advanced Input Processor](docs/adv_input_processor.md)
- [Advanced Context Manager](docs/adv_context_manager.md)
- [Advanced Reasoning Engine](docs/adv_reasoning_engine.md)
- [Advanced Planning Engine](docs/adv_planning_engine.md)
- [Advanced Knowledge Manager](docs/adv_knowledge_manager.md)
- [Advanced Output Manager](docs/adv_output_manager.md)

### Agent and Knowledge Management
- [Agent Tools](docs/agent_tools.md)
- [Knowledge Management](docs/knowledge_management.md)
- [Context Management](docs/context_management.md)
- [KB Graph](docs/kb_graph.md)

### System Architecture and Configuration
- [Architecture Guide](docs/architecture_guide.md)
- [Command Modules](docs/command_modules.md)
- [Config File](docs/config_file.md)

### Memory and History
- [JSON Memory Guide](docs/json_memory_guide.md)
- [Save History](docs/save_history.md)

### Utility and Logging
- [Logging Guide](docs/logging_guide.md)
- [Error Handling](docs/error_handling.md)

### User Guides
- [Building Agents](docs/building_agents.md)
- [Assistant User Guide](docs/assistant_user_guide.md)

## 🧠 Debug Agent Commands

- `/help`: Show available commands
- `/search <query>`: Perform an interactive web search
- `/context`: Show current context
- `/clear_context`: Clear the current context and bullet points
- `/bullets`: Display current bullet points
- `/knowledge_tree`: Display the knowledge tree
- `/explain <concept>`: Get an explanation of a concept
- `/fact_check <statement>`: Perform a fact check on a statement
- `/profile`: Display your user profile

## 🤝 Contributing

Got ideas? We love them! 💡 Submit a pull request or open an issue. Let's build the future of AI together!

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Built with ❤️ and 🧠 by the Ollama_Agents team. Let's revolutionize AI knowledge representation! 🚀
