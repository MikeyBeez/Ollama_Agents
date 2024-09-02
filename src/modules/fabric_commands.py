# src/modules/fabric_commands.py

import subprocess
from rich.console import Console
from rich.prompt import Prompt
from src.modules.save_history import save_document_chunk
from config import USER_NAME, DEFAULT_MODEL
from src.modules.logging_setup import logger
import traceback

console = Console()

def get_fabric_patterns():
    logger.info("Retrieving Fabric patterns")
    try:
        result = subprocess.run(['fabric', '--list'], capture_output=True, text=True)
        if result.returncode == 0:
            patterns = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            logger.debug(f"Retrieved {len(patterns)} Fabric patterns")
            return patterns
        else:
            error_msg = f"Error listing Fabric patterns: {result.stderr}"
            logger.error(error_msg)
            console.print(error_msg, style="bold red")
            return []
    except Exception as e:
        error_msg = f"An error occurred while getting Fabric patterns: {str(e)}"
        logger.exception(error_msg)
        console.print(error_msg, style="bold red")
        return []

def fabric_command(command: str) -> str:
    logger.info("Executing fabric command")
    patterns = get_fabric_patterns()

    if not patterns:
        logger.warning("No Fabric patterns found")
        console.print("No Fabric patterns found.", style="bold red")
        return 'CONTINUE'

    console.print("Available Fabric patterns:", style="bold blue")
    for i, pattern in enumerate(patterns, 1):
        console.print(f"{i}. {pattern}", style="cyan")

    choice = Prompt.ask("Enter the number of the pattern you want to use", default="1")
    try:
        pattern_index = int(choice) - 1
        if pattern_index < 0 or pattern_index >= len(patterns):
            raise ValueError("Invalid pattern number")
        selected_pattern = patterns[pattern_index]
        logger.info(f"Selected Fabric pattern: {selected_pattern}")
    except ValueError:
        logger.warning(f"Invalid input for pattern selection: {choice}")
        console.print("Invalid input. Please enter a valid number.", style="bold red")
        return 'CONTINUE'

    input_text = Prompt.ask("Enter the input text for the Fabric pattern")
    logger.debug(f"Input text for Fabric pattern: {input_text[:50]}...")  # Log only first 50 characters

    try:
        logger.info(f"Running Fabric command with pattern: {selected_pattern}")
        fabric_command = ['fabric', '--pattern', selected_pattern, '--stream']
        process = subprocess.Popen(fabric_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        fabric_output, fabric_error = process.communicate(input=input_text)

        if process.returncode == 0:
            logger.info("Fabric command executed successfully")
            console.print("\nFabric Output:", style="bold blue")
            console.print(fabric_output.strip(), style="bold green")

            logger.info("Saving Fabric output to chat history")
            save_document_chunk(f"Fabric_{selected_pattern}",
                                f"Pattern: {selected_pattern}\nInput: {input_text}\nOutput: {fabric_output}",
                                USER_NAME, DEFAULT_MODEL)
            console.print("\nFabric output added to chat history.", style="bold green")
        else:
            error_msg = f"Error running Fabric: {fabric_error}"
            logger.error(error_msg)
            console.print(error_msg, style="bold red")

    except Exception as e:
        error_msg = f"An error occurred while executing Fabric command: {str(e)}"
        logger.exception(error_msg)
        console.print(error_msg, style="bold red")
        logger.debug("Traceback:", exc_info=True)
        console.print("Traceback:", style="bold red")
        console.print(traceback.format_exc(), style="red")

    return 'CONTINUE'
