# src/modules/voice_assist.py

import os
import sys
import speech_recognition as sr
import whisper
import warnings
import tempfile
from src.modules.logging_setup import logger

# Suppress warnings
warnings.filterwarnings("ignore", category=UserWarning)

def initialize_whisper_models():
    logger.info("Loading Whisper models...")
    tiny_model = whisper.load_model("tiny")
    base_model = whisper.load_model("base")
    logger.info("Whisper models loaded")
    return tiny_model, base_model

def listen(recognizer, source):
    try:
        logger.info("Listening for audio...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        logger.info("Audio captured")
        return audio
    except sr.WaitTimeoutError:
        logger.info("No audio detected within timeout period")
        return None

def transcribe_audio(audio, model):
    if audio is None:
        return ""
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
            temp_audio.write(audio.get_wav_data())
            temp_audio_path = temp_audio.name

        result = model.transcribe(temp_audio_path)
        os.unlink(temp_audio_path)
        return result['text']
    except Exception as e:
        logger.error(f"Error transcribing audio: {str(e)}")
        return ""

def speak(text):
    ALLOWED_CHARS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_:+-/ ')
    clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
    os.system(f"say '{clean_text}'")
    logger.info(f"Spoke: {clean_text}")
