# src/agents/smart_agent.py

import sys
import os
from typing import List, Dict, Any
from rich.console import Console
from rich.prompt import Confirm

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.logging_setup import logger
from src.modules.ddg_search import DDGSearch
from src.modules.save_history import chat_history
from src.modules.document_commands import upload_document
from src.modules.slash_commands import handle_slash_command
from src.modules.input import get_user_input
from src.modules.knowledge_management import classify_query_topic, determine_research_depth, update_knowledge_base
from src.modules.context_management import gather_context
from src.modules.query_processing import process_user_input, evaluate, format_response, process_user_feedback
from src.modules.research_tools import conduct_comprehensive_research
from src.modules.ollama_client import process_prompt
from src.modules.errors import OllamaAgentsError, InputError, LogicProcessingError
from src.modules.voice_assist import speak
from config import DEFAULT_MODEL, AGENT_NAME, USER_NAME

console = Console()

class SmartAgent:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
        self.ddg_search = DDGSearch()
        self.context = ""
        self.conversation_history = []
        self.speech_enabled = False

    def run(self):
        console.print(f"[bold green]{AGENT_NAME} initialized. Type '/q' to quit or '/help' for commands.[/bold green]")

        clear_history = Confirm.ask("Do you want to clear the chat history before starting?")
        if clear_history:
            chat_history.clear()
            self.conversation_history.clear()
            console.print("[bold green]Chat history cleared.[/bold green]")

        self.speech_enabled = Confirm.ask("Do you want me to speak all output?")
        if self.speech_enabled:
            console.print("[bold green]Speech enabled. I will speak all output.[/bold green]")
        else:
            console.print("[bold yellow]Speech disabled. I will only display text output.[/bold yellow]")

        while True:
            user_input = self.get_user_input()
            if user_input is None or user_input.lower() in ['/q', '/quit', '/exit']:
                break
            if user_input.startswith('/'):
                response = self.handle_command(user_input)
            else:
                response = self.process_input(user_input)
            self.output_response(response)

        console.print(f"[bold red]{AGENT_NAME} shutting down. Goodbye![/bold red]")

    def get_user_input(self) -> str:
        while True:
            user_input = get_user_input()
            if user_input is None:
                return None
            if user_input.strip() == "":
                console.print("[bold yellow]Please enter a question or command. Type '/help' for available commands or '/q' to quit.[/bold yellow]")
            else:
                return user_input

    def handle_command(self, command: str) -> str:
        try:
            if command == '/help':
                return self.get_help()
            elif command.startswith('/search '):
                query = command[8:]
                results = self.ddg_search.run_search(query)
                self.context += f"\nSearch results for '{query}':\n" + "\n".join(results[:3])
                return f"Search completed. Results added to context."
            elif command == '/context':
                return f"Current context:\n{self.context}"
            elif command == '/clear_context':
                self.context = ""
                return "Context cleared."
            elif command == '/upload':
                return upload_document(command)
            else:
                return handle_slash_command(command)
        except OllamaAgentsError as e:
            logger.error(f"Error handling command: {str(e)}")
            return f"Error: {str(e)}"

    def process_input(self, user_input: str) -> str:
        try:
            logger.info(f"Processing user input: {user_input[:50]}...")

            processed_input = process_user_input(user_input)
            topic = classify_query_topic(processed_input, self.model_name)
            research_depth = determine_research_depth(processed_input, self.model_name)

            self.context = gather_context(processed_input, topic, self.context, AGENT_NAME)

            research_results = conduct_comprehensive_research(processed_input, topic, self.model_name)
            self.context += f"\nResearch Results:\n{research_results}"

            if "how to" in processed_input.lower() or "steps to" in processed_input.lower():
                how_to_instructions = self.find_how_to_instructions(processed_input)
                self.context += f"\nHow-to Instructions:\n{how_to_instructions}"

            if "cost" in processed_input.lower() or "price" in processed_input.lower() or "expensive" in processed_input.lower():
                cost_analysis = self.analyze_costs(processed_input)
                self.context += f"\nCost Analysis:\n{cost_analysis}"

            response = evaluate(processed_input, self.context, self.model_name)

            formatted_response = format_response(response, "concise summary", self.model_name)

            update_knowledge_base(formatted_response, topic, self.model_name)

            console.print("[bold cyan]Was this response helpful? (yes/no)[/bold cyan]")
            user_feedback = console.input("[bold green]Your feedback: [/bold green]").lower()
            if user_feedback != 'yes':
                improved_response = process_user_feedback(user_feedback, formatted_response, self.model_name)
                formatted_response = improved_response

            self.conversation_history.append((user_input, formatted_response))
            chat_history.add_entry(user_input, formatted_response)

            return formatted_response

        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return "I'm sorry, but an unexpected error occurred. Please try again or rephrase your question."

    def find_how_to_instructions(self, query: str) -> str:
        try:
            search_query = f"how to {query}"
            search_results = self.ddg_search.run_search(search_query)

            instruction_prompt = f"""Based on the following search results, provide a clear and concise set of instructions for: {query}

            Search Results:
            {' '.join(search_results[:3])}

            Please format the instructions as a numbered list, with each step on a new line.
            """

            instructions = process_prompt(instruction_prompt, self.model_name, "InstructionGenerator")
            return instructions
        except Exception as e:
            logger.error(f"Error finding how-to instructions: {str(e)}")
            return f"Error: Unable to find how-to instructions for {query}"

    def analyze_costs(self, query: str) -> str:
        try:
            search_query = f"cost analysis {query}"
            search_results = self.ddg_search.run_search(search_query)

            cost_analysis_prompt = f"""Based on the following search results, provide a detailed cost analysis for: {query}

            Search Results:
            {' '.join(search_results[:3])}

            Please include:
            1. Estimated price range
            2. Factors affecting the cost
            3. Potential hidden or additional costs
            4. Cost-saving tips (if applicable)
            """

            cost_analysis = process_prompt(cost_analysis_prompt, self.model_name, "CostAnalyzer")
            return cost_analysis
        except Exception as e:
            logger.error(f"Error analyzing costs: {str(e)}")
            return f"Error: Unable to perform cost analysis for {query}"

    def output_response(self, response: str):
        console.print(f"[bold magenta]{AGENT_NAME}: [/bold magenta]{response}")
        if self.speech_enabled:
            speak(response)

    def get_help(self) -> str:
        return """
        Available commands:
        /help - Show this help message
        /search <query> - Perform a web search
        /context - Show current context
        /clear_context - Clear the current context
        /upload - Upload a document
        Other standard slash commands are also available.
        """

def run():
    try:
        agent = SmartAgent()
        agent.run()
    except Exception as e:
        logger.exception(f"An error occurred in SmartAgent: {str(e)}")
        console.print(f"An error occurred: {str(e)}", style="bold red")

def main():
    run()

if __name__ == "__main__":
    main()
