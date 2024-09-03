# 🤖 Ollama_Agents: Agent Creation Guide 🚀

## 📚 Introduction

Welcome to the Ollama_Agents Agent Creation Guide! This document will walk you through the process of creating custom AI agents within the Ollama_Agents framework. Whether you're building a simple chatbot or a complex voice-enabled assistant, this guide has got you covered! 🎉

## 🌟 Types of Agents

Ollama_Agents supports various types of agents:

1. 💬 Simple Text-based Agents
2. 🔊 Voice-enabled Agents
3. 🧠 Multi-Agent Systems
4. 🔍 Research and Debate Agents

## 🛠️ Creating a Basic Text Agent

Let's start by creating a simple text-based agent. We'll call it "EchoBot" 🗣️

### Step 1: Set Up the File 📁

Create a new file in the `src/agents/` directory called `echo_bot.py`.

### Step 2: Import Necessary Modules 📦

```python
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.logging_setup import logger
from src.modules.ollama_client import process_prompt
from rich.console import Console
from config import DEFAULT_MODEL, AGENT_NAME

console = Console()
```

### Step 3: Define the Agent Class 🏗️

```python
class EchoBot:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name

    def process_input(self, user_input: str) -> str:
        prompt = f"You are {AGENT_NAME}, an AI assistant that echoes user input. User said: {user_input}"
        response = process_prompt(prompt, self.model_name, "EchoBot")
        return response
```

### Step 4: Implement the Main Loop 🔁

```python
def run():
    echo_bot = EchoBot()
    console.print("[bold green]EchoBot initialized. Type 'exit' to quit.[/bold green]")

    while True:
        user_input = console.input("[bold cyan]You: [/bold cyan]")
        if user_input.lower() == 'exit':
            break

        response = echo_bot.process_input(user_input)
        console.print(f"[bold magenta]EchoBot: [/bold magenta]{response}")

    console.print("[bold red]EchoBot shutting down. Goodbye![/bold red]")

if __name__ == "__main__":
    run()
```

### Step 5: Test Your Agent 🧪

Run your new agent:

```bash
python -m src.agents.echo_bot
```

## 🎙️ Creating a Voice-Enabled Agent

Now, let's create a voice-enabled agent called "VoiceAssistant" 🗣️🎤

### Step 1: Set Up the File 📁

Create a new file in the `src/agents/` directory called `voice_assistant.py`.

### Step 2: Import Necessary Modules 📦

```python
import asyncio
from src.modules.voice_assist import initialize, start_voice_assistant, speak, stop_voice_assistant, OllamaHandler
from src.modules.logging_setup import logger
from src.modules.save_history import chat_history
from src.modules.assemble import assemble_prompt_with_history
from config import DEFAULT_MODEL, USER_NAME, AGENT_NAME
from rich.console import Console

console = Console()
```

### Step 3: Define the VoiceAssistant Class 🏗️

```python
class VoiceAssistant:
    def __init__(self, wake_word='hey assistant', quit_phrase='goodbye assistant', model_name=DEFAULT_MODEL):
        self.wake_word = wake_word
        self.quit_phrase = quit_phrase
        self.model_name = model_name
        self.ollama_handler = OllamaHandler(model_name)
        self.running = True

    async def process_command(self, command: str):
        try:
            logger.info(f"Processing command: {command}")
            console.print(f"User: {command}", style="bold cyan")

            current_prompt = f"You are {AGENT_NAME}, a voice-enabled AI assistant. {command}"
            full_prompt = assemble_prompt_with_history(current_prompt, chat_history_only=True)

            response = await self.ollama_handler.process_command(full_prompt, self.on_token)

            chat_history.add_entry(command, response)
            logger.info(f"AI response: {response}")

            return response

        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            error_message = "Sorry, I encountered an error while processing your command."
            console.print(error_message, style="bold red")
            speak(error_message)
            return error_message

    def on_token(self, token: str):
        console.print(token, style="bold green", end="")
        # Accumulate tokens and speak when a sentence is complete

    async def run(self):
        logger.info("Initializing Voice Assistant")
        console.print("Initializing Voice Assistant...", style="bold yellow")
        initialize(self.wake_word, self.quit_phrase, self.process_command)

        console.print(f"Voice Assistant initialized. Say '{self.wake_word}' to wake me up or '{self.quit_phrase}' to quit.", style="bold green")

        try:
            await start_voice_assistant()
        except Exception as e:
            logger.error(f"Error in Voice Assistant: {str(e)}")
        finally:
            await self.shutdown()

    async def shutdown(self):
        logger.info("Shutting down Voice Assistant")
        stop_voice_assistant()
        console.print("Voice Assistant stopped.", style="bold red")
```

### Step 4: Implement the Main Function 🔁

```python
def run():
    try:
        logger.info("Starting Voice Assistant")
        assistant = VoiceAssistant(wake_word='hey assistant', quit_phrase='goodbye assistant', model_name=DEFAULT_MODEL)
        asyncio.run(assistant.run())
    except KeyboardInterrupt:
        logger.info("Voice Assistant interrupted by user")
        console.print("Voice Assistant interrupted by user.", style="bold yellow")
    except Exception as e:
        logger.exception(f"Error in Voice Assistant: {str(e)}")
        console.print(f"An error occurred in the Voice Assistant: {str(e)}", style="bold red")
        console.print("Please check the logs for more details.", style="bold yellow")

if __name__ == "__main__":
    run()
```

### Step 5: Test Your Voice Assistant 🧪

Run your new voice-enabled agent:

```bash
python -m src.agents.voice_assistant
```

## 🧠 Advanced Agent Features

### Memory Management 🗃️

To give your agent long-term memory, use the `memory_search` module:

```python
from src.modules.memory_search import search_memories

class MemoryAgent(EchoBot):
    def process_input(self, user_input: str) -> str:
        memories = search_memories(user_input, top_k=3, similarity_threshold=0.7)
        memory_context = "\n".join([m['content'] for m in memories])
        prompt = f"You are {AGENT_NAME}, an AI assistant with memories. Context: {memory_context}\nUser said: {user_input}"
        response = process_prompt(prompt, self.model_name, "MemoryAgent")
        return response
```

### Web Search Integration 🌐

Integrate web search capabilities using the `ddg_search` module:

```python
from src.modules.ddg_search import DDGSearch

class WebSearchAgent(EchoBot):
    def __init__(self, model_name=DEFAULT_MODEL):
        super().__init__(model_name)
        self.ddg_search = DDGSearch()

    def process_input(self, user_input: str) -> str:
        search_results = self.ddg_search.run_search(user_input)
        search_context = "\n".join(search_results[:3])
        prompt = f"You are {AGENT_NAME}, an AI assistant with web search capabilities. Search results: {search_context}\nUser query: {user_input}"
        response = process_prompt(prompt, self.model_name, "WebSearchAgent")
        return response
```

## 🚀 Best Practices for Agent Development

1. 📝 **Clear Documentation**: Always document your agent's purpose, capabilities, and usage instructions.
2. 🧪 **Comprehensive Testing**: Write unit tests for your agent's core functionalities.
3. 🔒 **Error Handling**: Implement robust error handling to gracefully manage unexpected situations.
4. 🎨 **User Experience**: Use rich console output to create an engaging interaction experience.
5. 🔧 **Configurability**: Allow key parameters (e.g., model, wake words) to be easily configurable.
6. 📊 **Logging**: Implement detailed logging for debugging and performance monitoring.
7. 🔄 **Continuous Improvement**: Regularly update your agent based on user feedback and new capabilities.

## 🎓 Advanced Topics

- 🧩 **Multi-Agent Systems**: Implement multiple agents that can interact with each other.
- 🔊 **Custom Voice Models**: Integrate specialized voice recognition or text-to-speech models.
- 🌍 **Multilingual Support**: Add support for multiple languages in your agents.
- 🧠 **Adaptive Learning**: Implement techniques for agents to learn and improve from interactions.

## 🏁 Conclusion

Congratulations! You now have the knowledge to create various types of agents within the Ollama_Agents framework. Remember, the key to a great agent is creativity, robust implementation, and continuous refinement based on user needs. Happy coding! 🎉👨‍💻👩‍💻
