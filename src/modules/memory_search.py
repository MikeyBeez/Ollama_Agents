# src/modules/memory_search.py

import numpy as np
from numpy.linalg import norm
import ollama
import json
from typing import List, Tuple, Dict, Any
from pathlib import Path
from config import DATA_DIR, EMBEDDINGS_DIR, EMBEDDING_MODEL, DEFAULT_MODEL
from .file_utils import read_json_file, write_json_file, get_json_files_in_directory, increment_json_field
from .logging_setup import logger
from .ollama_client import process_prompt
from .kb_graph import get_related_nodes, get_db_connection

def read_memory(filename: str) -> Dict[str, Any]:
    file_path = DATA_DIR / filename
    try:
        data = read_json_file(file_path)
        increment_json_field(file_path, 'access_count')
        logger.debug(f"Read memory: {filename}, access count: {data['access_count']}")
        return data
    except Exception as e:
        logger.error(f"Error reading memory file {filename}: {str(e)}")
        return {}

def save_embeddings(filename: str, embeddings: List[float]) -> None:
    try:
        write_json_file(EMBEDDINGS_DIR / f"{filename}.json", embeddings)
        logger.info(f"Saved embeddings for file: {filename}")
    except Exception as e:
        logger.error(f"Error saving embeddings for file {filename}: {str(e)}")

def load_embeddings(filename: str) -> List[float]:
    embeddings_file = EMBEDDINGS_DIR / f"{filename}.json"
    if not embeddings_file.exists():
        logger.debug(f"No existing embeddings found for file: {filename}")
        return []
    try:
        return read_json_file(embeddings_file)
    except Exception as e:
        logger.error(f"Error loading embeddings for file {filename}: {str(e)}")
        return []

def get_embeddings(filename: str) -> List[float]:
    if embeddings := load_embeddings(filename):
        return embeddings
    memory_data = read_memory(filename)
    if 'type' not in memory_data:
        text = str(memory_data)
    elif memory_data['type'] == 'interaction':
        if isinstance(memory_data['content'], dict) and 'prompt' in memory_data['content'] and 'response' in memory_data['content']:
            text = f"{memory_data['content']['prompt']}\n{memory_data['content']['response']}"
        else:
            text = str(memory_data['content'])
    else:  # document_chunk or any other type
        text = str(memory_data['content'])
    try:
        embeddings = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)["embedding"]
        save_embeddings(filename, embeddings)
        logger.info(f"Generated new embeddings for file: {filename}")
        return embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings for file {filename}: {str(e)}")
        return []

def find_most_similar(needle: List[float], haystack: List[List[float]]) -> List[Tuple[float, int]]:
    try:
        needle_norm = norm(needle)
        similarity_scores = [
            np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack
        ]
        return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)
    except Exception as e:
        logger.error(f"Error in finding most similar embeddings: {str(e)}")
        return []

def search_memories(query: str, top_k: int = 5, similarity_threshold: float = 0.0) -> List[Dict[str, Any]]:
    logger.info(f"Searching memories for query: {query[:50]}...")  # Log only first 50 characters

    # Embedding-based search
    memory_files = get_json_files_in_directory(DATA_DIR)
    embeddings = [get_embeddings(f.name) for f in memory_files]
    try:
        query_embedding = ollama.embeddings(model=EMBEDDING_MODEL, prompt=query)["embedding"]
        most_similar_files = find_most_similar(query_embedding, embeddings)
    except Exception as e:
        logger.error(f"Error generating query embedding: {str(e)}")
        most_similar_files = []

    relevant_memories = []
    for similarity, index in most_similar_files:
        if similarity < similarity_threshold:
            break
        if len(relevant_memories) >= top_k:
            break
        filename = memory_files[index].name
        memory_data = read_memory(filename)

        relevant_memories.append({
            "content": memory_data.get("content", ""),
            "type": memory_data.get("type", "unknown"),
            "similarity": similarity,
            "timestamp": memory_data.get("timestamp", ""),
            "access_count": memory_data.get("access_count", 0),
            "permanent_marker": memory_data.get("permanent_marker", 0),
            "filename": filename,
            "source": "embedding"
        })

    # Edge-based search
    query_id = hash(query)  # Using a simple hash for demonstration; you might want a more robust method
    edge_results = get_related_nodes(str(query_id))

    for node_id, relationship_type, strength in edge_results:
        if len(relevant_memories) >= top_k * 2:  # Allowing more results to combine later
            break
        memory_data = read_memory(f"{node_id}.json")
        relevant_memories.append({
            "content": memory_data.get("content", ""),
            "type": memory_data.get("type", "unknown"),
            "similarity": strength,  # Using edge strength as a proxy for similarity
            "timestamp": memory_data.get("timestamp", ""),
            "access_count": memory_data.get("access_count", 0),
            "permanent_marker": memory_data.get("permanent_marker", 0),
            "filename": f"{node_id}.json",
            "source": "edge",
            "relationship": relationship_type
        })

    # Combine and rank results
    combined_results = sorted(relevant_memories, key=lambda x: x['similarity'], reverse=True)[:top_k]

    logger.info(f"Found {len(combined_results)} relevant memories")
    for result in combined_results:
        content = result.get('content', '')
        if isinstance(content, str):
            logger.debug(f"Search result: {content[:100]}...")  # Log first 100 chars of each result
        elif isinstance(content, dict):
            logger.debug(f"Search result: {str(content)[:100]}...")  # Log first 100 chars of stringified dict
        else:
            logger.debug(f"Search result: {type(content)}")  # Log type if content is neither string nor dict

    return combined_results

def generate_embeddings_for_existing_files():
    memory_files = get_json_files_in_directory(DATA_DIR)
    for file in memory_files:
        if not load_embeddings(file.name):
            get_embeddings(file.name)
    logger.info(f"Generated embeddings for {len(memory_files)} files")

def generate_search_query(topic: str, perspective: str) -> str:
    prompt = f"""Generate a short, focused search query to find information supporting the {perspective} side of the debate topic: '{topic}'.
    Return your response in the following JSON format:
    {{
        "query": "Your search query here"
    }}
    """
    response = process_prompt(prompt, DEFAULT_MODEL, "Search Query Generator")
    try:
        query_json = json.loads(response)
        return query_json['query']
    except json.JSONDecodeError:
        logger.error(f"Failed to parse JSON from response: {response}")
        return f"Error: Could not generate a valid search query for {topic} ({perspective})"
    except KeyError:
        logger.error(f"Missing 'query' key in JSON response: {response}")
        return f"Error: Invalid response format for {topic} ({perspective})"

# Run this function when the module is imported to ensure all files have embeddings
generate_embeddings_for_existing_files()
