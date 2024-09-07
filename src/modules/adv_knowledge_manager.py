from typing import List, Dict, Any
from src.modules.save_history import chat_history
from src.modules.kb_graph import update_knowledge_graph
from rich.prompt import Confirm

class KnowledgeManager:
    def __init__(self):
        self.conversation_history = []
        self.bullet_points = []

    def update_conversation_history(self, user_input: str, response: str):
        self.conversation_history.append({"prompt": user_input, "response": response})
        if len(self.conversation_history) > 10:
            self.conversation_history.pop(0)
        chat_history.add_entry(user_input, response)

    def update_knowledge_graph(self, topics: List[str], response: str):
        for topic in topics:
            update_knowledge_graph(topic, response)

    def update_bullet_points(self, response: str):
        new_points = response.split('\n')
        self.bullet_points.extend([point.strip() for point in new_points if point.strip().startswith('•')])
        self.bullet_points = self.bullet_points[-10:]

    def clear_history(self):
        if Confirm.ask("Do you want to clear the chat history?"):
            chat_history.clear()
            self.conversation_history.clear()
            self.bullet_points.clear()
            return "Chat history and bullet points cleared."
        return "Clear history operation cancelled."

    def get_bullet_points(self) -> str:
        if not self.bullet_points:
            return "No bullet points available."
        return "📌 Current key points:\n" + "\n".join(f"• {point}" for point in self.bullet_points)

    def get_conversation_history(self) -> List[Dict[str, str]]:
        return self.conversation_history
