from typing import Dict, Any, List
from src.modules.ollama_client import generate_response

class PlanningEngine:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def create_and_analyze_plan(self, user_input: str, context: str, knowledge: List[Dict[str, Any]],
                                causal_relationships: List[Dict[str, Any]], hypotheses: List[Dict[str, Any]],
                                analogies: List[Dict[str, str]], contradictions: List[Dict[str, Any]]) -> str:
        plan_prompt = f"""
        Based on the user input: "{user_input}"
        And the following context, knowledge, causal relationships, hypotheses, analogies, and resolved contradictions:
        Context: {context}
        Knowledge: {knowledge}
        Causal Relationships: {causal_relationships}
        Hypotheses: {hypotheses}
        Analogies: {analogies}
        Resolved Contradictions: {contradictions}

        Create a structured plan with main steps, sub-steps, analysis, and progress indicators.
        Format your response as a JSON object with 'main_steps' and 'overall_progress_evaluation' fields.
        """
        return generate_response(plan_prompt, self.model_name, "PlanCreator")

    def generate_response_from_plan(self, plan: str, user_input: str, context: str, knowledge: List[Dict[str, Any]],
                                    causal_relationships: List[Dict[str, Any]], hypotheses: List[Dict[str, Any]],
                                    analogies: List[Dict[str, str]], contradictions: List[Dict[str, Any]]) -> str:
        response_prompt = f"""
        Based on this plan: {plan}
        And considering:
        User Input: {user_input}
        Context: {context}
        Knowledge: {knowledge}
        Causal Relationships: {causal_relationships}
        Hypotheses: {hypotheses}
        Analogies: {analogies}
        Resolved Contradictions: {contradictions}

        Generate a comprehensive response that addresses the user's query and follows the plan.
        """
        return generate_response(response_prompt, self.model_name, "ResponseGenerator")

    def assess_progress(self, response: str, plan: str) -> Dict[str, Any]:
        progress_prompt = f"""
        Based on this response: {response}
        And this plan: {plan}
        Evaluate the progress. Provide a brief status update and a percentage of completion (0-100%).
        Format your response as a JSON object with 'status' and 'completion_percentage' fields.
        """
        progress_response = generate_response(progress_prompt, self.model_name, "ProgressAssessor")
        return eval(progress_response)  # In production, use json.loads() instead

    def determine_next_step(self, plan: str, progress: Dict[str, Any]) -> str:
        next_step_prompt = f"""
        Based on this plan: {plan}
        And this progress: {progress}
        Determine the next immediate step to take.
        Provide a clear and concise description of the next action.
        """
        return generate_response(next_step_prompt, self.model_name, "NextStepDeterminer")
