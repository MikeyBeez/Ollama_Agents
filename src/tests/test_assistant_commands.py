# src/tests/test_assistant_commands.py

import unittest
from unittest.mock import patch, MagicMock
import wikipedia
import datetime
from src.modules.slash_commands import assistant_command
from src.modules.errors import CommandExecutionError
from config import DEFAULT_BROWSER, TERMINAL_APP, DEFAULT_MODEL

class TestAssistantCommand(unittest.TestCase):

    @patch('webbrowser.get')
    def test_open_reddit(self, mock_webbrowser):
        mock_browser = MagicMock()
        mock_webbrowser.return_value = mock_browser
        result = assistant_command('/assistant open reddit')
        mock_webbrowser.assert_called_once_with(DEFAULT_BROWSER)
        mock_browser.open.assert_called_once_with('https://www.reddit.com/')
        self.assertEqual(result, 'CONTINUE')

    @patch('webbrowser.get')
    def test_open_youtube(self, mock_webbrowser):
        mock_browser = MagicMock()
        mock_webbrowser.return_value = mock_browser
        result = assistant_command('/assistant open youtube')
        mock_webbrowser.assert_called_once_with(DEFAULT_BROWSER)
        mock_browser.open.assert_called_once_with('https://www.youtube.com/')
        self.assertEqual(result, 'CONTINUE')

    @patch('datetime.datetime')
    def test_time(self, mock_datetime):
        mock_now = MagicMock()
        mock_now.hour = 14
        mock_now.minute = 30
        mock_datetime.now.return_value = mock_now
        result = assistant_command('/assistant time')
        self.assertEqual(result, 'CONTINUE')

    @patch('wikipedia.summary')
    def test_look_up_success(self, mock_wiki):
        mock_wiki.return_value = "Test summary"
        result = assistant_command('/assistant look up python')
        mock_wiki.assert_called_once_with('python', sentences=2)
        self.assertEqual(result, 'CONTINUE')

    @patch('wikipedia.summary')
    def test_look_up_disambiguation(self, mock_wiki):
        mock_wiki.side_effect = wikipedia.exceptions.DisambiguationError("Python", ["Python (programming)", "Python (snake)"])
        result = assistant_command('/assistant look up python')
        self.assertEqual(result, 'CONTINUE')

    @patch('wikipedia.summary')
    def test_look_up_not_found(self, mock_wiki):
        mock_wiki.side_effect = wikipedia.exceptions.PageError("NonexistentPage")
        result = assistant_command('/assistant look up nonexistentpage')
        self.assertEqual(result, 'CONTINUE')

    @patch('pyautogui.hotkey')
    def test_maximize(self, mock_hotkey):
        result = assistant_command('/assistant maximize')
        mock_hotkey.assert_called_once_with('winleft', 'up')
        self.assertEqual(result, 'CONTINUE')

    @patch('pyautogui.hotkey')
    def test_minimize(self, mock_hotkey):
        result = assistant_command('/assistant minimize')
        mock_hotkey.assert_called_once_with('winleft', 'h')
        self.assertEqual(result, 'CONTINUE')

    @patch('subprocess.Popen')
    def test_terminal(self, mock_popen):
        result = assistant_command('/assistant terminal')
        mock_popen.assert_called_once_with(TERMINAL_APP)
        self.assertEqual(result, 'CONTINUE')

    @patch('src.modules.slash_commands.process_prompt')
    def test_unknown_command(self, mock_process_prompt):
        mock_process_prompt.return_value = "I'm not sure how to help with that."
        result = assistant_command('/assistant unknown command')
        mock_process_prompt.assert_called_once_with("Assistant command: unknown command", DEFAULT_MODEL, "User")
        self.assertEqual(result, 'CONTINUE')

    @patch('webbrowser.get')
    def test_command_execution_error(self, mock_webbrowser):
        mock_webbrowser.side_effect = Exception("Browser error")
        with self.assertRaises(CommandExecutionError):
            assistant_command('/assistant open reddit')

if __name__ == '__main__':
    unittest.main()
