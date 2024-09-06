# src/modules/context_management.py

import json
from typing import List, Dict, Any
from src.modules.memory_search import search_memories
from src.modules.logging_setup import logger
from src.modules.errors import DataProcessingError
from src.modules.ollama_client import process_prompt

def gather_context(user_input: str, topic: str, conversation_history: List[Dict[str, str]], bullet_points: List[str], agent_name: str) -> str:
    """
    Gather context from various sources for a given user input.
    """
    try:
        logger.info(f"Gathering context for topic: {topic}")

        # Retrieve relevant memories
        memories = search_memories(user_input, top_k=3, similarity_threshold=0.7)
        memory_context = "\n".join([f"💾 Related info: {m['content']}" for m in memories])

        # Get recent conversation history
        recent_history = conversation_history[-3:]
        history_context = "\n".join([f"👤 User: {h.get('prompt', '')}\n🤖 {agent_name}: {h.get('response', '')}" for h in recent_history])

        # Format bullet points
        bullet_context = "\n".join([f"📌 {point}" for point in bullet_points])

        # Combine all context
        full_context = f"🏷️ Topic: {topic}\n\n📚 Relevant information:\n{memory_context}\n\n💬 Recent conversation:\n{history_context}\n\n🔑 Key points:\n{bullet_context}"

        logger.info("Context gathering completed successfully")
        return full_context
    except Exception as e:
        logger.error(f"Error gathering context: {str(e)}")
        raise DataProcessingError(f"Failed to gather context: {str(e)}")

def update_context(current_context: str, new_information: str, model_name: str) -> str:
    """
    Update the current context with new information.
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

def extract_key_information(context: str, model_name: str) -> Dict[str, Any]:
    """
    Extract key information from the given context.
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
        return eval(extracted_info)  # Convert string to dictionary. In production, use proper JSON parsing.
    except Exception as e:
        logger.error(f"Error extracting key information: {str(e)}")
        return {"error": "Failed to extract key information"}

def summarize_context(context: str, model_name: str) -> str:
    """
    Summarize the given context.
    """
    try:
        logger.info("Summarizing context")
        summary_prompt = f"Summarize the following context in a concise manner:\n\n{context}"
        return process_prompt(summary_prompt, model_name, "ContextSummarizer")
    except Exception as e:
        logger.error(f"Error summarizing context: {str(e)}")
        return "Failed to summarize context due to an error."

def identify_context_gaps(context: str, model_name: str) -> List[str]:
    """
    Identify gaps or missing information in the given context.
    """
    try:
        logger.info("Identifying context gaps")
        gap_prompt = f"""Analyze the following context and identify any gaps or missing information:
        {context}

        List the gaps or missing information as bullet points.
        """
        gaps = process_prompt(gap_prompt, model_name, "GapIdentifier")
        return [gap.strip() for gap in gaps.split('\n') if gap.strip()]
    except Exception as e:
        logger.error(f"Error identifying context gaps: {str(e)}")
        return []

def prioritize_context(context: str, user_query: str, model_name: str) -> str:
    """
    Prioritize and restructure the context based on relevance to the user query.
    """
    try:
        logger.info("Prioritizing context")
        prioritize_prompt = f"""Given the following context and user query, restructure and prioritize the information based on its relevance to the query:

        Context:
        {context}

        User Query:
        {user_query}

        Provide a restructured and prioritized version of the context.
        """
        return process_prompt(prioritize_prompt, model_name, "ContextPrioritizer")
    except Exception as e:
        logger.error(f"Error prioritizing context: {str(e)}")
        return context  # Return original context if prioritization fails

def merge_contexts(contexts: List[str], model_name: str) -> str:
    """
    Merge multiple contexts into a single, coherent context.
    """
    try:
        logger.info("Merging multiple contexts")
        merge_prompt = f"""Merge the following contexts into a single, coherent context:

        {json.dumps(contexts, indent=2)}

        Provide a merged context that combines information from all sources without redundancy.
        """
        return process_prompt(merge_prompt, model_name, "ContextMerger")
    except Exception as e:
        logger.error(f"Error merging contexts: {str(e)}")
        return "\n\n".join(contexts)  # Return concatenated contexts if merging fails

def filter_context(context: str, relevance_threshold: float, model_name: str) -> str:
    """
    Filter the context to keep only highly relevant information.
    """
    try:
        logger.info(f"Filtering context with relevance threshold: {relevance_threshold}")
        filter_prompt = f"""Filter the following context to keep only information with a relevance score above {relevance_threshold}:

        {context}

        For each piece of information, assign a relevance score between 0 and 1, and only keep information scoring above the threshold.
        Provide the filtered context.
        """
        return process_prompt(filter_prompt, model_name, "ContextFilter")
    except Exception as e:
        logger.error(f"Error filtering context: {str(e)}")
        return context  # Return original context if filtering fails

def expand_context(context: str, focus_area: str, model_name: str) -> str:
    """
    Expand the context with additional information about a specific focus area.
    """
    try:
        logger.info(f"Expanding context for focus area: {focus_area}")
        expand_prompt = f"""Expand the following context with additional information about the focus area:

        Context:
        {context}

        Focus Area:
        {focus_area}

        Provide an expanded context with more detailed information about the focus area.
        """
        return process_prompt(expand_prompt, model_name, "ContextExpander")
    except Exception as e:
        logger.error(f"Error expanding context: {str(e)}")
        return context  # Return original context if expansion fails

def generate_context_metadata(context: str, model_name: str) -> Dict[str, Any]:
    """
    Generate metadata for the given context.
    """
    try:
        logger.info("Generating context metadata")
        metadata_prompt = f"""Generate metadata for the following context:

        {context}

        Provide the metadata in the following JSON format:
        {{
            "word_count": 0,
            "main_language": "Language",
            "sentiment": "Positive/Neutral/Negative",
            "complexity_level": "Low/Medium/High",
            "key_themes": ["Theme 1", "Theme 2"],
            "content_type": "Informational/Narrative/Technical/etc."
        }}
        """
        metadata = process_prompt(metadata_prompt, model_name, "MetadataGenerator")
        return eval(metadata)  # Convert string to dictionary. In production, use proper JSON parsing.
    except Exception as e:
        logger.error(f"Error generating context metadata: {str(e)}")
        return {"error": "Failed to generate metadata"}

def adapt_context_to_user(context: str, user_profile: Dict[str, Any], model_name: str) -> str:
    """
    Adapt the context to a specific user's profile and preferences.
    """
    try:
        logger.info("Adapting context to user profile")
        adapt_prompt = f"""Adapt the following context to the user's profile and preferences:

        Context:
        {context}

        User Profile:
        {json.dumps(user_profile, indent=2)}

        Provide an adapted version of the context that matches the user's language preference, expertise level, and interests.
        """
        return process_prompt(adapt_prompt, model_name, "ContextAdapter")
    except Exception as e:
        logger.error(f"Error adapting context to user: {str(e)}")
        return context  # Return original context if adaptation fails
