# 🛠️ Ollama_Agents Setup Guide

This guide will help you set up your development environment for Ollama_Agents.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git
- Ollama

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Ollama_Agents.git
cd Ollama_Agents
```

## Step 2: Set Up a Virtual Environment

We recommend using a virtual environment to manage dependencies.
Install Anaconda if you need to:

```bash
conda create -name Ollama_Agents python=3.8
conda activate Ollama_Agents
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Set Up Ollama

1. Visit [Ollama's website](https://ollama.ai/) and follow their installation instructions.
2. Once installed, pull the default model:

```bash
ollama pull llama3.1:latest
```

## Step 5: Configure Environment Variables

Create a `.env` file in the project root to store your configuration:

```
AI_USER_NAME=YourName
AI_AGENT_NAME=AssistantName
AI_DEFAULT_MODEL=llama3.1:latest
AI_LOG_LEVEL=INFO
```

## Step 6: Set PYTHONPATH

Add the following line to your `.bashrc`, `.zshrc`, or equivalent shell configuration file:

```bash
export PYTHONPATH=/path/to/your/Ollama_Agents:$PYTHONPATH
```

Replace `/path/to/your/Ollama_Agents` with the actual path to your project directory.

After adding this line, restart your terminal or run:

```bash
source ~/.bashrc  # or source ~/.zshrc if you're using zsh
```

## Step 7: Run Tests

Ensure everything is set up correctly by running the test suite:

```bash
python -m unittest discover src/tests
```

## Step 8: Run the Application

```bash
python -m src.main
```

You're now ready to start developing with Ollama_Agents!

## Troubleshooting

- If you encounter any issues with Ollama, ensure it's running and accessible.
- For dependency issues, try updating your pip and setuptools:
  `pip install --upgrade pip setuptools`

For more help, please open an issue on the GitHub repository.
