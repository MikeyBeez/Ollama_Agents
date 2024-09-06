# src/agents/debug_agent.py

import sys
import os
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Confirm

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.logging_setup import logger
from src.modules.ddg_search import DDGSearch
from src.modules.save_history import chat_history
from src.modules.input import get_user_input
from src.modules.cognitive_engine import process_query_and_generate_response
from src.modules.meta_processes import debug_panel, print_step, print_result, print_error
from src.modules.errors import ModelInferenceError, DataProcessingError, InputError
from config import DEFAULT_MODEL, AGENT_NAME, USER_NAME

console = Console()

class DebugAgent:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
        self.context = ""
        self.conversation_history = []
        self.bullet_points = []
        self.ddg_search = DDGSearch()

    @debug_panel
    def run(self):
        print_result("Agent Initialization", f"🚀 {AGENT_NAME} initialized. I'm your advanced research assistant. Type '/q' to quit or '/help' for commands.")

        clear_history = Confirm.ask("Do you want to clear the chat history before starting?")
        if clear_history:
            chat_history.clear()
            self.conversation_history.clear()
            print_result("History Cleared", "🧹 Chat history cleared.")

        while True:
            user_input = self.get_user_input()
            if user_input is None or user_input.lower() in ['/q', '/quit', '/exit']:
                break
            if user_input.startswith('/'):
                response = self.handle_command(user_input)
            else:
                response = self.process_input(user_input)
            self.output_response(response)

        print_result("Session End", f"👋 Thank you for using {AGENT_NAME}. Your research journey ends here. Goodbye!")

    @debug_panel
    def get_user_input(self) -> Optional[str]:
        return get_user_input()

    @debug_panel
    def handle_command(self, command: str) -> str:
        print_step(f"Handling command: {command}")
        if command == '/help':
            return self.get_help()
        elif command.startswith('/search '):
            return self.interactive_search(command[8:])
        elif command == '/context':
            return f"📚 Current context:\n{self.context}"
        elif command == '/clear_context':
            self.context = ""
            self.bullet_points = []
            return "🧹 Context and bullet points cleared."
        elif command == '/bullets':
            return self.display_bullet_points()
        else:
            return f"❓ Unknown command: {command}. Type '/help' for available commands."

    @debug_panel
    def process_input(self, user_input: str) -> str:
        try:
            print_step("Starting cognitive processing")

            result = process_query_and_generate_response(user_input, self.model_name, self.context, self.conversation_history, self.bullet_points, AGENT_NAME)

            if 'error' in result:
                print_error(result['response'])
                return result['response']

            self.context = result['context']
            self.bullet_points = result['bullet_points']

            print_result("Input Analysis", result['input_analysis'])
            print_result("Query Info", f"Topic: {result['query_info']['topic']} (confidence: {result['query_info']['confidence']:.2f})\nResearch depth: {result['query_info']['depth']}/5")
            print_result("Credibility", f"{result['credibility']:.2f}/1.00")
            print_result("Key Concepts", ", ".join(result['key_concepts']))
            print_result("Topic Summary", result['topic_summary'])

            self.conversation_history.append((user_input, result['response']))
            chat_history.add_entry(user_input, result['response'])

            # Handle follow-up questions
            follow_up_questions = result.get('follow_up_questions', [])
            if follow_up_questions:
                print_result("Follow-up Questions", "\n".join(f"{i+1}. {q}" for i, q in enumerate(follow_up_questions)))
                choice = console.input("Select a follow-up question (number) or press Enter to skip: ")
                if choice.isdigit() and 1 <= int(choice) <= len(follow_up_questions):
                    follow_up = follow_up_questions[int(choice) - 1]
                    print_result("Selected Follow-up", follow_up)
                    return self.process_input(follow_up)

            return result['response']

        except Exception as e:
            logger.exception(f"Unexpected error in cognitive processing: {str(e)}")
            print_error(f"Unexpected error: {str(e)}")
            return "😰 I apologize, but an unexpected error occurred. Please try rephrasing your question or try a different query."

    @debug_panel
    def interactive_search(self, query: str) -> str:
        print_step(f"Performing interactive search for: {query}")
        results = self.ddg_search.run_search(query)
        print_result("Search Results", "\n".join([f"{i+1}. {result}" for i, result in enumerate(results[:5])]))

        selection = console.input("Enter the numbers of relevant results (comma-separated), or 'all', or 'none': ")
        if selection.lower() == 'all':
            relevant = results[:5]
        elif selection.lower() == 'none':
            relevant = []
        else:
            indices = [int(i.strip()) - 1 for i in selection.split(',') if i.strip().isdigit()]
            relevant = [results[i] for i in indices if 0 <= i < len(results)]

        self.context = self.update_context(self.context, "\n".join(relevant))
        return f"✅ Added {len(relevant)} search results to the context."

    @debug_panel
    def display_bullet_points(self) -> str:
        if not self.bullet_points:
            return "No bullet points available."
        return "📌 Current key points:\n" + "\n".join(f"• {point}" for point in self.bullet_points)

    @debug_panel
    def output_response(self, response: str):
        print_result(f"🤖 {AGENT_NAME}", Markdown(response))

    @debug_panel
    def get_help(self) -> str:
        return """
        📚 Available commands:
        /help - Show this help message
        /search <query> - Perform an interactive web search
        /context - Show current context
        /clear_context - Clear the current context and bullet points
        /bullets - Display current bullet points
        /q or /quit or /exit - Exit the program

        For any other input, I'll conduct research and provide informative responses.
        """

    @debug_panel
    def update_context(self, current_context: str, new_info: str) -> str:
        # This is a placeholder for context updating logic
        # In a real implementation, this might involve more sophisticated processing
        return current_context + "\n" + new_info

@debug_panel
def run():
    try:
        agent = DebugAgent()
        agent.run()
    except Exception as e:
        logger.exception(f"An error occurred in DebugAgent: {str(e)}")
        print_error(f"An error occurred: {str(e)}")

@debug_panel
def main():
    run()

if __name__ == "__main__":
    main()
