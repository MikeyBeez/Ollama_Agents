# 🌈 AI_Functions: Your Personal AI Assistant Builder 🤖

Welcome to the magical world of AI_Functions! 🎉 This repository is your ticket to creating a spectacular AI agent using Ollama. It's like having a LEGO set for AI - mix, match, and build your dream assistant! 🧱✨

## 🚀 What's New?

- 🎨 Colorful command-line interface
- 🧠 Enhanced memory management
- 🔍 Integrated DuckDuckGo search capabilities
- 🛠️ Modular design for easy customization
- 🔎 New memory search commands: `/ms` and `/msl`

## 🌟 Key Features

1. **📚 Modular Architecture**: Each function is a separate module, making it easy to add, remove, or modify features.
2. **💬 Interactive CLI**: Built with `prompt_toolkit` for a sci-fi movie-worthy experience!
3. **🔐 Secure Configuration**: Customize your AI's personality in `config.py`.
4. **🧪 Comprehensive Testing**: Because quality is our superpower!
5. **🌐 Web Search Integration**: Your AI can now search the web using DuckDuckGo.
6. **📜 Chat History**: Never forget a conversation with built-in history management.
7. **🧠 Memory Search**: Quickly retrieve and utilize relevant information from past interactions and uploaded documents.

## 🛠️ Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/AI_Functions.git
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Customize your AI in `config.py`.
4. Run the main script:
   ```bash
   python src/main.py
   ```

## 🧪 Running Tests

Ensure your AI is in top shape:

```bash
python -m unittest discover src/tests
```

## 📘 Module Documentation

- [Input Module](docs/input_module.md)
- [Ollama Client](docs/ollama_client.md)
- [Assemble Module](docs/assemble_module.md)
- [Banner Module](docs/banner_module.md)
- [DuckDuckGo Search](docs/ddg_search_module.md)

## 🔍 Memory Search Commands

- `/ms n m query`: Search memories and process query (short version, only shows answer)
- `/msl n m query`: Search memories and process query (long version, shows memories and answer)
  - `n`: Number of top results to retrieve
  - `m`: Minimum similarity threshold (0-1)
  - `query`: Your question or prompt
  Example: `/ms 5 0.7 Who was Alan Turing?`

## 🤝 Contributing

Got ideas? We love them! 💡 Submit a pull request or open an issue. Let's build the future of AI together!

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Built with ❤️ and ☕ by the AI_Functions team. Let's make AI magic happen! ✨
