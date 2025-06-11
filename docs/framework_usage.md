# Ollama Agents Framework Usage Guide

## Overview
The Ollama agents framework provides a way to communicate with the Mistral model through Ollama. This guide explains the key components and how to use them.

## Key Components

### OllamaClient
Main client for communicating with Ollama:
```python
from src.modules.ollama_client import OllamaClient, generate_response

# Simple usage
response = generate_response(prompt, "mistral", username)

# Or using the client directly
client = OllamaClient(base_url="http://localhost:11434")
response = client.process_prompt(prompt, "mistral", username)
```

### ReasoningEngine
Higher-level interface for structured interactions:
```python
from src.modules.adv_reasoning_engine import ReasoningEngine

engine = ReasoningEngine("mistral")

# Generate hypotheses
hypotheses = engine.generate_hypotheses(context)

# Analyze cause/effect
analysis = engine.perform_causal_analysis(context)

# Find analogies
analogies = engine.find_analogies(problem, context)
```

## Best Practices

1. Use `generate_response` for simple queries
2. Use ReasoningEngine for structured analysis
3. Format prompts clearly:
   ```python
   prompt = f"""Analyze this context and infer potential relationships:
   
   Context: {context}
   
   Provide your response as a JSON list with 'relationship' and 'confidence' fields."""
   ```

## Important Notes

1. Responses are streamed by default
2. All interactions are logged
3. Error handling is built in
4. Default timeout is 60 seconds

## Common Patterns

### Basic Query
```python
response = generate_response(
    "Analyze this pattern: 1,2,3,?",
    "mistral",
    "pattern_analysis"
)
```

### Structured Analysis
```python
engine = ReasoningEngine("mistral")
hypothesis = engine.generate_hypotheses(
    "Given sequence 1,2,3,?, predict next value"
)
```

### Error Handling
```python
try:
    response = generate_response(prompt, "mistral", username)
except Exception as e:
    logger.error(f"Error: {str(e)}")
```

## Configuration

- Default URL: http://localhost:11434
- Default timeout: 60 seconds
- Default model: mistral
- Logging enabled by default

## Tips

1. Keep prompts clear and structured
2. Use JSON response formats when possible
3. Remember responses are streamed
4. Check logs for debugging