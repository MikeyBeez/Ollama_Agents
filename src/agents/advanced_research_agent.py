# src/agents/advanced_research_agent.py

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
from src.modules.knowledge_management import process_query, assess_source_credibility, update_knowledge_base, extract_key_concepts, generate_follow_up_questions, summarize_topic
from src.modules.context_management import gather_context, summarize_context, extract_key_information, update_context
from src.modules.agent_tools import update_bullet_points, rank_bullet_points, generate_response, analyze_user_input
from src.modules.research_tools import perform_research, generate_search_queries, verify_information, conduct_basic_research
from src.modules.errors import ModelInferenceError, DataProcessingError, InputError
from config import DEFAULT_MODEL, AGENT_NAME, USER_NAME

console = Console()

def print_func_name(func_name: str):
    console.print(f"[bold blue]Executing: {func_name}[/bold blue]")

class AdvancedResearchAgent:
    def __init__(self, model_name=DEFAULT_MODEL, verbose=False):
        self.model_name = model_name
        self.context = ""
        self.conversation_history = []
        self.bullet_points = []
        self.ddg_search = DDGSearch()
        self.verbose = verbose

    def run(self):
        if self.verbose:
            print_func_name("AdvancedResearchAgent.run")
        console.print(Panel(f"🚀 {AGENT_NAME} initialized. I'm your advanced research assistant. Type '/q' to quit or '/help' for commands.", title="Welcome", border_style="bold green"))

        clear_history = Confirm.ask("Do you want to clear the chat history before starting?")
        if clear_history:
            chat_history.clear()
            self.conversation_history.clear()
            console.print(Panel("🧹 Chat history cleared.", border_style="bold blue"))

        while True:
            user_input = self.get_user_input()
            if user_input is None or user_input.lower() in ['/q', '/quit', '/exit']:
                break
            if user_input.startswith('/'):
                response = self.handle_command(user_input)
            else:
                response = self.process_input(user_input)
            self.output_response(response)

        console.print(Panel(f"👋 Thank you for using {AGENT_NAME}. Your research journey ends here. Goodbye!", border_style="bold green"))

    def get_user_input(self) -> Optional[str]:
        if self.verbose:
            print_func_name("AdvancedResearchAgent.get_user_input")
        return get_user_input()

    def handle_command(self, command: str) -> str:
        if self.verbose:
            print_func_name("AdvancedResearchAgent.handle_command")
        if command == '/help':
            return self.get_help()
        elif command == '/toggle_verbose':
            self.verbose = not self.verbose
            return f"Verbose mode {'enabled' if self.verbose else 'disabled'}."
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

    def process_input(self, user_input: str) -> str:
        if self.verbose:
            print_func_name("AdvancedResearchAgent.process_input")
        try:
            console.print(Panel("🔍 Starting research process...", border_style="bold cyan"))

            if self.verbose:
                print_func_name("analyze_user_input")
            input_analysis = analyze_user_input(user_input, self.model_name)
            console.print(Markdown("📝 Input analysis:"))
            for key, value in input_analysis.items():
                console.print(f"  - {key}: {value}")

            if self.verbose:
                print_func_name("process_query")
            query_info = process_query(user_input, self.model_name)
            console.print(f"📊 Identified topic: {query_info['topic']} (confidence: {query_info['confidence']:.2f})")
            console.print(f"🔬 Research depth: {query_info['depth']}/5")

            if self.verbose:
                print_func_name("gather_context")
            self.context = gather_context(user_input, query_info['topic'], self.conversation_history, self.bullet_points, AGENT_NAME)

            if self.verbose:
                print_func_name("perform_research")
            research_results = perform_research(user_input, query_info['topic'], self.model_name)

            if self.verbose:
                print_func_name("update_context")
            self.context = update_context(self.context, research_results, self.model_name)

            if self.verbose:
                print_func_name("generate_response")
            response = generate_response(user_input, self.context, self.model_name)

            if self.verbose:
                print_func_name("assess_source_credibility")
            credibility = assess_source_credibility(response, self.model_name)
            console.print(f"📊 Response credibility: {credibility:.2f}/1.00")

            if self.verbose:
                print_func_name("update_knowledge_base")
            update_knowledge_base(response, query_info['topic'], self.model_name)

            if self.verbose:
                print_func_name("extract_key_concepts")
            key_concepts = extract_key_concepts(response, self.model_name)
            console.print(f"🔑 Key concepts: {', '.join(key_concepts)}")

            if self.verbose:
                print_func_name("generate_follow_up_questions")
            follow_up_questions = generate_follow_up_questions(self.context, self.model_name)
            console.print("❓ Follow-up questions:")
            for question in follow_up_questions:
                console.print(f"  - {question}")

            if self.verbose:
                print_func_name("update_bullet_points")
            new_bullets = update_bullet_points(response, self.model_name)
            self.bullet_points.extend(new_bullets)
            self.bullet_points = rank_bullet_points(self.bullet_points, self.model_name)

            if self.verbose:
                print_func_name("summarize_topic")
            topic_summary = summarize_topic(query_info['topic'], self.context, self.model_name)
            console.print(Panel(topic_summary, title="📌 Topic Summary", border_style="bold yellow"))

            self.conversation_history.append((user_input, response))
            chat_history.add_entry(user_input, response)

            return response

        except (ModelInferenceError, DataProcessingError, InputError) as e:
            logger.error(f"Error in process_input: {str(e)}")
            return f"😕 I apologize, but an error occurred: {str(e)}"
        except Exception as e:
            logger.exception(f"Unexpected error in process_input: {str(e)}")
            return "😰 I apologize, but an unexpected error occurred. Please try rephrasing your question or try a different query."

    def interactive_search(self, query: str) -> str:
        if self.verbose:
            print_func_name("AdvancedResearchAgent.interactive_search")
        results = self.ddg_search.run_search(query)
        console.print(Panel(f"📊 Search results for: {query}", border_style="bold blue"))
        for i, result in enumerate(results[:5], 1):
            console.print(f"{i}. {result}")
        selection = console.input("Enter the numbers of relevant results (comma-separated), or 'all', or 'none': ")
        if selection.lower() == 'all':
            relevant = results[:5]
        elif selection.lower() == 'none':
            relevant = []
        else:
            indices = [int(i.strip()) - 1 for i in selection.split(',') if i.strip().isdigit()]
            relevant = [results[i] for i in indices if 0 <= i < len(results)]
        self.context = update_context(self.context, "\n".join(relevant), self.model_name)
        return f"✅ Added {len(relevant)} search results to the context."

    def display_bullet_points(self) -> str:
        if self.verbose:
            print_func_name("AdvancedResearchAgent.display_bullet_points")
        if not self.bullet_points:
            return "No bullet points available."
        return "📌 Current key points:\n" + "\n".join(f"• {point}" for point in self.bullet_points)

    def output_response(self, response: str):
        if self.verbose:
            print_func_name("AdvancedResearchAgent.output_response")
        console.print(Panel(Markdown(response), title=f"🤖 {AGENT_NAME}", border_style="bold magenta"))

    def get_help(self) -> str:
        if self.verbose:
            print_func_name("AdvancedResearchAgent.get_help")
        return """
        📚 Available commands:
        /help - Show this help message
        /toggle_verbose - Toggle verbose mode (show/hide function calls)
        /search <query> - Perform an interactive web search
        /context - Show current context
        /clear_context - Clear the current context and bullet points
        /bullets - Display current bullet points
        /q or /quit or /exit - Exit the program

        For any other input, I'll conduct research and provide informative responses.
        """

def run():
    try:
        agent = AdvancedResearchAgent(verbose=False)  # Set initial verbose mode here
        agent.run()
    except Exception as e:
        logger.exception(f"An error occurred in AdvancedResearchAgent: {str(e)}")
        console.print(Panel(f"😱 An error occurred: {str(e)}", border_style="bold red"))

def main():
    run()

if __name__ == "__main__":
    main()
