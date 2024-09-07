from typing import List, Dict, Any
from src.modules.ollama_client import generate_response

class ReasoningEngine:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def perform_causal_analysis(self, context: str) -> List[Dict[str, Any]]:
        prompt = f"Analyze the following context and infer potential causal relationships:\n\n{context}\n\nProvide your response as a JSON list of objects with 'cause', 'effect', 'explanation', and 'confidence' fields."
        response = generate_response(prompt, self.model_name, "CausalAnalyzer")
        return eval(response)  # In production, use json.loads() instead

    def generate_hypotheses(self, context: str) -> List[Dict[str, Any]]:
        prompt = f"Based on this context, generate plausible hypotheses:\n\n{context}\n\nProvide your response as a JSON list of objects with 'hypothesis', 'explanation', and 'likelihood' fields."
        response = generate_response(prompt, self.model_name, "HypothesisGenerator")
        return eval(response)  # In production, use json.loads() instead

    def test_hypotheses(self, hypotheses: List[Dict[str, Any]], context: str) -> List[Dict[str, Any]]:
        prompt = f"Test these hypotheses based on the given context:\n\nHypotheses: {hypotheses}\n\nContext: {context}\n\nProvide your response as a JSON list of objects with 'hypothesis', 'test_result', and 'confidence' fields."
        response = generate_response(prompt, self.model_name, "HypothesisTester")
        return eval(response)  # In production, use json.loads() instead

    def find_analogies(self, problem: str, context: str) -> List[Dict[str, str]]:
        prompt = f"Find analogies for this problem based on the given context:\n\nProblem: {problem}\n\nContext: {context}\n\nProvide your response as a JSON list of objects with 'analogy', 'explanation', and 'relevance' fields."
        response = generate_response(prompt, self.model_name, "AnalogyFinder")
        return eval(response)  # In production, use json.loads() instead

    def detect_contradictions(self, information: List[str]) -> List[Dict[str, Any]]:
        prompt = f"Detect contradictions in this information:\n\n{information}\n\nProvide your response as a JSON list of objects with 'statement1', 'statement2', and 'explanation' fields."
        response = generate_response(prompt, self.model_name, "ContradictionDetector")
        return eval(response)  # In production, use json.loads() instead

    def resolve_contradictions(self, contradictions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        prompt = f"Resolve these contradictions:\n\n{contradictions}\n\nProvide your response as a JSON list of objects with 'contradiction', 'resolution', and 'confidence' fields."
        response = generate_response(prompt, self.model_name, "ContradictionResolver")
        return eval(response)  # In production, use json.loads() instead
