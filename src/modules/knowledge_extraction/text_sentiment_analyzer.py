# src/modules/knowledge_extraction/text_sentiment_analyzer.py

from typing import Dict, Any
from src.modules.ollama_client import process_prompt
from src.modules.logging_setup import logger
from .json_response_parser import extract_json_from_response, handle_extraction_error

def analyze_sentiment(text: str) -> Dict[str, Any]:
    prompt = f"""
    Analyze the sentiment of the following text:
    "{text}"

    Provide your response as a JSON object with the following structure:
    {{
        "sentiment": "positive/negative/neutral",
        "intensity": 0.0 to 1.0
    }}
    """

    try:
        response = process_prompt(prompt, "llama3.1:latest", "SentimentAnalyzer")
        logger.debug(f"Raw response from SentimentAnalyzer: {response}")

        result = extract_json_from_response(response)

        if 'sentiment' in result and 'intensity' in result:
            result['sentiment'] = result['sentiment'].lower()
            result['intensity'] = float(result['intensity'])
            return result
        else:
            raise ValueError("Missing required keys in sentiment analysis result")
    except Exception as e:
        return handle_extraction_error(e, "Error in sentiment analysis")
