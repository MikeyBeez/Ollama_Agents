# test_chat_agent.py

import sys
import os
from pathlib import Path

# Add the project root to the Python path if needed
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

print("Python path:")
for path in sys.path:
    print(path)

try:
    from ollama_agents_knowledge.kb_graph import create_edge, get_related_nodes
    from ollama_agents_knowledge.knowledge_extraction import extract_knowledge
    from ollama_agents_knowledge.memory_search import search_memories
    print("Successfully imported from ollama_agents_knowledge")
except ImportError as e:
    print(f"Error importing from ollama_agents_knowledge: {e}")
    print("Falling back to local modules")
    from src.modules.kb_graph import create_edge, get_related_nodes
    from src.modules.knowledge_extraction import extract_knowledge
    from src.modules.memory_search import search_memories

from src.modules.ollama_client import process_prompt
from config import DEFAULT_MODEL

class SimpleChatAgent:
    def __init__(self):
        self.model = DEFAULT_MODEL
        self.context = ""

    def run(self):
        print("Simple Chat Agent initialized. Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break

            response = self.process_input(user_input)
            print(f"Agent: {response}")

    def process_input(self, user_input: str) -> str:
        # Extract knowledge from input
        knowledge = extract_knowledge(user_input)
        print(f"Extracted knowledge: {knowledge}")

        # Search for relevant memories
        memories = search_memories(user_input, top_k=2)
        print(f"Relevant memories: {memories}")

        # Update knowledge graph
        create_edge("user_input", user_input, "CONTAINS", 1.0)
        related = get_related_nodes("user_input")
        print(f"Related nodes: {related}")

        # Generate response using Ollama
        prompt = f"Given the following information:\nUser input: {user_input}\nExtracted knowledge: {knowledge}\nRelevant memories: {memories}\nRelated nodes: {related}\n\nGenerate a response:"
        response = process_prompt(prompt, self.model, "SimpleChatAgent")

        return response

def main():
    agent = SimpleChatAgent()
    agent.run()

if __name__ == "__main__":
    main()
