# 🔍 DuckDuckGo Search Module

The DuckDuckGo Search Module integrates web search capabilities into the AI assistant.

## 🌟 Key Features

- 🌐 Performs web searches using the DuckDuckGo search engine
- 📊 Processes and formats search results

## 🔧 Main Functions

- 🔎 `run_search(query)`: Executes a web search and returns the results

## 🚀 Usage

This module is used when the AI assistant needs to fetch current information from the web to answer user queries.

## 🧪 Testing

While there's no dedicated test file for this module, consider adding one to cover:

- Successful search queries
- Handling of empty results
- Error handling for network issues

A sample test file structure could be:

```python
import unittest
from unittest.mock import patch
from src.modules.ddg_search import DDGSearch

class TestDDGSearch(unittest.TestCase):
    def setUp(self):
        self.ddg_search = DDGSearch()

    @patch('src.modules.ddg_search.DuckDuckGoSearchRun')
    def test_successful_search(self, mock_ddg):
        # Test implementation

    def test_empty_results(self):
        # Test implementation

    @patch('src.modules.ddg_search.DuckDuckGoSearchRun')
    def test_network_error(self, mock_ddg):
        # Test implementation

if __name__ == '__main__':
    unittest.main()
```

## 🔍 Key Considerations

- Implement rate limiting to avoid overloading the search service
- Consider caching frequently searched queries to improve response time
- Ensure proper error handling for network issues or service unavailability
