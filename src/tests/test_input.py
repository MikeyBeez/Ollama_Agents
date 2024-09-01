import unittest
from unittest.mock import patch
from src.modules.input import get_user_input

class TestInput(unittest.TestCase):
    @patch('src.modules.input.PromptSession.prompt')
    def test_get_user_input_normal(self, mock_prompt):
        mock_prompt.return_value = "test input"
        result = get_user_input()
        self.assertEqual(result, "test input")

    @patch('src.modules.input.PromptSession.prompt')
    def test_get_user_input_exit_commands(self, mock_prompt):
        for command in ['/e', '/exit', '/q', '/quit']:
            mock_prompt.return_value = command
            result = get_user_input()
            self.assertIsNone(result)

    @patch('src.modules.input.PromptSession.prompt')
    def test_get_user_input_help_command(self, mock_prompt):
        for command in ['/h', '/help']:
            mock_prompt.return_value = command
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

if __name__ == '__main__':
    unittest.main()
