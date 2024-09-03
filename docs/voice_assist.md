# src/docs/voice_assist_module.md

# 🎙️ Voice Assist Module

The Voice Assist Module provides voice interaction capabilities to the Ollama_Agents project.

## 🌟 Key Features

- 🗣️ Wake word detection
- 🎤 Speech-to-text conversion using Whisper models
- 🤖 Integration with Ollama for natural language processing
- 🔊 Text-to-speech output for AI responses

## 🔧 Main Components

- `VoiceAssistant`: Main class that handles voice interaction flow
- `transcribe_audio()`: Converts audio to text using Whisper models
- `prompt_ollama()`: Sends transcribed text to Ollama and processes the response
- `speak()`: Converts text responses to speech

## 🚀 Usage

The Voice Assist module is primarily used by the Voice Agent to provide a voice interface to Ollama. It can be initialized and run as follows:

```python
from src.modules.voice_assist import VoiceAssistant

assistant = VoiceAssistant(wake_word='jarvis', model_name='your_model_name')
assistant.run()
```

## 🔍 Key Considerations

- Ensure the necessary dependencies (SpeechRecognition, whisper, pyaudio) are installed
- The module uses the system's built-in text-to-speech capabilities
- Whisper models are used for speech recognition, which may require significant computational resources

## 🔮 Future Enhancements

- Add support for custom text-to-speech engines
- Implement voice activity detection to improve wake word recognition
- Add multilingual support for both speech recognition and synthesis
