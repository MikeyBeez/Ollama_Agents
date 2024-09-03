# src/agents/V3.py

import asyncio
from src.modules.voice_assist1 import initialize, start_voice_assistant, speak, stop_voice_assistant, OllamaHandler
from src.modules.logging_setup import logger
from config import DEFAULT_MODEL
from rich.console import Console

console = Console()

class V3Agent:
    def __init__(self, wake_word='jarvis', quit_phrase='goodbye overlord', model_name=DEFAULT_MODEL):
        self.wake_word = wake_word
        self.quit_phrase = quit_phrase
        self.model_name = model_name
        self.ollama_handler = OllamaHandler(model_name)
        self.running = True

    async def process_command(self, command: str):
        current_sentence = ""

        def on_token(token: str):
            nonlocal current_sentence
            current_sentence += token
            if token.endswith(('.', '!', '?', '\n')):
                speak(current_sentence.strip())
                current_sentence = ""

        response = await self.ollama_handler.process_command(command, on_token)

        if current_sentence.strip():
            speak(current_sentence.strip())

        # Print wake word message after response is finished
        console.print(f"\nSay '{self.wake_word}' to wake me up or '{self.quit_phrase}' to quit.", style="bold blue")

        return response

    async def run(self):
        logger.info("Initializing V3 Agent")
        console.print("Initializing V3 Agent...", style="bold yellow")
        initialize(self.wake_word, self.quit_phrase, self.process_command)

        console.print(f"V3 Agent initialized. Say '{self.wake_word}' to wake me up or '{self.quit_phrase}' to quit.", style="bold green")

        try:
            await start_voice_assistant()
        except Exception as e:
            logger.error(f"Error in V3 Agent: {str(e)}")
        finally:
            await self.shutdown()

    async def shutdown(self):
        logger.info("Shutting down V3 Agent")
        stop_voice_assistant()
        console.print("V3 Agent stopped.", style="bold red")

def run():
    try:
        logger.info("Starting V3 Agent")
        agent = V3Agent(wake_word='jarvis', quit_phrase='goodbye overlord', model_name=DEFAULT_MODEL)
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        logger.info("V3 Agent interrupted by user")
        console.print("V3 Agent interrupted by user.", style="bold yellow")
    except Exception as e:
        logger.exception(f"Error in V3 Agent: {str(e)}")
        console.print(f"An error occurred in the V3 Agent: {str(e)}", style="bold red")
        console.print("Please check the logs for more details.", style="bold yellow")

def main():
    run()

if __name__ == "__main__":
    main()
