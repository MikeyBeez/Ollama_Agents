# src/agents/voice_agent.py

import sys
import os
import asyncio
import speech_recognition as sr
import threading

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.voice_assist import initialize_whisper_models, transcribe_audio, speak
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
        self.source = sr.Microphone(sample_rate=16000)

    def callback(self, recognizer, audio):
        try:
            if self.listening_for_wake_word:
                text = transcribe_audio(audio, self.tiny_model)
                if self.wake_word.lower() in text.lower():
                    print('Wake word detected. Please speak your prompt to the AI.')
                    speak('Listening')
                    self.listening_for_wake_word = False
            else:
                text = transcribe_audio(audio, self.base_model)
                if text.strip():
                    print('User:', text)
                    asyncio.run(self.process_command(text))
                else:
                    print('Empty prompt. Please speak again.')
                    speak('Empty prompt. Please speak again.')
                    self.listening_for_wake_word = True
        except Exception as e:
            logger.error(f'Error in callback: {str(e)}')
            print(f'Error: {str(e)}')

    async def process_command(self, text):
        try:
            response = await self.ollama_client.chat(model=self.model_name, messages=[
                {
                    'role': 'user',
                    'content': text
                }
            ])
            output = response['message']['content']
            print('AI:', output)
            speak(output)
        except Exception as e:
            logger.error(f'Error processing command: {str(e)}')
            speak('Sorry, I encountered an error while processing your command.')
        finally:
            print(f'\nSay {self.wake_word} to wake me up. \n')
            self.listening_for_wake_word = True

    def run(self):
        with self.source as s:
            self.r.adjust_for_ambient_noise(s, duration=2)

        print(f'\nSay {self.wake_word} to wake me up. \n')

        stop_listening = self.r.listen_in_background(self.source, self.callback)

        try:
            while True:
                asyncio.get_event_loop().run_until_complete(asyncio.sleep(0.1))
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            stop_listening(wait_for_stop=False)

def run():
    try:
        logger.info("Starting Voice Agent")
        agent = VoiceAgent(wake_word='jarvis', model_name=DEFAULT_MODEL)
        agent.run()
    except Exception as e:
        logger.exception(f"Error in Voice Agent: {str(e)}")
        print(f"An error occurred in the Voice Agent: {str(e)}")
        print("Please check the logs for more details.")

def main():
    run()

if __name__ == "__main__":
    main()
