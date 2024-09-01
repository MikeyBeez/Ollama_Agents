# 🛠️ AI_Functions Setup Guide

This guide will help you set up your development environment for AI_Functions.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/AI_Functions.git
cd AI_Functions
```

## Step 2: Set Up a Virtual Environment

We recommend using a virtual environment to manage dependencies.
Install Anaconda if you need to:

```bash
conda create -name AI_Functions python=3.8
conda activate AI_Functions
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

You can create a `.env` file in the project root to hide your configuration.
You probably don't need this.

```
AI_USER_NAME=YourName
AI_AGENT_NAME=AssistantName
AI_DEFAULT_MODEL=llama3.1:latest
AI_LOG_LEVEL=INFO
```

## Step 6: Run Tests

Ensure everything is set up correctly by running the test suite:

```bash
python -m unittest discover src/tests
```

## Step 7: Run the Application

```bash
python src/main.py
```

You're now ready to start developing with AI_Functions!

## Troubleshooting

- If you encounter any issues with Ollama, ensure it's running and accessible.
- For dependency issues, try updating your pip and setuptools:
  `pip install --upgrade pip setuptools`

For more help, please open an issue on the GitHub repository.
