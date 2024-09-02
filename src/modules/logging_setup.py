# src/modules/logging_setup.py

import logging
import sys
from pathlib import Path
from config import LOG_LEVEL, LOG_FILE

def setup_logging():
    try:
        # Ensure the log file directory exists
        log_file_path = Path(LOG_FILE)
        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        # Create a logger for our application
        logger = logging.getLogger("ollama_agents")
        logger.setLevel(LOG_LEVEL)

        # Create file handler which logs even debug messages
        file_handler = logging.FileHandler(LOG_FILE, mode='a', encoding='utf-8')
        file_handler.setLevel(LOG_LEVEL)

        # Create formatter and add it to the handler
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        logger.addHandler(file_handler)

        # Prevent the logger from propagating messages to the root logger
        logger.propagate = False

        print(f"Logging setup complete. Log file: {LOG_FILE}")
        return logger

    except Exception as e:
        print(f"Error setting up logging: {str(e)}", file=sys.stderr)
        raise

# Create a global logger instance
try:
    logger = setup_logging()
except Exception as e:
    print(f"Failed to set up logging: {str(e)}", file=sys.stderr)
    sys.exit(1)
