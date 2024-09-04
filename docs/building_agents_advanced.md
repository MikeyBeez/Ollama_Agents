# 🤖 Ollama_Agents: Agent Creation Guide 2.0 🚀

## 📚 Introduction

Welcome to the updated Ollama_Agents Agent Creation Guide! This document will walk you through the process of creating custom AI agents within the Ollama_Agents framework, now with enhanced modularity and new powerful tools. Whether you're building a simple chatbot or a complex voice-enabled assistant, this guide has got you covered! 🎉

## 🌟 Types of Agents

Ollama_Agents supports various types of agents:

1. 💬 Simple Text-based Agents
2. 🔊 Voice-enabled Agents
3. 🧠 Multi-Agent Systems
4. 🔍 Research and Debate Agents
5. 🛠️ Task-Specific Agents (NEW!)

## 🧩 New Modular Structure

We've introduced new modules to make agent creation more organized and powerful:

1. `context_management.py`: Handles context gathering and management
2. `knowledge_management.py`: Manages knowledge base and topic classification
3. `research_tools.py`: Provides tools for conducting research
4. `agent_tools.py`: Offers various utility functions for agents

Let's explore these new modules and their functions:

### 🧠 context_management.py

This module helps agents maintain and update context during conversations.

Key functions:
- `gather_context(user_input: str, topic: str, current_context: str, agent_name: str) -> str`
- `build_context(model_name: str) -> str`
- `query_response(query_type: str, context: str, model_name: str) -> str`

### 📚 knowledge_management.py

This module handles topic classification and knowledge base updates.

Key functions:
- `classify_query_topic(query: str, model_name: str) -> str`
- `determine_research_depth(query: str, model_name: str) -> int`
- `update_knowledge_base(new_info: str, topic: str, model_name: str) -> None`
- `assess_source_credibility(source: str, model_name: str) -> float`

### 🔍 research_tools.py

This module provides tools for conducting comprehensive research.

Key functions:
- `generate_search_queries(user_input: str, model_name: str) -> List[str]`
- `basic_research(input_text: str, model_name: str) -> List[str]`
- `conduct_comprehensive_research(user_input: str, topic: str, model_name: str) -> str`

### 🛠️ agent_tools.py

This module offers various utility functions for agents.

Key functions:
- `analyze_input(user_input: str, model_name: str) -> Dict[str, Any]`
- `generate_response(user_input: str, context: str, analysis: Dict[str, Any], agent_name: str, model_name: str) -> str`
- `needs_clarification(response: str) -> bool`
- `refine_response(user_input: str, initial_response: str, context: str, model_name: str) -> str`

## 🛠️ Building an Advanced Agent

Now, let's create an advanced agent using these new modules. We'll call it `AdvancedResearchAgent`.

```python
# src/agents/advanced_research_agent.py

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.logging_setup import logger
from src.modules.ddg_search import DDGSearch
from src.modules.save_history import chat_history
from src.modules.input import get_user_input
from src.modules.context_management import gather_context, build_context
from src.modules.knowledge_management import classify_query_topic, determine_research_depth, update_knowledge_base
from src.modules.research_tools import conduct_comprehensive_research
from src.modules.agent_tools import analyze_input, generate_response, needs_clarification, refine_response
from src.modules.errors import OllamaAgentsError
from config import DEFAULT_MODEL, AGENT_NAME

from rich.console import Console

console = Console()

class AdvancedResearchAgent:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
        self.ddg_search = DDGSearch()
        self.context = ""

    def run(self):
        console.print(f"[bold green]{AGENT_NAME} initialized. Type 'exit' to quit.[/bold green]")

        while True:
            user_input = get_user_input()
            if user_input.lower() == 'exit':
                break

            try:
                response = self.process_input(user_input)
                console.print(f"[bold magenta]{AGENT_NAME}:[/bold magenta] {response}")
            except OllamaAgentsError as e:
                logger.error(f"Error processing input: {str(e)}")
                console.print(f"[bold red]Error:[/bold red] {str(e)}")

        console.print(f"[bold red]{AGENT_NAME} shutting down. Goodbye![/bold red]")

    def process_input(self, user_input: str) -> str:
        analysis = analyze_input(user_input, self.model_name)
        topic = classify_query_topic(user_input, self.model_name)
        research_depth = determine_research_depth(user_input, self.model_name)

        self.context = gather_context(user_input, topic, self.context, AGENT_NAME)

        if analysis.get('requires_research', False):
            research_results = conduct_comprehensive_research(user_input, topic, self.model_name)
            self.context += f"\nResearch Results:\n{research_results}"

        response = generate_response(user_input, self.context, analysis, AGENT_NAME, self.model_name)

        if needs_clarification(response):
            clarification = self.get_clarification()
            response = refine_response(user_input, response, self.context + f"\nUser clarification: {clarification}", self.model_name)

        update_knowledge_base(response, topic, self.model_name)
        chat_history.add_entry(user_input, response)

        return response

    def get_clarification(self) -> str:
        return get_user_input("I need more information. Can you please clarify?")

def main():
    agent = AdvancedResearchAgent()
    agent.run()

if __name__ == "__main__":
    main()
```

This `AdvancedResearchAgent` demonstrates how to use the new modules to create a more powerful and flexible agent. It incorporates context management, knowledge classification, research capabilities, and dynamic response generation.

## 🎓 Best Practices for Agent Development

1. 📝 **Modular Design**: Use the new modules to keep your agent code clean and organized.
2. 🧪 **Comprehensive Testing**: Write unit tests for your agent's core functionalities, including the new module functions.
3. 🔒 **Error Handling**: Implement robust error handling using the custom error classes in `errors.py`.
4. 🎨 **User Experience**: Use rich console output to create an engaging interaction experience.
5. 🔧 **Configurability**: Allow key parameters (e.g., model, research depth) to be easily configurable.
6. 📊 **Logging**: Implement detailed logging for debugging and performance monitoring.
7. 🔄 **Continuous Improvement**: Regularly update your agent based on user feedback and new capabilities.
8. 🧠 **Context Awareness**: Leverage the `context_management` module to maintain coherent conversations.
9. 🔍 **Research Integration**: Use the `research_tools` module to enhance your agent's knowledge in real-time.
10. 📚 **Knowledge Management**: Utilize the `knowledge_management` module to classify topics and update the agent's knowledge base.

## 🏁 Conclusion

With these new modules and the `AdvancedResearchAgent` example, you now have a powerful toolkit for creating sophisticated AI agents within the Ollama_Agents framework. Remember, the key to a great agent is creativity, robust implementation, and continuous refinement based on user needs. Happy coding! 🎉👨‍💻👩‍💻
