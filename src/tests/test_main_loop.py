# src/tests/test_main_loop.py

import sys
import os
import unittest
from unittest.mock import patch, MagicMock, call

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.main import main
from config import AGENT_NAME

class TestMainLoop(unittest.TestCase):

    @patch('src.main.get_user_input')
    @patch('src.main.process_query_and_generate_response')
    @patch('src.main.update_context')
    @patch('src.main.get_related_nodes')
    @patch('src.main.gather_context')
    @patch('src.main.chat_history.add_entry')
    @patch('src.main.console.print')
    @patch('src.main.Prompt.ask')
    def test_main_loop(self, mock_prompt_ask, mock_console_print, mock_add_entry, mock_gather_context,
                       mock_get_related_nodes, mock_update_context, mock_process_query, mock_get_user_input):
        # Set up mock behaviors
        mock_prompt_ask.side_effect = ['1', 'q']  # Select first agent, then quit
        mock_get_user_input.side_effect = ['Hello, AI!', 'exit']
        mock_process_query.return_value = {
            'response': 'AI response',
            'query_info': {'topic': 'general'},
            'bullet_points': ['Point 1', 'Point 2']
        }
        mock_update_context.return_value = 'Updated context'
        mock_get_related_nodes.return_value = [('node1', 'relation', 0.5)]
        mock_gather_context.return_value = 'Gathered context'

        # Run the main function
        main()

        # Print all calls to console.print for debugging
        print("All calls to console.print:")
        for call in mock_console_print.mock_calls:
            print(call)

        # Assertions
        mock_console_print.assert_any_call("Ollama_Agents application starting...", style="bold green")
        mock_console_print.assert_any_call(f"{AGENT_NAME}: AI response", style="bold magenta")

        # Check if functions were called with expected arguments
        mock_process_query.assert_called()
        mock_update_context.assert_called()
        mock_get_related_nodes.assert_called()
        mock_gather_context.assert_called()
        mock_add_entry.assert_called()

    @patch('src.main.get_user_input')
    @patch('src.main.process_query_and_generate_response')
    @patch('src.main.console.print')
    @patch('src.main.Prompt.ask')
    def test_error_handling(self, mock_prompt_ask, mock_console_print, mock_process_query, mock_get_user_input):
        mock_prompt_ask.side_effect = ['1', 'q']
        mock_get_user_input.side_effect = ['Hello, AI!', 'exit']
        mock_process_query.side_effect = Exception('Test error')

        # Run the main function
        main()

        # Check if error message was printed
        mock_console_print.assert_any_call("An error occurred: Test error", style="bold red")

if __name__ == '__main__':
    unittest.main()
