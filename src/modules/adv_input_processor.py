# src/modules/adv_input_processor.py

from typing import Dict, Any, Optional
from src.modules.ollama_client import generate_response
from src.modules.errors import InputError
from src.modules.input import get_user_input
from rich.prompt import Prompt
import json

class InputProcessor:
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def get_user_input(self) -> Optional[str]:
        try:
            return get_user_input()
        except KeyboardInterrupt:
            return None

    def analyze_input(self, user_input: str) -> Dict[str, Any]:
        analysis_prompt = f"""Analyze the following user input:
        "{user_input}"
        Provide your response in the following JSON format:
        {{
            "input_type": "The type of input (question, command, statement, etc.)",
            "topics": ["Main topic 1", "Main topic 2"],
            "complexity": "Low, medium, or high",
            "sentiment": "Positive, negative, or neutral",
            "requires_research": true or false
        }}
        """
        analysis_result = generate_response(analysis_prompt, self.config['DEFAULT_MODEL'], "InputAnalyzer")
        try:
            return json.loads(analysis_result)
        except json.JSONDecodeError as e:
            raise InputError(f"Failed to parse input analysis: {e}")

    def set_current_goal(self, user_input: str) -> str:
        goal_prompt = f"Based on the user input: '{user_input}', what is the main goal or objective? Provide a concise statement of the goal."
        return generate_response(goal_prompt, self.config['DEFAULT_MODEL'], self.config['USER_NAME'])

    def setup_user_profile(self):
        self.config['expertise_level'] = Prompt.ask("What's your expertise level?", choices=['beginner', 'medium', 'expert'], default="medium")
        interests = Prompt.ask("What are your main interests? (comma-separated)")
        self.config['interests'] = [interest.strip() for interest in interests.split(',')]
        self.config['language_preference'] = Prompt.ask("Preferred language", default="English")
        return self.config
