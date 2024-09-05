# src/modules/config_manager.py

import os
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self):
        load_dotenv()  # Load environment variables from .env file

        self.AGENT_NAME = os.getenv("AGENT_NAME", "AdvancedResearchAgent")
        self.USER_NAME = os.getenv("USER_NAME", "User")
        self.MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.API_KEY = os.getenv("API_KEY")  # Make sure to add this to your .env file
