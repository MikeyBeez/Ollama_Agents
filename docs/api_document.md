# Ollama_Agents API Documentation

## Overview

This document outlines the API for the Ollama_Agents framework, a system for creating and interacting with sophisticated AI agents using Ollama. The API provides programmatic access to the core functionality of the framework without needing to understand all implementation details.

## Installation and Setup

### Option 1: Install as a Package

To use Ollama_Agents in your own project, you can install it as a package:

```bash
# From the root of the Ollama_Agents repository
pip install -e .
```

This will install the package in development mode, allowing you to use it in other projects while still being able to modify the source code.

### Option 2: Add to Python Path

Alternatively, you can add the Ollama_Agents directory to your Python path:

```bash
# Add to PYTHONPATH temporarily
export PYTHONPATH="/path/to/Ollama_Agents:$PYTHONPATH"

# Or add to your shell profile for permanent access
echo 'export PYTHONPATH="/path/to/Ollama_Agents:$PYTHONPATH"' >> ~/.bashrc  # or ~/.zshrc
```

### Dependencies

Ensure all required dependencies are installed:

```bash
pip install -r /path/to/Ollama_Agents/requirements.txt
```

### Environment Configuration

1. Create a `.env` file in your project directory or copy it from the Ollama_Agents repository
2. Configure the necessary environment variables:

```
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama2:13b
EMBEDDING_MODEL=all-MiniLM-L6-v2
LOG_LEVEL=INFO
```

## Core API Classes

### AgentAPI

Central interface for creating and managing agent sessions.

```python
class AgentAPI:
    """Main API for interacting with Ollama_Agents"""
    
    def list_agents():
        """
        Return all available agent types
        
        Returns:
            dict: Dictionary of available agent types with descriptions
        """
        
    def create_session(agent_type, config=None):
        """
        Create a new agent session with optional custom config
        
        Args:
            agent_type (str): Type of agent to create (e.g., 'debug', 'research', 'memory')
            config (dict, optional): Custom configuration options
            
        Returns:
            str: Session ID for the created agent
        """
        
    def get_response(session_id, user_input):
        """
        Process user input and return agent response
        
        Args:
            session_id (str): Session identifier
            user_input (str): User's message or query
            
        Returns:
            dict: Response containing agent's reply and any metadata
        """
        
    def execute_command(session_id, command, params=None):
        """
        Execute a slash command with optional parameters
        
        Args:
            session_id (str): Session identifier
            command (str): Command name (without slash)
            params (dict, optional): Command parameters
            
        Returns:
            dict: Command execution results
        """
        
    def terminate_session(session_id):
        """
        End an agent session and clean up resources
        
        Args:
            session_id (str): Session identifier
            
        Returns:
            bool: Success status
        """
```

### KnowledgeAPI

Interface for working with the graph-based knowledge system.

```python
class KnowledgeAPI:
    """API for working with the graph knowledgebase"""
    
    def add_edge(source, target, relationship, metadata=None):
        """
        Add knowledge edge to the graph
        
        Args:
            source (str): Source node (concept)
            target (str): Target node (concept)
            relationship (str): Type of relationship
            metadata (dict, optional): Additional edge information
            
        Returns:
            str: Edge ID
        """
        
    def query_edges(node=None, relationship=None, limit=10):
        """
        Query edges from the knowledge graph
        
        Args:
            node (str, optional): Filter by node name
            relationship (str, optional): Filter by relationship type
            limit (int, optional): Maximum results to return
            
        Returns:
            list: Matching edges
        """
        
    def get_related_concepts(concept, depth=1):
        """
        Get concepts related to the given concept
        
        Args:
            concept (str): Base concept to expand from
            depth (int, optional): How many relation hops to traverse
            
        Returns:
            dict: Related concepts grouped by relationship type
        """
        
    def visualize_graph(concept=None, depth=2):
        """
        Return visualization data for the knowledge graph
        
        Args:
            concept (str, optional): Center node for visualization
            depth (int, optional): Graph depth to include
            
        Returns:
            dict: Graph visualization data
        """
        
    def generate_knowledge_tree(concept, depth=2):
        """
        Generate a hierarchical knowledge tree for a concept
        
        Args:
            concept (str): Root concept
            depth (int, optional): Tree depth
            
        Returns:
            dict: Tree structure of related knowledge
        """
        
    def extract_entities(text):
        """
        Extract named entities and concepts from text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            list: Extracted entities with types
        """
        
    def extract_relationships(text):
        """
        Extract relationships between entities from text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            list: Extracted relationship triples
        """
```

### MemoryAPI

Interface for searching and managing conversation history.

```python
class MemoryAPI:
    """API for searching and managing conversation history"""
    
    def search_history(query, limit=5, semantic=True):
        """
        Search conversation history semantically or by keywords
        
        Args:
            query (str): Search query
            limit (int, optional): Maximum results
            semantic (bool, optional): Use semantic search if True
            
        Returns:
            list: Matching conversation snippets
        """
        
    def get_conversation(conversation_id):
        """
        Retrieve a complete conversation by ID
        
        Args:
            conversation_id (str): Conversation identifier
            
        Returns:
            dict: Full conversation data
        """
        
    def save_interaction(session_id, user_input, agent_response):
        """
        Save an interaction to history
        
        Args:
            session_id (str): Session identifier
            user_input (str): User's message
            agent_response (str): Agent's response
            
        Returns:
            str: Interaction ID
        """
        
    def get_summary(conversation_id):
        """
        Generate a summary of a conversation
        
        Args:
            conversation_id (str): Conversation identifier
            
        Returns:
            str: Conversation summary
        """
        
    def extract_topics(conversation_id):
        """
        Extract main topics from a conversation
        
        Args:
            conversation_id (str): Conversation identifier
            
        Returns:
            list: Main conversation topics
        """
```

### ReasoningAPI

Interface for accessing advanced reasoning capabilities.

```python
class ReasoningAPI:
    """API for accessing reasoning and cognitive functions"""
    
    def generate_hypotheses(question, count=3):
        """
        Generate multiple hypotheses for a question
        
        Args:
            question (str): Question to generate hypotheses for
            count (int, optional): Number of hypotheses to generate
            
        Returns:
            list: Generated hypotheses
        """
        
    def apply_causal_reasoning(situation):
        """
        Apply causal reasoning to a situation
        
        Args:
            situation (str): Situation description
            
        Returns:
            dict: Cause-effect analysis
        """
        
    def generate_counterfactuals(scenario, count=3):
        """
        Generate counterfactual scenarios
        
        Args:
            scenario (str): Base scenario
            count (int, optional): Number of counterfactuals
            
        Returns:
            list: Counterfactual scenarios
        """
        
    def find_analogies(concept, domain=None, count=3):
        """
        Find analogies for a concept
        
        Args:
            concept (str): Source concept
            domain (str, optional): Target domain
            count (int, optional): Number of analogies
            
        Returns:
            list: Analogous concepts
        """
        
    def evaluate_ethical_implications(action):
        """
        Evaluate ethical implications of an action
        
        Args:
            action (str): Action description
            
        Returns:
            dict: Ethical analysis
        """
        
    def perform_arc_reasoning(grid_problem):
        """
        Apply abstract reasoning to ARC-style grid problems
        
        Args:
            grid_problem (dict): Problem definition
            
        Returns:
            dict: Solution with explanation
        """
```

### ToolsAPI

Interface for agent tools and utilities.

```python
class ToolsAPI:
    """API for agent tools and utilities"""
    
    def web_search(query, limit=3):
        """
        Perform a web search using DuckDuckGo
        
        Args:
            query (str): Search query
            limit (int, optional): Maximum results
            
        Returns:
            list: Search results with snippets
        """
        
    def fact_check(statement):
        """
        Verify a statement against knowledge sources
        
        Args:
            statement (str): Statement to verify
            
        Returns:
            dict: Verification results with confidence
        """
        
    def extract_knowledge(text):
        """
        Extract structured knowledge from text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Extracted entities and relationships
        """
        
    def analyze_sentiment(text):
        """
        Analyze sentiment of text
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Sentiment analysis results
        """
```

### VoiceAPI

Interface for voice interaction capabilities.

```python
class VoiceAPI:
    """API for voice interaction capabilities"""
    
    def initialize_voice(wake_word=None, voice_id=None):
        """
        Initialize voice capabilities
        
        Args:
            wake_word (str, optional): Custom wake word
            voice_id (str, optional): Voice ID for text-to-speech
            
        Returns:
            bool: Success status
        """
        
    def start_listening():
        """
        Start listening for voice input
        
        Returns:
            str: Session ID
        """
        
    def stop_listening(session_id):
        """
        Stop listening for voice input
        
        Args:
            session_id (str): Voice session ID
            
        Returns:
            bool: Success status
        """
        
    def text_to_speech(text, voice_id=None):
        """
        Convert text to speech
        
        Args:
            text (str): Text to convert
            voice_id (str, optional): Voice to use
            
        Returns:
            bytes: Audio data
        """
        
    def speech_to_text(audio_data):
        """
        Convert speech to text
        
        Args:
            audio_data (bytes): Audio data
            
        Returns:
            str: Transcribed text
        """
```

## Agent-Specific APIs

### ResearchAgentAPI

Specialized API for the research agent functionality.

```python
class ResearchAgentAPI(AgentAPI):
    """API for research agent functionality"""
    
    def start_research(topic, depth=2):
        """
        Start a research session on a topic
        
        Args:
            topic (str): Research topic
            depth (int, optional): Research depth
            
        Returns:
            str: Research session ID
        """
        
    def get_research_status(session_id):
        """
        Get status of a research session
        
        Args:
            session_id (str): Research session ID
            
        Returns:
            dict: Research progress
        """
        
    def generate_research_summary(session_id, format="markdown"):
        """
        Generate a summary of research findings
        
        Args:
            session_id (str): Research session ID
            format (str, optional): Output format
            
        Returns:
            str: Research summary
        """
        
    def add_research_source(session_id, source_url):
        """
        Add a source to a research session
        
        Args:
            session_id (str): Research session ID
            source_url (str): URL of source
            
        Returns:
            bool: Success status
        """
```

### DebugAgentAPI

Specialized API for debug agent functionality.

```python
class DebugAgentAPI(AgentAPI):
    """API for debug agent functionality"""
    
    def start_debug_session(code=None, error=None):
        """
        Start a debugging session
        
        Args:
            code (str, optional): Code to debug
            error (str, optional): Error message
            
        Returns:
            str: Debug session ID
        """
        
    def get_cognitive_trace(session_id):
        """
        Get cognitive trace of agent's reasoning
        
        Args:
            session_id (str): Session ID
            
        Returns:
            dict: Cognitive process visualization
        """
        
    def suggest_fixes(session_id, count=3):
        """
        Suggest code fixes
        
        Args:
            session_id (str): Debug session ID
            count (int, optional): Number of suggestions
            
        Returns:
            list: Suggested fixes
        """
```

## Usage Examples

### Creating and Using an Agent

```python
from ollama_agents.api import AgentAPI

# List available agents
agents = AgentAPI.list_agents()
print(agents)

# Create a debug agent session
session_id = AgentAPI.create_session('debug')

# Get a response
response = AgentAPI.get_response(session_id, "Explain how the knowledge graph works")
print(response['reply'])

# Execute a command
result = AgentAPI.execute_command(session_id, 'knowledge_tree', {'concept': 'AI'})
print(result)

# End session
AgentAPI.terminate_session(session_id)
```

### Working with the Knowledge Graph

```python
from ollama_agents.api import KnowledgeAPI

# Add knowledge to the graph
KnowledgeAPI.add_edge(
    source="Python", 
    target="Programming", 
    relationship="is_a", 
    metadata={"confidence": 0.95}
)

# Query related concepts
programming_languages = KnowledgeAPI.get_related_concepts("Programming")
print(programming_languages)

# Visualize a portion of the graph
graph_data = KnowledgeAPI.visualize_graph(concept="AI", depth=2)
# Then render graph_data using a visualization library
```

### Using Memory Search

```python
from ollama_agents.api import MemoryAPI

# Search for previous conversations about Python
results = MemoryAPI.search_history("Python programming tips")

# Print the results
for result in results:
    print(f"Date: {result['timestamp']}")
    print(f"User: {result['user_input']}")
    print(f"Agent: {result['agent_response']}")
    print("---")
```

### Using Research Capabilities

```python
from ollama_agents.api import ResearchAgentAPI

# Start a research session
session_id = ResearchAgentAPI.start_research("Quantum computing advancements 2023")

# Get research status
status = ResearchAgentAPI.get_research_status(session_id)
print(f"Research progress: {status['progress']}%")

# Generate a summary when complete
if status['status'] == 'complete':
    summary = ResearchAgentAPI.generate_research_summary(session_id)
    print(summary)
```

## Error Handling

All API methods will raise exceptions for errors. Common exceptions include:

- `SessionNotFoundError`: When an invalid session ID is provided
- `AgentTypeNotFoundError`: When an invalid agent type is specified
- `KnowledgeGraphError`: When operations on the knowledge graph fail
- `CommandExecutionError`: When slash commands cannot be executed
- `MemorySearchError`: When memory search operations fail

Example error handling:

```python
from ollama_agents.api import AgentAPI
from ollama_agents.exceptions import SessionNotFoundError

try:
    response = AgentAPI.get_response("invalid_session_id", "Hello")
except SessionNotFoundError:
    print("Session not found, creating a new one...")
    session_id = AgentAPI.create_session('debug')
    response = AgentAPI.get_response(session_id, "Hello")
```

## Configuration

The API can be configured using environment variables or by passing a configuration dictionary to the initialization methods:

```python
from ollama_agents.api import AgentAPI

# Configure using a dictionary
config = {
    "model": "llama2:13b",
    "temperature": 0.7,
    "system_prompt": "You are a helpful assistant..."
}

session_id = AgentAPI.create_session('research', config=config)
```

## Advanced Usage

For advanced usage patterns and integration with other systems, please refer to the framework usage documentation.

## Using the API in External Projects

Here's a complete example of how to use the Ollama_Agents API in an external project:

### Project Structure

```
Ollama_Experiments/
├── .env
├── requirements.txt
└── experiment.py
```

### Example experiment.py

```python
import os
import sys
# Add Ollama_Agents to Python path if not installed as a package
ollama_agents_path = "/path/to/Ollama_Agents"
if ollama_agents_path not in sys.path:
    sys.path.append(ollama_agents_path)

from ollama_agents.api import AgentAPI, KnowledgeAPI, MemoryAPI

def run_experiment():
    # Initialize
    print("Starting Ollama_Agents experiment...")
    
    # List available agents
    agents = AgentAPI.list_agents()
    print(f"Available agents: {agents}")
    
    # Create a session
    session_id = AgentAPI.create_session('debug', {
        "model": "llama2:13b",
        "temperature": 0.7
    })
    
    try:
        # Use the agent
        response = AgentAPI.get_response(session_id, "What is a knowledge graph?")
        print(f"Response: {response['reply']}")
        
        # Add some knowledge
        KnowledgeAPI.add_edge(
            source="Knowledge Graph", 
            target="Data Structure", 
            relationship="is_a"
        )
        
        # Execute a command
        result = AgentAPI.execute_command(session_id, 'knowledge_tree', {
            'concept': 'Knowledge Graph'
        })
        print("Knowledge tree result:", result)
        
    finally:
        # Clean up
        AgentAPI.terminate_session(session_id)
        print("Experiment complete.")

if __name__ == "__main__":
    run_experiment()
```

### Running the Experiment

1. Create a `.env` file with your configuration
2. Install dependencies: `pip install -r /path/to/Ollama_Agents/requirements.txt`
3. Run the experiment: `python experiment.py`

## Troubleshooting

### Common Issues

1. **ImportError**: Ensure Ollama_Agents is properly added to your Python path or installed as a package
2. **Module not found**: Check that all dependencies are installed
3. **Connection error**: Make sure Ollama is running locally or the OLLAMA_HOST is correctly set
4. **DB errors**: Ensure the necessary database files exist and are accessible

### Logging

Enable debug logging by setting `LOG_LEVEL=DEBUG` in your `.env` file or:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Getting Help

If you encounter issues, check:
1. The official documentation in the `/docs` directory
2. Open issues on the GitHub repository
3. Log files in the `/logs` directory