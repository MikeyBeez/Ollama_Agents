from src.modules.logging_setup import logger
from src.modules.errors import InputError, APIConnectionError
from src.modules.ollama_client import process_prompt
from rich.console import Console
from config import DEFAULT_MODEL, AGENT_NAME

console = Console()

def main():
    logger.info(f"Starting {AGENT_NAME} agent")
    console.print(f"[bold green]Hello! I'm {AGENT_NAME}, your AI assistant.[/bold green]")

    try:
        while True:
            try:
                user_input = console.input("[bold cyan]You: [/bold cyan]")
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break

                if not user_input.strip():
                    raise InputError("Input cannot be empty")

                logger.info(f"User input: {user_input}")
                response = process_prompt(user_input, DEFAULT_MODEL, AGENT_NAME)
                logger.info(f"Agent response: {response}")

                console.print(f"[bold magenta]{AGENT_NAME}: [/bold magenta]{response}")

            except InputError as e:
                logger.warning(f"Input error: {str(e)}")
                console.print(f"Input error: {str(e)}", style="bold red")
            except APIConnectionError as e:
                logger.error(f"API error: {str(e)}")
                console.print(f"API error: {str(e)}", style="bold red")
    except KeyboardInterrupt:
        logger.info("Agent interaction interrupted by user")
    except Exception as e:
        logger.exception(f"Unexpected error in {AGENT_NAME} agent: {str(e)}")
        console.print("An unexpected error occurred. Please check the logs.", style="bold red")
    finally:
        logger.info(f"{AGENT_NAME} agent shutting down")
        console.print(f"[bold green]Goodbye! {AGENT_NAME} signing off.[/bold green]")

if __name__ == "__main__":
    main()
