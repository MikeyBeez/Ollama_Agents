from typing import Dict, Any
from rich.console import Console
from rich.panel import Panel
from src.modules.slash_commands import handle_slash_command

class OutputManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.console = Console()

    def format_response(self, response: str) -> str:
        # Implement any formatting logic here
        return response

    def display_response(self, response: str):
        formatted_response = self.format_response(response)
        self.console.print(f"🤖 {self.config['AGENT_NAME']}:", style="bold magenta")
        self.console.print(formatted_response)

    def handle_followup(self, context: str, process_input_func) -> str:
        # Implement follow-up question handling logic here
        pass

    def execute_debug_command(self, command: str) -> str:
        return handle_slash_command(command)

    def print_welcome_message(self):
        welcome_message = f"🚀 {self.config['AGENT_NAME']} initialized. I'm your advanced debug AI assistant. Type '/q' to quit or '/help' for commands."
        self.console.print(Panel(welcome_message, style="bold green"))

    def print_farewell_message(self):
        farewell_message = f"👋 Thank you for using {self.config['AGENT_NAME']}. Your debug session has ended. Goodbye!"
        self.console.print(Panel(farewell_message, style="bold red"))
