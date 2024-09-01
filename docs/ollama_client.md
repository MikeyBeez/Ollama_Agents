# 🤖 Ollama Client

The Ollama Client module manages communication with the Ollama AI model.

## 🌟 Key Features

- 📤 Sends prompts to the Ollama API
- 📥 Processes and streams responses
- 🛡️ Handles API errors and exceptions
- 🎨 Formats responses for display

## 🔧 Main Functions

- 💬 `process_prompt(prompt, model, username)`: Sends a prompt to Ollama and returns the response

## 🚀 Usage

This module is used whenever the application needs to interact with the Ollama AI model, typically for generating responses to user queries.

## 🧪 Testing

The Ollama client is tested in `test_ollama_client.py`, covering:

- Correct processing of API responses
- Handling of different response formats
- Error handling for API failures

To run tests specific to this module:

```bash
python -m unittest src/tests/test_ollama_client.py
```

## 🔍 Key Considerations

- Keep the API interaction logic up-to-date with any changes in the Ollama API
- Consider implementing retry logic for transient failures
- Monitor and optimize performance, especially for longer conversations
