# src/modules/ddg_search.py

from duckduckgo_search import DDGS
from src.modules.logging_setup import logger
from src.modules.errors import APIConnectionError

class DDGSearch:
    def __init__(self):
        self.ddgs = DDGS()

    def run_search(self, query):
        try:
            logger.info(f"Initiating DuckDuckGo search for query: '{query[:50]}...'")
            results = list(self.ddgs.text(query, max_results=5))
            logger.info(f"Received {len(results)} results from DuckDuckGo")
            return [result['title'] + ': ' + result['body'] for result in results]
        except Exception as e:
            logger.error(f"Error during DuckDuckGo search: {str(e)}")
            return []  # Return an empty list instead of raising an exception
