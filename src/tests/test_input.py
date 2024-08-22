# src/tests/test_input.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import unittest
from unittest.mock import patch
import sys
from src.modules.input import get_user_input, get_help


class TestInput(unittest.TestCase):

    @patch('src.modules.input.PromptSession.prompt')
    def test_get_user_input_normal(self, mock_prompt):
        mock_prompt.return_value = "test input"
        result = get_user_input()
        self.assertEqual(result, "test input")

    @patch('src.modules.input.PromptSession.prompt')
    def test_get_user_input_exit(self, mock_prompt):
        for exit_command in ['/e', '/exit', '/q', '/quit']:
            mock_prompt.return_value = exit_command
            result = get_user_input()
            self.assertIsNone(result)

    @patch('src.modules.input.PromptSession.prompt')
    def test_get_user_input_help(self, mock_prompt):
        for help_command in ['/h', '/help']:
            mock_prompt.return_value = help_command
            result = get_user_input()
            self.assertEqual(result, 'CONTINUE')

    @patch('src.modules.input.PromptSession.prompt')
    def test_get_user_input_keyboard_interrupt(self, mock_prompt):
        mock_prompt.side_effect = KeyboardInterrupt()
        result = get_user_input()
        self.assertIsNone(result)

    @patch('src.modules.input.PromptSession.prompt')
    def test_get_user_input_eof(self, mock_prompt):
        mock_prompt.side_effect = EOFError()
        result = get_user_input()
        self.assertIsNone(result)

    def test_get_help(self):
        help_text = get_help()
        self.assertIn('/h or /help', help_text)
        self.assertIn('/e or /exit', help_text)
        self.assertIn('/q or /quit', help_text)

if __name__ == '__main__':
    unittest.main()
