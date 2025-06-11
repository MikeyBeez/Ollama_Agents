# src/modules/base_agent.py

import asyncio
from typing import Optional
from src.modules.config_manager import ConfigManager
from src.modules.logging_setup import logger
from rich.console import Console

class BaseAgent:
    def __init__(self, config: Optional[ConfigManager] = None):
        self.config = config or ConfigManager()
        self.logger = logger
        self.console = Console()

    async def run(self):
        self.console.print(f"[bold green]{self.config.AGENT_NAME} initialized. Type 'exit' to quit.[/bold green]")

        while True:
            user_input = await self.get_user_input()
            if user_input.lower() == 'exit':
                break

            response = await self.process_input(user_input)
            self.console.print(f"[bold magenta]{self.config.AGENT_NAME}:[/bold magenta] {response}")

        self.console.print(f"[bold red]{self.config.AGENT_NAME} shutting down. Goodbye![/bold red]")

    async def get_user_input(self, prompt: Optional[str] = None) -> str:
        if prompt:
            self.console.print(f"[bold cyan]{prompt}[/bold cyan]")
        user_input = await asyncio.get_event_loop().run_in_executor(None, input, f"{self.config.USER_NAME}> ")
        return user_input

    async def process_input(self, user_input: str) -> str:
        raise NotImplementedError("Subclasses must implement process_input method")

    async def add_to_history(self, user_input: str, response: str):
        # Implement this method to add the interaction to your chat history
        pass