# src/tests/test_voice_assist.py

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import speech_recognition as sr
import tempfile

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.modules.voice_assist import initialize_whisper_models, listen, transcribe_audio, speak

class TestVoiceAssist(unittest.TestCase):

    @patch('whisper.load_model')
    def test_initialize_whisper_models(self, mock_load_model):
        mock_tiny_model = MagicMock()
        mock_base_model = MagicMock()
        mock_load_model.side_effect = [mock_tiny_model, mock_base_model]

        tiny_model, base_model = initialize_whisper_models()

        self.assertEqual(mock_load_model.call_count, 2)
        mock_load_model.assert_any_call("tiny")
        mock_load_model.assert_any_call("base")
        self.assertEqual(tiny_model, mock_tiny_model)
        self.assertEqual(base_model, mock_base_model)

    @patch('speech_recognition.Recognizer.listen')
    def test_listen(self, mock_listen):
        mock_recognizer = MagicMock()
        mock_source = MagicMock()
        mock_audio = MagicMock()
        mock_listen.return_value = mock_audio

        result = listen(mock_recognizer, mock_source)

        mock_listen.assert_called_once_with(mock_source, timeout=5, phrase_time_limit=5)
        self.assertEqual(result, mock_audio)

    @patch('speech_recognition.Recognizer.listen')
    def test_listen_timeout(self, mock_listen):
        mock_recognizer = MagicMock()
        mock_source = MagicMock()
        mock_listen.side_effect = sr.WaitTimeoutError("listening timed out")

        result = listen(mock_recognizer, mock_source)

        mock_listen.assert_called_once_with(mock_source, timeout=5, phrase_time_limit=5)
        self.assertIsNone(result)

    @patch('tempfile.NamedTemporaryFile')
    @patch('os.unlink')
    def test_transcribe_audio(self, mock_unlink, mock_temp_file):
        mock_audio = MagicMock()
        mock_audio.get_wav_data.return_value = b'fake_audio_data'
        mock_model = MagicMock()
        mock_model.transcribe.return_value = {'text': 'Test transcription'}

        mock_temp_file_instance = MagicMock()
        mock_temp_file_instance.name = '/tmp/fake_audio.wav'
        mock_temp_file.return_value.__enter__.return_value = mock_temp_file_instance

        result = transcribe_audio(mock_audio, mock_model)

        mock_temp_file.assert_called_once_with(suffix=".wav", delete=False)
        mock_temp_file_instance.write.assert_called_once_with(b'fake_audio_data')
        mock_model.transcribe.assert_called_once_with('/tmp/fake_audio.wav')
        mock_unlink.assert_called_once_with('/tmp/fake_audio.wav')
        self.assertEqual(result, 'Test transcription')

    def test_transcribe_audio_none(self):
        mock_model = MagicMock()

        result = transcribe_audio(None, mock_model)

        mock_model.transcribe.assert_not_called()
        self.assertEqual(result, '')

    @patch('os.system')
    def test_speak(self, mock_system):
        test_text = "Hello, world! Test 123."
        speak(test_text)

        mock_system.assert_called_once_with("say 'Hello, world! Test 123.'")

    @patch('os.system')
    def test_speak_with_special_characters(self, mock_system):
        test_text = "Hello, world! Test 123. @#$%^&*"
        speak(test_text)

        mock_system.assert_called_once_with("say 'Hello, world! Test 123. '")

if __name__ == '__main__':
    unittest.main()
