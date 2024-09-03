# src/agents/smart_agent.py

import sys
import os
from typing import List, Dict, Any
import json
from rich.console import Console
from rich.prompt import Prompt

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.logging_setup import logger
from src.modules.ollama_client import process_prompt
from src.modules.ddg_search import DDGSearch
from src.modules.memory_search import search_memories
from src.modules.save_history import chat_history
from src.modules.document_commands import upload_document
from src.modules.slash_commands import handle_slash_command
from config import DEFAULT_MODEL, AGENT_NAME, USER_NAME

console = Console()

class SmartAgent:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
        self.ddg_search = DDGSearch()
        self.context = ""

    def run(self):
        console.print(f"[bold green]{AGENT_NAME} initialized. Type 'exit' to quit or '/help' for commands.[/bold green]")
        while True:
            user_input = console.input(f"[bold cyan]{USER_NAME}: [/bold cyan]")
            if user_input.lower() == 'exit':
                break

            if user_input.startswith('/'):
                response = self.handle_command(user_input)
            else:
                response = self.process_input(user_input)

            console.print(f"[bold magenta]{AGENT_NAME}: [/bold magenta]{response}")

        console.print(f"[bold red]{AGENT_NAME} shutting down. Goodbye![/bold red]")

    def handle_command(self, command: str) -> str:
        if command == '/help':
            return """Available commands:
            /search <query>: Perform a web search
            /context: Show current context
            /clear_context: Clear the current context
            /upload: Upload a document
            /ms <n> <threshold> <query>: Search memories
            Other standard slash commands are also available."""
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

    def process_input(self, user_input: str) -> str:
        # Step 1: Analyze the input
        analysis = self.analyze_input(user_input)

        # Step 2: Retrieve relevant information
        self.gather_context(user_input, analysis)

        # Step 3: Generate initial response or question
        initial_response = self.generate_response(user_input, self.context, analysis)

        # Step 4: Determine if clarification is needed
        if self.needs_clarification(initial_response):
            clarification = self.get_clarification(initial_response)
            self.context += f"\nClarification: {clarification}"
            return self.process_input(clarification)  # Recursive call with clarification

        # Step 5: Refine the response
        final_response = self.refine_response(user_input, initial_response, self.context)

        # Step 6: Update chat history
        chat_history.add_entry(user_input, final_response)

        return final_response

    def analyze_input(self, user_input: str) -> Dict[str, Any]:
        analysis_prompt = f"""Analyze the following user input:
        "{user_input}"
        Provide a JSON output with the following fields:
        - input_type: The type of input (question, command, statement, etc.)
        - topics: Main topics or keywords
        - complexity: Low, medium, or high
        - sentiment: Positive, negative, or neutral
        - requires_search: true if web search might be helpful, false otherwise
        - requires_memory: true if searching past interactions might be helpful, false otherwise"""

        analysis_result = process_prompt(analysis_prompt, self.model_name, "Analyzer")
        try:
            return json.loads(analysis_result)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse analysis result: {analysis_result}")
            return {}

    def gather_context(self, user_input: str, analysis: Dict[str, Any]) -> None:
        # Add relevant memories
        if analysis.get('requires_memory', False):
            memories = search_memories(user_input, top_k=3, similarity_threshold=0.7)
            memory_context = "\n".join([f"Memory: {m['content']}" for m in memories])
            self.context += f"\nRelevant memories:\n{memory_context}"

        # Add web search results if not already searched
        if analysis.get('requires_search', False) and "Search results for" not in self.context:
            search_query = self.refine_search_query(user_input, analysis)
            search_results = self.ddg_search.run_search(search_query)
            filtered_results = self.filter_search_results(user_input, search_results)
            self.context += f"\nWeb search results:\n{filtered_results}"

        # Add recent chat history
        recent_history = chat_history.get_history()[-3:]  # Get last 3 interactions
        history_context = "\n".join([f"User: {h['prompt']}\n{AGENT_NAME}: {h['response']}" for h in recent_history])
        self.context += f"\nRecent conversation:\n{history_context}"

    def refine_search_query(self, user_input: str, analysis: Dict[str, Any]) -> str:
        refine_prompt = f"""Given the user query: '{user_input}'
        and this analysis: {json.dumps(analysis)}
        Generate a concise and specific web search query to find relevant information.
        Query:"""

        return process_prompt(refine_prompt, self.model_name, "QueryRefiner").strip()

    def filter_search_results(self, query: str, results: List[str]) -> str:
        result_text = "\n".join(results[:5])  # Limit to top 5 results
        filter_prompt = f"""Given the query: '{query}' and these search results:
        {result_text}

        Provide a concise summary of the most relevant information:"""

        return process_prompt(filter_prompt, self.model_name, "ResultFilter")

    def generate_response(self, user_input: str, context: str, analysis: Dict[str, Any]) -> str:
        response_prompt = f"""As {AGENT_NAME}, respond to the user's input:
        "{user_input}"

        Consider this context:
        {context}

        And this analysis:
        {json.dumps(analysis)}

        Generate a thoughtful and relevant response. If you need more information to provide a complete answer,
        ask a clarifying question instead of giving a full response:"""

        return process_prompt(response_prompt, self.model_name, "ResponseGenerator")

    def needs_clarification(self, response: str) -> bool:
        return '?' in response and len(response.split()) < 20  # Simple heuristic

    def get_clarification(self, question: str) -> str:
        return console.input(f"[bold magenta]{AGENT_NAME}: [/bold magenta]{question}\n[bold cyan]{USER_NAME}: [/bold cyan]")

    def refine_response(self, user_input: str, initial_response: str, context: str) -> str:
        refine_prompt = f"""Given the user's input: "{user_input}"
        And the initial response: "{initial_response}"
        And this context: {context}

        Refine the response to ensure it is:
        1. Directly addressing the user's input
        2. Factually accurate
        3. Coherent and well-structured
        4. Empathetic and appropriate in tone

        Refined response:"""

        return process_prompt(refine_prompt, self.model_name, "ResponseRefiner")

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
