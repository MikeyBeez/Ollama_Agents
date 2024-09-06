# src/modules/context_management.py

from typing import List, Tuple, Dict, Any
from src.modules.memory_search import search_memories
from src.modules.logging_setup import logger
from src.modules.errors import DataProcessingError
from src.modules.ollama_client import process_prompt

class BulletPointManager:
    def __init__(self):
        self.bullet_points = []

    def add_bullet_point(self, bullet_point: str):
        if bullet_point not in self.bullet_points:
            self.bullet_points.append(bullet_point)
            self._rank_and_trim()

    def _rank_and_trim(self):
        if len(self.bullet_points) > 15:
            self.bullet_points = rank_bullet_points(self.bullet_points)[:15]

    def get_bullet_points(self) -> List[str]:
        return self.bullet_points

bullet_manager = BulletPointManager()

def gather_context(user_input: str, topic: str, conversation_history: List[Tuple[str, str]], bullet_points: List[str], agent_name: str) -> str:
    """
    Gather context from various sources for a given user input.

    Args:
    user_input (str): The user's input query.
    topic (str): The main topic of the query.
    conversation_history (List[Tuple[str, str]]): Recent conversation history.
    bullet_points (List[str]): Current bullet points.
    agent_name (str): Name of the agent gathering context.

    Returns:
    str: A string containing the gathered context.
    """
    try:
        logger.info(f"Gathering context for topic: {topic}")

        # Retrieve relevant memories
        memories = search_memories(user_input, top_k=3, similarity_threshold=0.7)
        memory_context = "\n".join([f"💾 Related info: {m['content']}" for m in memories])

        # Get recent conversation history
        recent_history = conversation_history[-3:]
        history_context = "\n".join([f"👤 User: {h[0]}\n🤖 {agent_name}: {h[1]}" for h in recent_history])

        # Format bullet points
        bullet_context = "\n".join([f"📌 {point}" for point in bullet_points])

        # Combine all context
        full_context = f"🏷️ Topic: {topic}\n\n📚 Relevant information:\n{memory_context}\n\n💬 Recent conversation:\n{history_context}\n\n🔑 Key points:\n{bullet_context}"

        logger.info("Context gathering completed successfully")
        return full_context
    except Exception as e:
        logger.error(f"Error gathering context: {str(e)}")
        raise DataProcessingError(f"Failed to gather context: {str(e)}")

def rank_bullet_points(bullet_points: List[str], model_name: str = "default") -> List[str]:
    """
    Rank a list of bullet points by importance and relevance.

    Args:
    bullet_points (List[str]): List of bullet points to rank.
    model_name (str): Name of the model to use for ranking.

    Returns:
    List[str]: Ranked list of bullet points.
    """
    try:
        logger.info("Ranking bullet points")
        ranking_prompt = "Rank the following bullet points by importance and relevance:\n" + "\n".join(bullet_points)
        ranked = process_prompt(ranking_prompt, model_name, "BulletPointRanker")
        return [b.strip() for b in ranked.split('\n') if b.strip()]
    except Exception as e:
        logger.error(f"Error ranking bullet points: {str(e)}")
        return bullet_points  # Return original list if ranking fails

def summarize_context(context: str, model_name: str) -> str:
    """
    Summarize the given context.

    Args:
    context (str): The context to summarize.
    model_name (str): Name of the model to use for summarization.

    Returns:
    str: A summary of the context.
    """
    try:
        logger.info("Summarizing context")
        summary_prompt = f"Summarize the following context in a concise manner:\n\n{context}"
        return process_prompt(summary_prompt, model_name, "ContextSummarizer")
    except Exception as e:
        logger.error(f"Error summarizing context: {str(e)}")
        return "Failed to summarize context due to an error."

def extract_key_information(context: str, model_name: str) -> Dict[str, Any]:
    """
    Extract key information from the given context.

    Args:
    context (str): The context to extract information from.
    model_name (str): Name of the model to use for extraction.

    Returns:
    Dict[str, Any]: A dictionary containing extracted key information.
    """
    try:
        logger.info("Extracting key information from context")
        extraction_prompt = f"""Extract key information from the following context:
        {context}

        Provide the extracted information in the following JSON format:
        {{
            "main_topic": "The main topic of the context",
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "entities": ["Entity 1", "Entity 2"],
            "time_references": ["Time reference 1", "Time reference 2"],
            "open_questions": ["Question 1", "Question 2"]
        }}
        """
        extracted_info = process_prompt(extraction_prompt, model_name, "InfoExtractor")
        return json.loads(extracted_info)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing extracted information: {str(e)}")
        return {"error": "Failed to parse extracted information"}
    except Exception as e:
        logger.error(f"Error extracting key information: {str(e)}")
        return {"error": "Failed to extract key information"}

def update_context(current_context: str, new_information: str, model_name: str) -> str:
    """
    Update the current context with new information.

    Args:
    current_context (str): The current context.
    new_information (str): New information to be incorporated.
    model_name (str): Name of the model to use for context updating.

    Returns:
    str: Updated context.
    """
    try:
        logger.info("Updating context with new information")
        update_prompt = f"""Update the following context with the new information:

        Current Context:
        {current_context}

        New Information:
        {new_information}

        Provide an updated context that incorporates the new information coherently.
        """
        return process_prompt(update_prompt, model_name, "ContextUpdater")
    except Exception as e:
        logger.error(f"Error updating context: {str(e)}")
        return current_context  # Return original context if update fails
