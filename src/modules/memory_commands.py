# src/modules/memory_commands.py

from typing import List, Dict, Any
from rich.console import Console
from src.modules.memory_search import search_memories
from src.modules.ollama_client import process_prompt
from src.modules.save_history import get_chat_history, chat_history
from config import AGENT_NAME, DEFAULT_MODEL, USER_NAME
from src.modules.logging_setup import logger

console = Console()

def memory_search(command: str) -> str:
    try:
        parts = command.split(maxsplit=3)
        if len(parts) < 4:
            raise ValueError("Insufficient arguments")

        _, top_k, similarity_threshold, query = parts
        top_k = int(top_k)
        similarity_threshold = float(similarity_threshold)

        if top_k <= 0 or similarity_threshold < 0 or similarity_threshold > 1:
            raise ValueError("Invalid parameters")

        logger.info(f"Performing memory search with query: '{query[:50]}...', top_k: {top_k}, threshold: {similarity_threshold}")
        memories = search_memories(query, top_k=top_k, similarity_threshold=similarity_threshold)

        if not memories:
            logger.info("No relevant memories found")
            console.print("No relevant memories found.", style="bold yellow")
        else:
            logger.info(f"Found {len(memories)} relevant memories")
            # Prepare context from memories
            context = "\n".join([f"Memory (similarity {m['similarity']:.2f}):\n{m['content']}" for m in memories])

            # Generate answer using AI model
            prompt = f"You are {AGENT_NAME}, an AI assistant. Based on the following memories and the original query, please provide a comprehensive answer:\n\nQuery: {query}\n\nRelevant Memories:\n{context}\n\nAnswer:"
            logger.info("Generating answer based on memories")
            answer = process_prompt(prompt, DEFAULT_MODEL, USER_NAME)

            console.print("\nGenerated Answer:", style="bold blue")
            console.print(answer, style="bold green")
            logger.info("Answer generated and displayed")

    except ValueError as e:
        error_msg = f"Error: {str(e)}. Usage: /ms n m query (where n is the number of memories, m is the similarity threshold between 0 and 1, and query is your question)"
        logger.error(error_msg)
        console.print(error_msg, style="bold red")
    except Exception as e:
        logger.exception(f"Unexpected error in memory_search: {str(e)}")
        console.print(f"An unexpected error occurred: {str(e)}", style="bold red")

    return 'CONTINUE'

def memory_search_long(command: str) -> str:
    try:
        parts = command.split(maxsplit=3)
        if len(parts) < 4:
            raise ValueError("Insufficient arguments")

        _, top_k, similarity_threshold, query = parts
        top_k = int(top_k)
        similarity_threshold = float(similarity_threshold)

        if top_k <= 0 or similarity_threshold < 0 or similarity_threshold > 1:
            raise ValueError("Invalid parameters")

        logger.info(f"Performing detailed memory search with query: '{query[:50]}...', top_k: {top_k}, threshold: {similarity_threshold}")
        console.print(f"Searching for top {top_k} memories with similarity above {similarity_threshold*100}%", style="bold yellow")
        memories = search_memories(query, top_k=top_k, similarity_threshold=similarity_threshold)

        logger.info(f"Found {len(memories)} memories in search")

        if not memories:
            logger.info("No relevant memories found")
            console.print("No relevant memories found.", style="bold yellow")
        else:
            console.print(f"Found {len(memories)} relevant memories:", style="bold green")
            for i, memory in enumerate(memories, 1):
                console.print(f"\n--- Memory {i} (Similarity: {memory['similarity']:.2%}) ---", style="bold blue")
                console.print(f"Type: {memory.get('type', 'unknown')}", style="cyan")
                console.print(f"Timestamp: {memory.get('timestamp', 'unknown')}", style="cyan")
                console.print(f"Filename: {memory.get('filename', 'unknown')}", style="cyan")
                if memory.get('type') == 'interaction':
                    if isinstance(memory.get('content'), dict) and 'prompt' in memory['content'] and 'response' in memory['content']:
                        console.print(f"User: {memory['content']['prompt']}", style="green")
                        console.print(f"Assistant: {memory['content']['response']}", style="yellow")
                    else:
                        console.print(f"Content: {memory.get('content', 'No content available')}", style="yellow")
                else:  # document_chunk or unknown
                    console.print(f"Content: {memory.get('content', 'No content available')}", style="yellow")

            # Prepare context from memories
            context = "\n".join([f"Memory (similarity {m['similarity']:.2f}):\n{m['content']}" for m in memories])

            # Generate answer using AI model
            prompt = f"You are {AGENT_NAME}, an AI assistant. Based on the following memories and the original query, please provide a comprehensive answer:\n\nQuery: {query}\n\nRelevant Memories:\n{context}\n\nAnswer:"
            logger.info("Generating answer based on memories")
            answer = process_prompt(prompt, DEFAULT_MODEL, USER_NAME)

            console.print("\nGenerated Answer:", style="bold blue")
            console.print(answer, style="bold green")
            logger.info("Answer generated and displayed")

    except ValueError as e:
        error_msg = f"Error: {str(e)}. Usage: /msl n m query (where n is the number of memories, m is the similarity threshold between 0 and 1, and query is your question)"
        logger.error(error_msg)
        console.print(error_msg, style="bold red")
    except Exception as e:
        logger.exception(f"Unexpected error in memory_search_long: {str(e)}")
        console.print(f"An unexpected error occurred: {str(e)}", style="bold red")

    return 'CONTINUE'

def print_history(command: str = '') -> str:
    history = get_chat_history()
    if not history:
        logger.info("No chat history available")
        console.print("No chat history available.", style="bold green")
        return 'CONTINUE'

    logger.info(f"Displaying chat history. Total entries: {len(history)}")
    console.print("Chat History:", style="bold green")
    for i, entry in enumerate(history, 1):
        console.print(f"\n--- Entry {i} ---", style="bold blue")
        console.print(f"User: {entry['prompt']}", style="green")
        console.print(f"Assistant: {entry['response']}", style="yellow")

    console.print(f"\nTotal entries in chat history: {len(history)}", style="bold purple")

    return 'CONTINUE'

def truncate_history(command: str) -> str:
    try:
        n = int(command.split()[1])
        if n < 0:
            raise ValueError("Number of entries must be non-negative")

        chat_history.history = chat_history.history[-n:]
        chat_history.save_history()

        logger.info(f"Chat history truncated to last {n} entries")
        console.print(f"Chat history truncated to last {n} entries.", style="bold green")
    except IndexError:
        error_msg = "Error: Please provide the number of entries to keep. Usage: /tr n"
        logger.error(error_msg)
        console.print(error_msg, style="bold red")
    except ValueError as e:
        error_msg = f"Error: {str(e)}. Please provide a valid non-negative integer."
        logger.error(error_msg)
        console.print(error_msg, style="bold red")
    return 'CONTINUE'
