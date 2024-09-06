# src/agents/smart_agent.py

import sys
import os
import json
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Confirm, Prompt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.logging_setup import logger
from src.modules.ddg_search import DDGSearch
from src.modules.save_history import chat_history
from src.modules.input import get_user_input
from src.modules.cognitive_engine import process_query_and_generate_response
from src.modules.meta_processes import debug_panel, print_step, print_result, print_error
from src.modules.errors import ModelInferenceError, DataProcessingError, InputError
from src.modules.agent_tools import (
    analyze_user_input,
    generate_response,
    update_bullet_points,
    interactive_followup,
    generate_search_queries,
    summarize_search_results,
    evaluate_response,
    generate_examples,
    explain_concept,
    generate_analogies,
    fact_check
)
from src.modules.knowledge_management import (
    classify_query_topic,
    determine_research_depth,
    process_query,
    assess_source_credibility,
    update_knowledge_base,
    extract_key_concepts,
    generate_follow_up_questions,
    summarize_topic,
    identify_knowledge_gaps,
    compare_information,
    validate_information,
    generate_knowledge_tree,
    evaluate_knowledge_consistency
)
from src.modules.context_management import (
    gather_context,
    update_context,
    extract_key_information,
    summarize_context,
    identify_context_gaps,
    prioritize_context,
    merge_contexts,
    filter_context,
    expand_context,
    generate_context_metadata,
    adapt_context_to_user
)
from config import DEFAULT_MODEL, AGENT_NAME, USER_NAME

console = Console()

class SmartAgent:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
        self.context = ""
        self.conversation_history = []
        self.bullet_points = []
        self.ddg_search = DDGSearch()
        self.knowledge_tree = {}
        self.user_profile = {"expertise_level": "medium", "interests": [], "language_preference": "English"}

    @debug_panel
    def run(self):
        print_result("Agent Initialization", f"🚀 {AGENT_NAME} initialized. I'm your advanced AI assistant. Type '/q' to quit or '/help' for commands.")

        clear_history = Confirm.ask("Do you want to clear the chat history before starting?")
        if clear_history:
            chat_history.clear()
            self.conversation_history.clear()
            print_result("History Cleared", "🧹 Chat history cleared.")

        self._setup_user_profile()

        while True:
            user_input = self.get_user_input()
            if user_input is None or user_input.lower() in ['/q', '/quit', '/exit']:
                break
            if user_input.startswith('/'):
                response = self.handle_command(user_input)
            else:
                response = self.process_input(user_input)
            self.output_response(response)

        print_result("Session End", f"👋 Thank you for using {AGENT_NAME}. Your session has ended. Goodbye!")

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
        elif command == '/knowledge_tree':
            return self.display_knowledge_tree()
        elif command.startswith('/explain '):
            return self.explain_concept_command(command[9:])
        elif command.startswith('/fact_check '):
            return self.fact_check_command(command[12:])
        elif command == '/profile':
            return self.display_user_profile()
        else:
            return f"❓ Unknown command: {command}. Type '/help' for available commands."

    @debug_panel
    def process_input(self, user_input: str) -> str:
        try:
            print_step("Starting cognitive processing")

            input_analysis = analyze_user_input(user_input, self.model_name)
            query_info = process_query(user_input, self.model_name)

            self.context = gather_context(user_input, query_info['topic'], self.conversation_history, self.bullet_points, AGENT_NAME)
            self.context = adapt_context_to_user(self.context, self.user_profile, self.model_name)

            research_depth = query_info['depth']
            if research_depth > 1:
                search_queries = generate_search_queries(user_input, self.model_name)
                search_results = [self.ddg_search.run_search(query) for query in search_queries]
                summarized_results = summarize_search_results(sum(search_results, []), self.model_name)
                self.context = update_context(self.context, summarized_results, self.model_name)

            response = generate_response(user_input, self.context, input_analysis, AGENT_NAME, self.model_name)

            credibility = assess_source_credibility(response, self.model_name)
            update_knowledge_base(response, query_info['topic'], self.model_name)

            new_bullets = update_bullet_points(response, self.model_name)
            self.bullet_points.extend(new_bullets)

            key_concepts = extract_key_concepts(response, self.model_name)
            self.update_knowledge_tree(query_info['topic'], key_concepts)

            topic_summary = summarize_topic(query_info['topic'], self.context, self.model_name)

            self.conversation_history.append({"prompt": user_input, "response": response})
            chat_history.add_entry(user_input, response)

            print_result("Input Analysis", input_analysis)
            print_result("Query Info", f"Topic: {query_info['topic']} (confidence: {query_info['confidence']:.2f})\nResearch depth: {research_depth}/5")
            print_result("Credibility", f"{credibility:.2f}/1.00")
            print_result("Key Concepts", ", ".join(key_concepts))
            print_result("Topic Summary", topic_summary)

            followup = self.handle_followup(self.context)
            if followup:
                response += f"\n\n{followup}"

            return response

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

        self.context = update_context(self.context, "\n".join(relevant), self.model_name)
        return f"✅ Added {len(relevant)} search results to the context."

    @debug_panel
    def display_bullet_points(self) -> str:
        if not self.bullet_points:
            return "No bullet points available."
        return "📌 Current key points:\n" + "\n".join(f"• {point}" for point in self.bullet_points)

    @debug_panel
    def display_knowledge_tree(self) -> str:
        if not self.knowledge_tree:
            return "Knowledge tree is empty."
        return "🌳 Knowledge Tree:\n" + json.dumps(self.knowledge_tree, indent=2)

    @debug_panel
    def explain_concept_command(self, concept: str) -> str:
        explanation = explain_concept(concept, self.model_name, self.user_profile['expertise_level'])
        analogies = generate_analogies(concept, self.model_name)
        examples = generate_examples(concept, self.model_name)

        response = f"Explanation of '{concept}':\n\n{explanation}\n\n"
        response += "Analogies:\n" + "\n".join(f"• {analogy}" for analogy in analogies) + "\n\n"
        response += "Examples:\n" + "\n".join(f"• {example}" for example in examples)

        return response

    @debug_panel
    def fact_check_command(self, statement: str) -> str:
        result = fact_check(statement, self.model_name)
        response = f"Fact check for: '{statement}'\n\n"
        response += f"Factual: {'Yes' if result['is_factual'] else 'No'}\n"
        response += f"Confidence: {result['confidence']:.2f}\n"
        response += f"Explanation: {result['explanation']}\n"
        if result['sources']:
            response += "Sources:\n" + "\n".join(f"• {source}" for source in result['sources'])
        return response

    @debug_panel
    def display_user_profile(self) -> str:
        return f"👤 User Profile:\n{json.dumps(self.user_profile, indent=2)}"

    @debug_panel
    def output_response(self, response: str):
        print_result(f"🤖 {AGENT_NAME}", response)

    @debug_panel
    def get_help(self) -> str:
        return """
        📚 Available commands:
        /help - Show this help message
        /search <query> - Perform an interactive web search
        /context - Show current context
        /clear_context - Clear the current context and bullet points
        /bullets - Display current bullet points
        /knowledge_tree - Display the knowledge tree
        /explain <concept> - Get an explanation of a concept
        /fact_check <statement> - Perform a fact check on a statement
        /profile - Display your user profile
        /q or /quit or /exit - Exit the program

        For any other input, I'll conduct research and provide informative responses.
        """

    def update_knowledge_tree(self, topic: str, concepts: List[str]):
        if topic not in self.knowledge_tree:
            self.knowledge_tree[topic] = set()
        self.knowledge_tree[topic].update(concepts)

    def handle_followup(self, context: str) -> Optional[str]:
        followup_questions = generate_follow_up_questions(context, self.model_name)
        if followup_questions:
            print_result("Follow-up Questions", "\n".join(f"{i+1}. {q}" for i, q in enumerate(followup_questions)))
            choice = console.input("Select a follow-up question (number) or press Enter to skip: ")
            if choice.isdigit() and 1 <= int(choice) <= len(followup_questions):
                selected_question = followup_questions[int(choice) - 1]
                return f"Follow-up question: {selected_question}\n\n{self.process_input(selected_question)}"
        return None

    def _setup_user_profile(self):
        print_step("Setting up user profile")
        self.user_profile['expertise_level'] = Prompt.ask("What's your expertise level?", choices=['beginner', 'medium', 'expert'], default="medium")
        interests = Prompt.ask("What are your main interests? (comma-separated)")
        self.user_profile['interests'] = [interest.strip() for interest in interests.split(',')]
        self.user_profile['language_preference'] = Prompt.ask("Preferred language", default="English")
        print_result("User Profile", f"Profile set up: {self.user_profile}")

@debug_panel
def run():
    try:
        agent = SmartAgent()
        agent.run()
    except Exception as e:
        logger.exception(f"An error occurred in SmartAgent: {str(e)}")
        print_error(f"An error occurred: {str(e)}")

@debug_panel
def main():
    run()

if __name__ == "__main__":
    main()
