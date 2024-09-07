# 🚀 Building Advanced AI Agents with Ollama_Agents

## 🌟 Introduction

This guide will walk you through the process of building sophisticated AI agents using the advanced modules provided by Ollama_Agents. These modules offer a higher level of abstraction, making it easier to create, maintain, and extend complex AI systems.

## 🧩 Advanced Modules Overview

Ollama_Agents provides six core advanced modules:

1. 🎤 `adv_input_processor.py`: Handles user input analysis and goal setting.
2. 🧠 `adv_context_manager.py`: Manages context gathering and knowledge retrieval.
3. 🤔 `adv_reasoning_engine.py`: Performs complex reasoning tasks like causal analysis and hypothesis generation.
4. 📝 `adv_planning_engine.py`: Creates and executes plans based on gathered information.
5. 📚 `adv_knowledge_manager.py`: Manages conversation history, knowledge graphs, and bullet points.
6. 💬 `adv_output_manager.py`: Handles response formatting and user interaction.

## 🛠️ Tutorial: Building an Advanced Agent

Let's walk through the process of creating an advanced AI agent using these modules.

### Step 1: Set Up Your Environment 🌿

Ensure you have Ollama_Agents installed and your PYTHONPATH set up correctly.

```bash
export PYTHONPATH=/path/to/your/Ollama_Agents:$PYTHONPATH
```

### Step 2: Create Your Agent Class 🤖

Create a new file called `advanced_agent.py` in the `src/agents/` directory:

```python
# src/agents/advanced_agent.py

from src.modules.adv_input_processor import InputProcessor
from src.modules.adv_context_manager import ContextManager
from src.modules.adv_reasoning_engine import ReasoningEngine
from src.modules.adv_planning_engine import PlanningEngine
from src.modules.adv_knowledge_manager import KnowledgeManager
from src.modules.adv_output_manager import OutputManager
from config import DEFAULT_MODEL, AGENT_NAME, USER_NAME

class AdvancedAgent:
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

    def run(self):
        self.output_manager.print_welcome_message()
        self.input_processor.setup_user_profile()

        while True:
            user_input = self.input_processor.get_user_input()
            if user_input is None:
                break
            if user_input.startswith('/'):
                response = self.output_manager.execute_debug_command(user_input)
                if response is None:
                    break
            else:
                response = self._process_input(user_input)
            self.output_manager.display_response(response)

        self.output_manager.print_farewell_message()

    def _process_input(self, user_input: str) -> str:
        analysis = self.input_processor.analyze_input(user_input)
        context = self.context_manager.gather_context(user_input, analysis)
        knowledge = self.context_manager.retrieve_knowledge(context, analysis)

        causal_relationships = self.reasoning_engine.perform_causal_analysis(context)
        hypotheses = self.reasoning_engine.generate_hypotheses(context)
        tested_hypotheses = self.reasoning_engine.test_hypotheses(hypotheses, context)
        analogies = self.reasoning_engine.find_analogies(user_input, context)
        contradictions = self.reasoning_engine.detect_contradictions(knowledge)
        resolved_contradictions = self.reasoning_engine.resolve_contradictions(contradictions)

        plan = self.planning_engine.create_and_analyze_plan(
            user_input, context, knowledge, causal_relationships,
            tested_hypotheses, analogies, resolved_contradictions
        )
        response = self.planning_engine.generate_response_from_plan(
            plan, user_input, context, knowledge, causal_relationships,
            tested_hypotheses, analogies, resolved_contradictions
        )

        progress = self.planning_engine.assess_progress(response, plan)
        next_step = self.planning_engine.determine_next_step(plan, progress)
        response += f"\n\nNext step: {next_step}"

        self.knowledge_manager.update_conversation_history(user_input, response)
        self.knowledge_manager.update_knowledge_graph(analysis['topics'], response)
        self.knowledge_manager.update_bullet_points(response)

        return response

def main():
    agent = AdvancedAgent()
    agent.run()

if __name__ == "__main__":
    main()
```

### Step 3: Customize Your Agent 🎨

You can customize your agent by modifying the behavior of individual modules. For example, to change how the agent analyzes input, you would modify the `analyze_input` method in `adv_input_processor.py`.

### Step 4: Run Your Agent 🏃‍♂️

Run your advanced agent using:

```bash
python -m src.agents.advanced_agent
```

## 📚 Reference Guide

### 🎤 InputProcessor

- `get_user_input()`: Prompts the user for input.
- `analyze_input(user_input)`: Analyzes the user's input for type, topics, complexity, etc.
- `set_current_goal(user_input)`: Determines the current goal based on user input.
- `setup_user_profile()`: Initializes the user's profile with preferences and expertise level.

### 🧠 ContextManager

- `gather_context(user_input, analysis)`: Gathers relevant context based on user input and analysis.
- `retrieve_knowledge(context, analysis)`: Retrieves relevant knowledge based on the context and analysis.
- `perform_web_search(query)`: Performs a web search for additional information.

### 🤔 ReasoningEngine

- `perform_causal_analysis(context)`: Analyzes causal relationships in the given context.
- `generate_hypotheses(context)`: Generates plausible hypotheses based on the context.
- `test_hypotheses(hypotheses, context)`: Tests generated hypotheses against the context.
- `find_analogies(problem, context)`: Finds analogies to explain complex concepts.
- `detect_contradictions(information)`: Identifies contradictions in the given information.
- `resolve_contradictions(contradictions)`: Attempts to resolve identified contradictions.

### 📝 PlanningEngine

- `create_and_analyze_plan(...)`: Creates a structured plan based on all available information.
- `generate_response_from_plan(...)`: Generates a response based on the created plan.
- `assess_progress(response, plan)`: Evaluates progress towards the goal.
- `determine_next_step(plan, progress)`: Determines the next action to take.

### 📚 KnowledgeManager

- `update_conversation_history(user_input, response)`: Updates the conversation history.
- `update_knowledge_graph(topics, response)`: Updates the knowledge graph with new information.
- `update_bullet_points(response)`: Updates the list of key points.
- `clear_history()`: Clears the conversation history and bullet points.
- `get_bullet_points()`: Retrieves the current list of bullet points.
- `get_conversation_history()`: Retrieves the conversation history.

### 💬 OutputManager

- `format_response(response)`: Formats the agent's response for display.
- `display_response(response)`: Displays the formatted response to the user.
- `handle_followup(context, process_input_func)`: Handles follow-up questions.
- `execute_debug_command(command)`: Executes debug commands (e.g., /help, /context).
- `print_welcome_message()`: Displays a welcome message when the agent starts.
- `print_farewell_message()`: Displays a farewell message when the agent exits.

## 🌟 Best Practices

1. 🧩 **Modular Design**: Keep each module focused on its specific responsibility. If a module starts to become too complex, consider breaking it down further.

2. 🛡️ **Error Handling**: Implement robust error handling in each module to prevent crashes and provide informative error messages.

3. ⚙️ **Configuration**: Use the config dictionary to store and pass around global settings and preferences.

4. 🧪 **Testing**: Write unit tests for each module to ensure they work correctly in isolation and integration tests to verify they work together as expected.

5. 📝 **Documentation**: Keep your code well-documented, especially the public methods of each module.

6. 🔧 **Extensibility**: Design your modules with extensibility in mind. Use inheritance and interfaces where appropriate to allow for easy customization and extension.

## 🎉 Conclusion

By using these advanced modules, you can create sophisticated AI agents with complex reasoning capabilities, efficient knowledge management, and dynamic planning abilities. This modular approach allows for easier maintenance, testing, and extension of your AI systems.

Remember, the key to building great AI agents is iterative development and continuous refinement. Start with a basic implementation using these modules, test thoroughly, gather feedback, and gradually enhance your agent's capabilities.

Happy coding, and may your AI agents be ever insightful and helpful! 🚀🤖💡
