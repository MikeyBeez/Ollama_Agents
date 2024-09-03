# src/modules/voice_assist.py

import os
import asyncio
import speech_recognition as sr
import whisper
import warnings
from typing import Callable, Coroutine
from src.modules.logging_setup import logger
from rich.console import Console
from rich.live import Live
from rich.text import Text
from ollama import AsyncClient
from config import DEFAULT_MODEL

# Suppress specific warnings
warnings.filterwarnings("ignore", category=UserWarning, module="whisper")
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

console = Console()

class OllamaHandler:
    def __init__(self, model_name=DEFAULT_MODEL):
        self.model_name = model_name
        self.ollama_client = AsyncClient()

    async def process_command(self, command: str, on_token: Callable[[str], None]):
        try:
            logger.info(f"Processing command: {command}")
            console.print(f"User: {command}", style="bold cyan")

            with Live(Text("Processing...", style="bold yellow"), refresh_per_second=4) as live:
                full_response = ""
                async for chunk in await self.ollama_client.chat(model=self.model_name, messages=[
                    {
                        'role': 'user',
                        'content': command
                    }
                ], stream=True):
                    content = chunk['message']['content']
                    full_response += content
                    live.update(Text(full_response, style="bold green"))
                    on_token(content)
                    await asyncio.sleep(0.01)  # Small delay for smooth output

            logger.info(f"AI response: {full_response}")
            return full_response

        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            console.print("Sorry, I encountered an error while processing your command.", style="bold red")
            return "Error processing command."

class VoiceAssistant:
    def __init__(self, wake_word: str, quit_phrase: str, on_command: Callable[[str], Coroutine]):
        self.wake_word = wake_word.lower()
        self.quit_phrase = quit_phrase.lower()
        self.on_command = on_command
        self.r = sr.Recognizer()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.tiny_model = whisper.load_model("tiny")
            self.base_model = whisper.load_model("base")
        self.listening_for_wake_word = True
        self.source = sr.Microphone(sample_rate=16000)
        self.running = True

    async def start(self):
        logger.info("Starting Voice Assistant")
        console.print(f"Voice Assistant started. Say '{self.wake_word}' to wake me up or '{self.quit_phrase}' to quit.", style="bold green")

        with self.source as s:
            self.r.adjust_for_ambient_noise(s, duration=2)

        while self.running:
            try:
                audio = await self.listen()
                if self.listening_for_wake_word:
                    await self._process_wake_word(audio)
                else:
                    await self._process_command(audio)
            except Exception as e:
                logger.error(f"Error in main loop: {e}")

    async def listen(self):
        with self.source as s:
            audio = self.r.listen(s, phrase_time_limit=5)
        return audio

    async def _process_wake_word(self, audio):
        try:
            text = await self._transcribe(audio, self.tiny_model)
            logger.info(f"Detected: {text}")
            if self.wake_word in text.lower():
                logger.info("Wake word detected")
                console.print("Wake word detected. Listening...", style="bold blue")
                self.listening_for_wake_word = False
            elif self.quit_phrase in text.lower():
                logger.info("Quit phrase detected")
                console.print("Quit phrase detected. Shutting down...", style="bold red")
                self.running = False
        except Exception as e:
            logger.error(f"Error processing wake word: {e}")

    async def _process_command(self, audio):
        try:
            command = await self._transcribe(audio, self.base_model)
            if command.strip():
                logger.info(f"Command received: {command}")
                await self.on_command(command)
            else:
                console.print("I didn't catch that. Please try again.", style="bold yellow")
            self.listening_for_wake_word = True
        except Exception as e:
            logger.error(f"Error processing command: {e}")
            self.listening_for_wake_word = True

    async def _transcribe(self, audio, model):
        with open('audio.wav', 'wb') as f:
            f.write(audio.get_wav_data())
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = model.transcribe('audio.wav')
        return result['text']

    def stop(self):
        self.running = False

def speak(text: str):
    ALLOWED_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNSTUVWXYZ0123456789.,?!-_$:+-/ ')
    clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
    os.system(f"say '{clean_text}'")

# Global voice assistant instance
voice_assistant = None

def initialize(wake_word: str, quit_phrase: str, on_command: Callable[[str], Coroutine]):
    global voice_assistant
    voice_assistant = VoiceAssistant(wake_word, quit_phrase, on_command)

async def start_voice_assistant():
    if voice_assistant:
        await voice_assistant.start()
    else:
        logger.error("Voice assistant not initialized")

async def listen():
    if voice_assistant:
        return await voice_assistant.listen()
    else:
        logger.error("Voice assistant not initialized")
        return None

def stop_voice_assistant():
    if voice_assistant:
        voice_assistant.stop()
    else:
        logger.error("Voice assistant not initialized")
