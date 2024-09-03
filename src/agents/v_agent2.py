# src/agents/v_agent2.py

import asyncio
from src.modules.voice_assist import initialize, start_voice_assistant, speak, stop_voice_assistant, OllamaHandler
from src.modules.logging_setup import logger
from src.modules.save_history import chat_history
from src.modules.assemble import assemble_prompt_with_history
from config import DEFAULT_MODEL, USER_NAME, AGENT_NAME
from rich.console import Console

console = Console()

class V2Agent:
    def __init__(self, wake_word='jarvis', quit_phrase='goodbye overlord', model_name=DEFAULT_MODEL):
        self.wake_word = wake_word
        self.quit_phrase = quit_phrase
        self.model_name = model_name
        self.ollama_handler = OllamaHandler(model_name)
        self.running = True

    async def process_command(self, command: str):
        try:
            logger.info(f"Processing command: {command}")
            console.print(f"User: {command}", style="bold cyan")

            current_prompt = f"You are {AGENT_NAME}, an AI assistant. {command}"
            full_prompt = assemble_prompt_with_history(current_prompt, chat_history_only=True)
            logger.debug(f"Full prompt (first 500 chars): {full_prompt[:500]}...")

            current_sentence = ""
            full_response = ""

            def on_token(token: str):
                nonlocal current_sentence, full_response
                current_sentence += token
                full_response += token
                if token.endswith(('.', '!', '?', '\n')):
                    console.print(current_sentence.strip(), style="bold green", end="")
                    speak(current_sentence.strip())
                    current_sentence = ""

            response = await self.ollama_handler.process_command(full_prompt, on_token)

            if current_sentence.strip():
                console.print(current_sentence.strip(), style="bold green")
                speak(current_sentence.strip())

            chat_history.add_entry(command, full_response)

            logger.info(f"AI response: {full_response}")
            console.print(f"\nSay '{self.wake_word}' to wake me up or '{self.quit_phrase}' to quit.", style="bold blue")

            return full_response

        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            console.print("Sorry, I encountered an error while processing your command.", style="bold red")
            speak("Sorry, I encountered an error while processing your command.")
            return "Error processing command."

    async def run(self):
        logger.info("Initializing V2 Agent")
        console.print("Initializing V2 Agent...", style="bold yellow")
        initialize(self.wake_word, self.quit_phrase, self.process_command)

        console.print(f"V2 Agent initialized. Say '{self.wake_word}' to wake me up or '{self.quit_phrase}' to quit.", style="bold green")

        try:
            await start_voice_assistant()
        except Exception as e:
            logger.error(f"Error in V2 Agent: {str(e)}")
        finally:
            await self.shutdown()

    async def shutdown(self):
        logger.info("Shutting down V2 Agent")
        stop_voice_assistant()
        console.print("V2 Agent stopped.", style="bold red")

def run():
    try:
        logger.info("Starting V2 Agent")
        agent = V2Agent(wake_word='jarvis', quit_phrase='goodbye overlord', model_name=DEFAULT_MODEL)
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        logger.info("V2 Agent interrupted by user")
        console.print("V2 Agent interrupted by user.", style="bold yellow")
    except Exception as e:
        logger.exception(f"Error in V2 Agent: {str(e)}")
        console.print(f"An error occurred in the V2 Agent: {str(e)}", style="bold red")
        console.print("Please check the logs for more details.", style="bold yellow")

def main():
    run()

if __name__ == "__main__":
    main()
