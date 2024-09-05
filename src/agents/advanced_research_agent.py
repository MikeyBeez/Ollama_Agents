# src/agents/advanced_research_agent.py

import sys
import os
import json
from typing import List, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.logging_setup import logger
from src.modules.ddg_search import DDGSearch
from src.modules.save_history import chat_history
from src.modules.input import get_user_input
from src.modules.ollama_client import process_prompt
from src.modules.memory_search import search_memories
from config import DEFAULT_MODEL, AGENT_NAME, USER_NAME

console = Console()
ddg_search = DDGSearch()

class AdvancedResearchAgent:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
        self.context = ""
        self.conversation_history = []
        self.bullet_points = []

    def run(self):
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

    def get_user_input(self) -> str:
        return get_user_input()

    def handle_command(self, command: str) -> str:
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

    def process_input(self, user_input: str) -> str:
        try:
            logger.info(f"Processing user input: {user_input[:50]}...")

            # Topic modeling
            topic = self.classify_topic(user_input)
            console.print(f"📊 Identified topic: {topic}")

            # Query analysis
            query_analysis = self.analyze_query(user_input)
            console.print(Markdown("📝 Query analysis:"))
            for key, value in query_analysis.items():
                console.print(f"  - {key}: {value}")

            # Gather context
            self.context = self.gather_context(user_input, topic)

            # Conduct research
            research_results = self.conduct_research(user_input, query_analysis)
            self.context += f"\nResearch Results:\n{research_results}"

            # Generate initial response
            initial_response = self.generate_response(user_input, self.context, query_analysis)

            # Self-evaluation
            evaluation = self.self_evaluate(user_input, initial_response)
            if evaluation['needs_clarification']:
                clarification = self.request_clarification(evaluation['questions'])
                user_input += f"\nAdditional context: {clarification}"
                return self.process_input(user_input)  # Recursive call with updated input
            else:
                response = initial_response

            # Update bullet points
            self.update_bullet_points(response)

            # Format response
            formatted_response = self.format_response(response, query_analysis['response_type'])

            # Update conversation history
            self.conversation_history.append((user_input, formatted_response))
            chat_history.add_entry(user_input, formatted_response)

            return formatted_response

        except Exception as e:
            logger.exception(f"Unexpected error in process_input: {str(e)}")
            error_details = f"Error type: {type(e).__name__}\nError message: {str(e)}\n"
            error_details += f"Occurred in method: process_input\n"
            error_details += f"User input: {user_input}\n"
            console.print(Panel(error_details, title="Error Details", border_style="bold red"))
            return "I apologize, but an unexpected error occurred. Please check the error details above and try rephrasing your question or try a different query."

    def classify_topic(self, query: str) -> str:
        prompt = f"Classify the following query into a general topic area (1-3 words): {query}"
        return process_prompt(prompt, self.model_name, "TopicClassifier")

    def analyze_query(self, query: str) -> Dict[str, Any]:
        prompt = f"""Analyze the following query:
        "{query}"
        Provide a JSON response with the following keys:
        - intent: The user's intention (e.g., learn, solve a problem, find instructions)
        - complexity: A number from 1-5 indicating the complexity of the query
        - response_type: The type of response needed (e.g., explanation, steps, analysis)
        - key_aspects: List of key aspects or subtopics to cover
        """
        response = process_prompt(prompt, self.model_name, "QueryAnalyzer")
        try:
            # Try to find JSON content within the response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                raise ValueError("No valid JSON found in the response")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON from analyze_query: {str(e)}")
            return {
                "intent": "unknown",
                "complexity": 3,
                "response_type": "explanation",
                "key_aspects": ["error in query analysis"]
            }

    def gather_context(self, user_input: str, topic: str) -> str:
        memories = search_memories(user_input, top_k=3, similarity_threshold=0.7)
        memory_context = "\n".join([f"Related info: {m['content']}" for m in memories])

        recent_history = self.conversation_history[-3:]
        history_context = "\n".join([f"User: {h[0]}\n{AGENT_NAME}: {h[1]}" for h in recent_history])

        bullet_context = "\n".join(self.bullet_points)

        return f"Topic: {topic}\n\nRelevant information:\n{memory_context}\n\nRecent conversation:\n{history_context}\n\nKey points:\n{bullet_context}"

    def conduct_research(self, user_input: str, query_analysis: Dict[str, Any]) -> str:
        research_prompt = f"""Based on this query: "{user_input}"
        And this analysis: {query_analysis}
        Conduct thorough research and provide a summary of key findings.
        Focus on accurate, relevant, and helpful information.
        Address each of the key_aspects mentioned in the query analysis.
        If the query involves instructions or steps, include them.
        If multiple viewpoints exist, present them objectively.
        Limit your response to 300 words.
        """
        return process_prompt(research_prompt, self.model_name, "Researcher")

    def generate_response(self, user_input: str, context: str, query_analysis: Dict[str, Any]) -> str:
        response_prompt = f"""Given the user query: "{user_input}"
        This context: {context}
        And this query analysis: {query_analysis}

        Generate a helpful and informative response that:
        1. Directly addresses the user's query and intention
        2. Incorporates relevant research findings
        3. Provides clear explanations or instructions as needed
        4. Acknowledges any limitations or uncertainties in the information
        5. Suggests areas for further research if applicable

        Ensure the response is accurate, ethical, and helpful.
        Limit your response to 400 words.
        """
        return process_prompt(response_prompt, self.model_name, "ResponseGenerator")

    def self_evaluate(self, user_input: str, response: str) -> Dict[str, Any]:
        eval_prompt = f"""Evaluate this response to the user query:
        User query: "{user_input}"
        Response: "{response}"

        Provide a JSON with the following keys:
        - completeness: Rate from 1-5 how completely the response answers the query
        - clarity: Rate from 1-5 how clear and understandable the response is
        - accuracy: Rate from 1-5 how accurate and well-researched the response seems
        - needs_clarification: Boolean indicating if clarification from the user is needed
        - questions: List of questions to ask the user if clarification is needed
        """
        eval_response = process_prompt(eval_prompt, self.model_name, "SelfEvaluator")
        try:
            # Try to find JSON content within the response
            json_start = eval_response.find('{')
            json_end = eval_response.rfind('}') + 1
            if json_start != -1 and json_end != -1:
                json_str = eval_response[json_start:json_end]
                return json.loads(json_str)
            else:
                raise ValueError("No valid JSON found in the response")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON from self_evaluate: {str(e)}")
            return {
                "completeness": 3,
                "clarity": 3,
                "accuracy": 3,
                "needs_clarification": False,
                "questions": []
            }

    def request_clarification(self, questions: List[str]) -> str:
        console.print(Panel("🤔 I need some clarification to better assist you:", border_style="bold yellow"))
        for i, question in enumerate(questions, 1):
            console.print(f"{i}. {question}")
        return self.get_user_input()

    def update_bullet_points(self, response: str):
        bullet_prompt = f"Extract 3-5 key points from this text as a bullet point list: {response}"
        bullets = process_prompt(bullet_prompt, self.model_name, "BulletPointExtractor")
        new_bullets = [b.strip() for b in bullets.split('\n') if b.strip()]
        self.bullet_points.extend(new_bullets)
        self.rank_bullet_points()

    def rank_bullet_points(self):
        if len(self.bullet_points) > 15:
            rank_prompt = "Rank the following bullet points by importance and relevance:\n" + "\n".join(self.bullet_points)
            ranked = process_prompt(rank_prompt, self.model_name, "BulletPointRanker")
            self.bullet_points = [b.strip() for b in ranked.split('\n') if b.strip()][:15]

    def format_response(self, response: str, response_type: str) -> str:
        format_prompt = f"Format the following response as a {response_type}, ensuring clarity and readability: {response}"
        return process_prompt(format_prompt, self.model_name, "ResponseFormatter")

    def interactive_search(self, query: str) -> str:
        results = ddg_search.run_search(query)
        console.print(Panel(f"📊 Search results for: {query}", border_style="bold blue"))
        for i, result in enumerate(results[:5], 1):
            console.print(f"{i}. {result}")
        selection = Prompt.ask("Enter the numbers of relevant results (comma-separated), or 'all', or 'none'")
        if selection.lower() == 'all':
            relevant = results[:5]
        elif selection.lower() == 'none':
            relevant = []
        else:
            indices = [int(i.strip()) - 1 for i in selection.split(',') if i.strip().isdigit()]
            relevant = [results[i] for i in indices if 0 <= i < len(results)]
        self.context += "\n" + "\n".join(relevant)
        return f"✅ Added {len(relevant)} search results to the context."

    def display_bullet_points(self) -> str:
        if not self.bullet_points:
            return "No bullet points available."
        return "📌 Current key points:\n" + "\n".join(f"• {point}" for point in self.bullet_points)

    def output_response(self, response: str):
        console.print(Panel(Markdown(response), title=f"🤖 {AGENT_NAME}", border_style="bold magenta"))

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

def run():
    try:
        agent = AdvancedResearchAgent()
        agent.run()
    except Exception as e:
        logger.exception(f"An error occurred in AdvancedResearchAgent: {str(e)}")
        console.print(f"An error occurred: {str(e)}", style="bold red")

def main():
    run()

if __name__ == "__main__":
    main()
