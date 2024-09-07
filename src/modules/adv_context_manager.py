from typing import Dict, Any, List
from src.modules.ddg_search import DDGSearch
from src.modules.kb_graph import get_related_nodes

class ContextManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ddg_search = DDGSearch()

    def gather_context(self, user_input: str, analysis: Dict[str, Any]) -> str:
        context = f"User Input: {user_input}\n\nAnalysis: {analysis}\n\n"
        for topic in analysis['topics']:
            related_nodes = get_related_nodes(topic)
            if related_nodes:
                context += f"\nRelated information for {topic}:\n"
                for node, relation, strength in related_nodes:
                    context += f"- {node} ({relation}, strength: {strength})\n"
        return context

    def retrieve_knowledge(self, context: str, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        # This is a placeholder. Implement your knowledge retrieval logic here.
        return []

    def perform_web_search(self, query: str) -> List[str]:
        return self.ddg_search.run_search(query)
