# src/modules/memory_search.py

import numpy as np
from numpy.linalg import norm
import ollama
from typing import List, Tuple, Dict, Any
from config import DATA_DIR, EMBEDDINGS_DIR, EMBEDDING_MODEL
from .file_utils import read_json_file, write_json_file, get_json_files_in_directory, increment_json_field
from .logging_setup import logger

def read_memory(filename: str) -> Dict[str, Any]:
    file_path = DATA_DIR / filename
    data = read_json_file(file_path)
    increment_json_field(file_path, 'access_count')
    logger.debug(f"Read memory: {filename}, access count: {data['access_count']}")
    return data

def save_embeddings(filename: str, embeddings: List[float]) -> None:
    write_json_file(EMBEDDINGS_DIR / f"{filename}.json", embeddings)
    logger.info(f"Saved embeddings for file: {filename}")

def load_embeddings(filename: str) -> List[float]:
    embeddings_file = EMBEDDINGS_DIR / f"{filename}.json"
    if not embeddings_file.exists():
        logger.debug(f"No existing embeddings found for file: {filename}")
        return []
    return read_json_file(embeddings_file)

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
    embeddings = ollama.embeddings(model=EMBEDDING_MODEL, prompt=text)["embedding"]
    save_embeddings(filename, embeddings)
    logger.info(f"Generated new embeddings for file: {filename}")
    return embeddings

def find_most_similar(needle: List[float], haystack: List[List[float]]) -> List[Tuple[float, int]]:
    needle_norm = norm(needle)
    similarity_scores = [
        np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack
    ]
    return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)

def search_memories(query: str, top_k: int = 5, similarity_threshold: float = 0.0) -> List[Dict[str, Any]]:
    logger.info(f"Searching memories for query: {query[:50]}...")  # Log only first 50 characters
    memory_files = get_json_files_in_directory(DATA_DIR)
    embeddings = [get_embeddings(f.name) for f in memory_files]
    query_embedding = ollama.embeddings(model=EMBEDDING_MODEL, prompt=query)["embedding"]
    most_similar_files = find_most_similar(query_embedding, embeddings)

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
            "filename": filename
        })

    logger.info(f"Found {len(relevant_memories)} relevant memories")
    return relevant_memories

def generate_embeddings_for_existing_files():
    memory_files = get_json_files_in_directory(DATA_DIR)
    for file in memory_files:
        if not load_embeddings(file.name):
            get_embeddings(file.name)
    logger.info(f"Generated embeddings for {len(memory_files)} files")

# Run this function when the module is imported to ensure all files have embeddings
generate_embeddings_for_existing_files()
