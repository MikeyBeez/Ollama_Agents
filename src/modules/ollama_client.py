# src/modules/ollama_client.py

import requests
import json
import asyncio
import nest_asyncio
from typing import Callable, Dict, Any
from rich.console import Console
from rich.live import Live
from rich.text import Text
from .save_history import save_interaction
from .logging_setup import logger

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

class OllamaClient:
    def __init__(self, base_url="http://localhost:11434", timeout=60):
        self.base_url = base_url
        self.timeout = timeout
        self.console = Console()

    def process_prompt(self, prompt: str, model: str, username: str) -> str:
        logger.info(f"Processing prompt for user: {username}, model: {model}")
        url = f"{self.base_url}/api/generate"
        headers = {"Content-Type": "application/json"}
        data = {"model": model, "prompt": prompt}

        try:
            with Live(Text("Processing...", style="yellow bold"), refresh_per_second=4) as live:
                full_response = self._stream_response(url, headers, data, live)

            logger.info(f"Response generated for prompt: {prompt[:50]}...")
            save_interaction(prompt, full_response.strip(), username, model)
            return full_response.strip()

        except requests.Timeout:
            error_msg = f"Error: Request timed out after {self.timeout} seconds"
            logger.error(error_msg)
            self.console.print(error_msg, style="bold red")
            return error_msg
        except requests.RequestException as e:
            error_msg = f"Error connecting to Ollama: {str(e)}"
            logger.error(error_msg)
            self.console.print(error_msg, style="bold red")
            return error_msg
        except json.JSONDecodeError as e:
            error_msg = f"Error decoding JSON response: {str(e)}"
            logger.error(error_msg)
            self.console.print(error_msg, style="bold red")
            return error_msg
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg)
            self.console.print(error_msg, style="bold red")
            return error_msg

    def _stream_response(self, url: str, headers: Dict[str, str], data: Dict[str, Any], live: Live) -> str:
        full_response = ""
        with requests.post(url, headers=headers, json=data, stream=True, timeout=self.timeout) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        json_response = json.loads(line)
                        if "response" in json_response:
                            chunk = json_response["response"]
                            full_response += chunk
                            live.update(Text(full_response, style="yellow bold"))
                        if json_response.get("done", False):
                            break
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to decode JSON from line: {line}")
                        continue
        return full_response

default_client = OllamaClient()

def process_prompt(prompt: str, model: str, username: str) -> str:
    return default_client.process_prompt(prompt, model, username)

generate_response = process_prompt

__all__ = ['OllamaClient', 'process_prompt', 'generate_response']
