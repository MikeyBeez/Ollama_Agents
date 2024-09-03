# src/agents/voice_agent.py

import sys
import os
import asyncio
import speech_recognition as sr

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.voice_assist import initialize_whisper_models, listen, transcribe_audio, speak
from src.modules.logging_setup import logger
from config import DEFAULT_MODEL
from ollama import AsyncClient

class VoiceAgent:
    def __init__(self, wake_word='jarvis', model_name=DEFAULT_MODEL):
        self.wake_word = wake_word
        self.model_name = model_name
        self.ollama_client = AsyncClient()
        self.r = sr.Recognizer()
        self.tiny_model, self.base_model = initialize_whisper_models()
        self.listening_for_wake_word = True
        self.mic = sr.Microphone()

    async def process_audio(self, audio):
        if self.listening_for_wake_word:
            await self.listen_for_wake_word(audio)
        else:
            await self.process_command(audio)

    async def listen_for_wake_word(self, audio):
        text = transcribe_audio(audio, self.tiny_model)
        if self.wake_word.lower() in text.lower():
            logger.info('Wake word detected')
            print('Wake word detected. Please speak your command.')
            speak('Listening')
            self.listening_for_wake_word = False

    async def process_command(self, audio):
        text = transcribe_audio(audio, self.base_model)
        if not text.strip():
            logger.warning('Empty command received')
            speak('Sorry, I didn\'t catch that. Could you repeat?')
            self.listening_for_wake_word = True
            return

        logger.info(f'User command: {text}')
        print('User:', text)

        try:
            response = await self.ollama_client.chat(model=self.model_name, messages=[
                {
                    'role': 'user',
                    'content': text
                }
            ])
            output = response['message']['content']
            logger.info(f'Ollama response: {output}')
            print('Assistant:', output)
            speak(output)
        except Exception as e:
            logger.error(f'Error processing command: {str(e)}')
            speak('Sorry, I encountered an error while processing your command.')

        print(f'\nSay {self.wake_word} to wake me up. \n')
        self.listening_for_wake_word = True

    async def run(self):
        with self.mic as source:
            self.r.adjust_for_ambient_noise(source, duration=2)

        print(f'\nSay {self.wake_word} to wake me up. \n')

        while True:
            with self.mic as source:
                try:
                    audio = self.r.listen(source, timeout=5, phrase_time_limit=5)
                    await self.process_audio(audio)
                except sr.WaitTimeoutError:
                    if not self.listening_for_wake_word:
                        speak("Sorry, I didn't hear anything. Please try again.")
                        self.listening_for_wake_word = True
                except Exception as e:
                    logger.error(f"Error listening: {str(e)}")
                    speak("I'm having trouble listening. Please try again.")
            await asyncio.sleep(0.1)

def run():
    try:
        logger.info("Starting Voice Agent")
        agent = VoiceAgent(wake_word='jarvis', model_name=DEFAULT_MODEL)
        asyncio.run(agent.run())
    except Exception as e:
        logger.exception(f"Error in Voice Agent: {str(e)}")
        print(f"An error occurred in the Voice Agent: {str(e)}")
        print("Please check the logs for more details.")

def main():
    run()

if __name__ == "__main__":
    main()
