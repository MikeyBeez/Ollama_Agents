# src/agents/debug_agent.py

import sys
import os
from typing import Optional
from functools import wraps
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.adv_input_processor import InputProcessor
from src.modules.adv_context_manager import ContextManager
from src.modules.adv_reasoning_engine import ReasoningEngine
from src.modules.adv_planning_engine import PlanningEngine
from src.modules.adv_knowledge_manager import KnowledgeManager
from src.modules.adv_output_manager import OutputManager
from src.modules.logging_setup import logger
from src.modules.errors import OllamaAgentsError
from config import DEFAULT_MODEL, AGENT_NAME, USER_NAME

console = Console()

def debug_panel(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        console.print(Panel(f"Entering: {func_name}", border_style="green"))
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            console.print(Panel(f"Error in {func_name}: {str(e)}", border_style="red"))
            raise
        finally:
            console.print(Panel(f"Exiting: {func_name}", border_style="yellow"))
    return wrapper

class DebugAgent:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.config = {
            'DEFAULT_MODEL': model_name,
            'AGENT_NAME': AGENT_NAME,
            'USER_NAME': USER_NAME
        }
        self.input_processor = InputProcessor(self.config)
        self.context_manager = ContextManager(self.config)
        self.reasoning_engine = ReasoningEngine(model_name)
        self.planning_engine = PlanningEngine(model_name)
        self.knowledge_manager = KnowledgeManager()
        self.output_manager = OutputManager(self.config)

    @debug_panel
    def run(self):
        self.output_manager.print_welcome_message()
        self.input_processor.setup_user_profile()
        self.knowledge_manager.clear_history()

        while True:
            user_input = self._get_user_input()
            if user_input is None:
                break
            if user_input.startswith('/'):
                response = self._handle_command(user_input)
                if response is None:
                    break
            else:
                response = self._process_input(user_input)
            self.output_manager.display_response(response)

        self.output_manager.print_farewell_message()

    @debug_panel
    def _get_user_input(self) -> Optional[str]:
        return self.input_processor.get_user_input()

    @debug_panel
    def _handle_command(self, command: str) -> Optional[str]:
        return self.output_manager.execute_debug_command(command)

    @debug_panel
    def _process_input(self, user_input: str) -> str:
        try:
            analysis = self.input_processor.analyze_input(user_input)
            console.print(Panel(f"Input Analysis: {analysis}", border_style="blue"))

            context = self.context_manager.gather_context(user_input, analysis)
            console.print(Panel(f"Gathered Context: {context[:500]}...", border_style="blue"))

            knowledge = self.context_manager.retrieve_knowledge(context, analysis)
            console.print(Panel(f"Retrieved Knowledge: {knowledge}", border_style="blue"))

            if not knowledge:
                knowledge = self.context_manager.perform_web_search(user_input)
                console.print(Panel(f"Web Search Results: {knowledge}", border_style="blue"))

            causal_relationships = self.reasoning_engine.perform_causal_analysis(context)
            console.print(Panel(f"Causal Relationships: {causal_relationships}", border_style="cyan"))

            hypotheses = self.reasoning_engine.generate_hypotheses(context)
            tested_hypotheses = self.reasoning_engine.test_hypotheses(hypotheses, context)
            console.print(Panel(f"Tested Hypotheses: {tested_hypotheses}", border_style="cyan"))

            analogies = self.reasoning_engine.find_analogies(user_input, context)
            console.print(Panel(f"Found Analogies: {analogies}", border_style="cyan"))

            contradictions = self.reasoning_engine.detect_contradictions(knowledge)
            resolved_contradictions = self.reasoning_engine.resolve_contradictions(contradictions)
            console.print(Panel(f"Resolved Contradictions: {resolved_contradictions}", border_style="cyan"))

            plan = self.planning_engine.create_and_analyze_plan(
                user_input, context, knowledge, causal_relationships,
                tested_hypotheses, analogies, resolved_contradictions
            )
            console.print(Panel(f"Analyzed Plan:\n{plan}", border_style="cyan"))

            response = self.planning_engine.generate_response_from_plan(
                plan, user_input, context, knowledge, causal_relationships,
                tested_hypotheses, analogies, resolved_contradictions
            )

            progress = self.planning_engine.assess_progress(response, plan)
            console.print(Panel(f"Progress Assessment:\n{progress}", border_style="green"))

            next_step = self.planning_engine.determine_next_step(plan, progress)
            response += f"\n\nNext step: {next_step}"

            self.knowledge_manager.update_conversation_history(user_input, response)
            self.knowledge_manager.update_knowledge_graph(analysis['topics'], response)
            self.knowledge_manager.update_bullet_points(response)

            return response

        except OllamaAgentsError as e:
            logger.error(f"OllamaAgentsError in _process_input: {str(e)}")
            return f"I encountered an error while processing your request: {str(e)}"
        except Exception as e:
            logger.exception(f"Unexpected error in _process_input: {str(e)}")
            return "I apologize, but an unexpected error occurred. Please try again or contact support."

    @debug_panel
    def _display_bullet_points(self) -> str:
        return self.knowledge_manager.get_bullet_points()

    @debug_panel
    def _display_knowledge_graph(self) -> str:
        # This method needs to be implemented in KnowledgeManager
        return "Knowledge graph visualization not yet implemented."

@debug_panel
def run():
    try:
        agent = DebugAgent()
        agent.run()
    except Exception as e:
        logger.exception(f"An error occurred in DebugAgent: {str(e)}")
        console.print(f"An error occurred: {str(e)}", style="bold red")

def main():
    run()

if __name__ == "__main__":
    main()
