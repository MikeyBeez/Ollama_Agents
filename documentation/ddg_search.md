# 🔍 DuckDuckGo Search Module

## Overview

The DuckDuckGo Search Module (`ddg_search.py`) integrates web search capabilities into the AI assistant using the DuckDuckGo search engine.

## Key Features

1. **Web Search Integration**: Allows the AI to perform web searches.
2. **Result Processing**: Handles and formats search results for easy consumption.
3. **Error Handling**: Manages potential issues during the search process.

## Main Class

### `DDGSearch`

This class encapsulates the DuckDuckGo search functionality.

#### Key Method

- `run_search(query)`: Executes a search query and returns formatted results.

## Why a Separate Module?

The DuckDuckGo search module is separated to:
1. Isolate web search functionality from core AI operations.
2. Allow for easy swapping or addition of different search engines.
3. Simplify testing and maintenance of search-related features.

## What Makes It Special?

- Integrates seamlessly with the LangChain ecosystem.
- Provides a simple interface for performing web searches.
- Enhances the AI's capabilities by allowing it to access current information.

This module significantly expands the AI's knowledge base, allowing it to provide up-to-date information and more informed responses to user queries.
