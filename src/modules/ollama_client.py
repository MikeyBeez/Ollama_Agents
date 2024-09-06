# src/modules/ollama_client.py

import requests
import json
from rich.console import Console
from rich.live import Live
from rich.text import Text
from .save_history import save_interaction
from .logging_setup import logger

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434"):
        self.base_url = base_url
        self.console = Console()

    def process_prompt(self, prompt: str, model: str, username: str):
        logger.info(f"Processing prompt for user: {username}, model: {model}")
        url = f"{self.base_url}/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {"model": model, "prompt": prompt}

        try:
            with requests.post(url, headers=headers, json=data, stream=True) as response:
                if response.status_code == 200:
                    full_response = ""
                    with Live(Text("", style="yellow bold"), refresh_per_second=4) as live:
                        for line in response.iter_lines():
                            if line:
                                json_response = json.loads(line)
                                if "response" in json_response:
                                    chunk = json_response["response"]
                                    full_response += chunk
                                    live.update(Text(full_response, style="yellow bold"))
                                if json_response.get("done", False):
                                    break

                    logger.info(f"Response generated for prompt: {prompt[:50]}...")
                    save_interaction(prompt, full_response.strip(), username, model)

                    return full_response.strip()
                else:
                    error_msg = f"Error: Received status code {response.status_code}"
                    logger.error(error_msg)
                    self.console.print(error_msg, style="bold red")
                    return error_msg
        except requests.RequestException as e:
            error_msg = f"Error connecting to Ollama: {e}"
            logger.error(error_msg)
            self.console.print(error_msg, style="bold red")
            return error_msg

default_client = OllamaClient()

def process_prompt(prompt: str, model: str, username: str):
    return default_client.process_prompt(prompt, model, username)

# Add this line to create an alias for process_prompt
generate_response = process_prompt

# Ensure all necessary functions are available for import
__all__ = ['OllamaClient', 'process_prompt', 'generate_response']
