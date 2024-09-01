import unittest
from unittest.mock import patch
from src.modules.basic_commands import change_model_command, get_ollama_models

class TestBasicCommands(unittest.TestCase):
    @patch('src.modules.basic_commands.get_ollama_models')
    @patch('src.modules.basic_commands.IntPrompt.ask')
    @patch('src.modules.basic_commands.update_config_model')
    def test_change_model_command(self, mock_update_config, mock_ask, mock_get_models):
        mock_get_models.return_value = ['model1', 'model2', 'model3']
        mock_ask.return_value = 2

        result = change_model_command("/cm")
        self.assertEqual(result, 'CONTINUE')
        mock_update_config.assert_called_once_with('model2')

    @patch('subprocess.run')
    def test_get_ollama_models(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "NAME      ID    SIZE   MODIFIED\nmodel1   1234   1.2GB  1 day ago\nmodel2   5678   2.3GB  2 days ago\n"

        models = get_ollama_models()
        self.assertEqual(models, ['model1', 'model2'])

if __name__ == '__main__':
    unittest.main()
