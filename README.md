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
- 🔍 Advanced Analogy Finding: Discover insightful analogies to explain complex concepts
- 🚦 Contradiction Detection and Resolution: Identify and resolve conflicting information
- 🧪 Hypothesis Generation and Testing: Create and evaluate hypotheses based on available data
- 🔗 Causal Reasoning: Infer and analyze cause-and-effect relationships

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
15. 🔍 Advanced Analogy Finding: Discover insightful analogies to explain complex concepts
16. 🚦 Contradiction Detection and Resolution: Identify and resolve conflicting information
17. 🧪 Hypothesis Generation and Testing: Create and evaluate hypotheses based on available data
18. 🔗 Causal Reasoning: Infer and analyze cause-and-effect relationships

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

Detailed documentation for each module can be found in the `docs/` directory:

### Core Modules
- [Input Module](docs/input_module.md)
- [Ollama Client](docs/ollama_client.md)
- [Assemble Module](docs/assemble_module.md)
- [Banner Module](docs/banner_module.md)
- [DuckDuckGo Search](docs/ddg_search_module.md)

### Agent and Knowledge Management
- [Agent Tools](docs/agent_tools.md)
- [Knowledge Management](docs/knowledge_management.md)
- [Context Management](docs/context_management.md)
- [KB Graph](docs/kb_graph.md)

### Reasoning and Analysis
- [Causal Reasoning](docs/causal_reasoning.md)
- [Hypothesis Testing](docs/hypothesis_testing.md)
- [Research Tools](docs/research_tools.md)

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
- `/graph`: Visualize the current state of the graph knowledgebase

## 🕸️ Graph Knowledgebase

Our graph knowledgebase is implemented in `src/modules/kb_graph.py`. It uses a JSON structure to represent nodes and edges, allowing for flexible and powerful knowledge representation. Key features include:

- 📊 Efficient storage of relationships between concepts
- 🔍 Fast querying of related information
- 🧠 Dynamic updating of knowledge as the AI learns
- 🌐 Easy integration with web search results and user interactions

To interact with the graph knowledgebase, use the `/graph` command in the debug agent.

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

Our multi-agent system allows you to interact with different AI personalities:

1. Run the main script: `python -m src.main`
2. Choose the multi-agent option from the menu.
3. Select an agent to chat with (e.g., Alice, Bob, or Charlie).
4. Chat with the selected agent.
5. Type 'back' to return to the agent selection menu.

## 🛠️ Advanced Agent Tools

Our `agent_tools.py` module now includes several advanced functions for sophisticated reasoning:

- `find_analogies()`: Discovers insightful analogies to explain complex concepts
- `detect_contradictions()`: Identifies conflicting information within a given dataset
- `resolve_contradictions()`: Proposes resolutions for detected contradictions
- `generate_hypotheses()`: Creates plausible hypotheses based on available data
- `design_experiment()`: Outlines experimental procedures to test generated hypotheses
- `infer_causal_relationships()`: Analyzes potential cause-and-effect relationships
- `analyze_causal_chain()`: Examines the sequence of events in a causal chain

These tools enable our agents to perform more nuanced and context-aware reasoning, leading to more insightful and comprehensive responses.

## 🤖 Assistant Command

The `/assistant` command provides various helpful functions. For details, see the [Assistant User Guide](docs/assistant_user_guide.md).

## 🤝 Contributing

Got ideas? We love them! 💡 Submit a pull request or open an issue. Let's build the future of AI together!

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Built with ❤️ and 🧠 by the Ollama_Agents team. Let's revolutionize AI knowledge representation! 🚀
