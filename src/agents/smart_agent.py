# src/agents/smart_agent.py

import sys
import os
from typing import List, Dict, Any
import json
from rich.console import Console
from rich.prompt import Confirm

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.logging_setup import logger
from src.modules.ollama_client import process_prompt
from src.modules.ddg_search import DDGSearch
from src.modules.memory_search import search_memories
from src.modules.save_history import chat_history
from src.modules.document_commands import upload_document
from src.modules.slash_commands import handle_slash_command
from src.modules.input import get_user_input
from config import DEFAULT_MODEL, AGENT_NAME, USER_NAME

console = Console()

class SmartAgent:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
        self.ddg_search = DDGSearch()
        self.context = ""

    def run(self):
        console.print(f"[bold green]{AGENT_NAME} initialized. Type '/q' to quit or '/help' for commands.[/bold green]")
        while True:
            if not self.context:
                clear_history = Confirm.ask("Do you want to clear the chat history before asking your question?")
                if clear_history:
                    chat_history.clear()
                    console.print("[bold green]Chat history cleared.[/bold green]")

            user_input = get_user_input()

            if user_input is None:
                break
            elif user_input == 'CONTINUE':
                continue
            elif user_input.startswith('/'):
                response = self.handle_command(user_input)
            else:
                response = self.process_input(user_input)

            console.print(f"[bold magenta]{AGENT_NAME}: [/bold magenta]{response}")

        console.print(f"[bold red]{AGENT_NAME} shutting down. Goodbye![/bold red]")

    def handle_command(self, command: str) -> str:
        if command == '/help':
            return """Available commands:
            /q, /quit, /exit: Exit the SmartAgent
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
        analysis = self.analyze_input(user_input)
        self.gather_context(user_input, analysis)

        research_results = self.conduct_research(user_input, analysis)
        self.context += f"\nResearch Results:\n{research_results}"

        initial_response = self.generate_response(user_input, self.context, analysis)

        if self.needs_clarification(initial_response):
            clarification = get_user_input()
            if clarification is None or clarification == 'CONTINUE':
                return "Clarification not provided. Please try asking your question again."
            self.context += f"\nClarification: {clarification}"
            return self.process_input(clarification)

        final_response = self.refine_response(user_input, initial_response, self.context)
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
        if analysis.get('requires_memory', False):
            memories = search_memories(user_input, top_k=3, similarity_threshold=0.7)
            memory_context = "\n".join([f"Memory: {m['content']}" for m in memories])
            self.context += f"\nRelevant memories:\n{memory_context}"

        if analysis.get('requires_search', False) and "Search results for" not in self.context:
            search_query = self.refine_search_query(user_input, analysis)
            search_results = self.ddg_search.run_search(search_query)
            filtered_results = self.filter_search_results(user_input, search_results)
            self.context += f"\nWeb search results:\n{filtered_results}"

        recent_history = chat_history.get_history()[-3:]
        history_context = "\n".join([f"User: {h['prompt']}\n{AGENT_NAME}: {h['response']}" for h in recent_history])
        self.context += f"\nRecent conversation:\n{history_context}"

    def conduct_research(self, user_input: str, analysis: Dict[str, Any]) -> str:
        research_prompt = f"""Conduct comprehensive research on the topic: "{user_input}"
        Consider the following aspects:
        1. Latest developments and breakthroughs
        2. Scientific studies and clinical trials
        3. Expert opinions and consensus
        4. Potential risks and benefits
        5. Alternative approaches or treatments

        Provide a concise summary of your findings:"""

        research_results = process_prompt(research_prompt, self.model_name, "Researcher")

        if analysis.get('requires_search', False):
            search_results = self.ddg_search.run_search(user_input)
            filtered_results = self.filter_search_results(user_input, search_results)
            research_results += f"\n\nWeb Search Results:\n{filtered_results}"

        return research_results

    def refine_search_query(self, user_input: str, analysis: Dict[str, Any]) -> str:
        refine_prompt = f"""Given the user query: '{user_input}'
        and this analysis: {json.dumps(analysis)}
        Generate a concise and specific web search query to find relevant information.
        Query:"""

        return process_prompt(refine_prompt, self.model_name, "QueryRefiner").strip()

    def filter_search_results(self, query: str, results: List[str]) -> str:
        result_text = "\n".join(results[:5])
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

        Generate a comprehensive and informative response that:
        1. Directly addresses the user's query
        2. Incorporates relevant research findings
        3. Provides clear explanations and examples
        4. Offers practical advice or next steps
        5. Acknowledges any limitations or uncertainties

        If you need more information to provide a complete answer, ask a clarifying question instead of giving a full response:"""

        return process_prompt(response_prompt, self.model_name, "ResponseGenerator")

    def needs_clarification(self, response: str) -> bool:
        return '?' in response and len(response.split()) < 20

    def refine_response(self, user_input: str, initial_response: str, context: str) -> str:
        refine_prompt = f"""Given the user's input: "{user_input}"
        And the initial response: "{initial_response}"
        And this context: {context}

        Refine the response to ensure it is:
        1. Comprehensive and informative
        2. Directly addressing the user's input
        3. Factually accurate and up-to-date
        4. Coherent and well-structured
        5. Empathetic and appropriate in tone
        6. Not repetitive

        Provide only the refined response, without repeating the original input or initial response:"""

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
