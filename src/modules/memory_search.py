import os
import json
import numpy as np
from numpy.linalg import norm
import ollama
# from datetime import datetime
from typing import List, Tuple, Dict, Any
import logging

# Get the absolute path of the current file
current_file_path = os.path.abspath(__file__)
# Get the project root directory (assuming it's two levels up from this file)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
# Set the data directory relative to the project root
data_dir = os.path.join(project_root, "data", "json_history")


def read_file(filename: str) -> Dict[str, Any]:
    """Read a JSON file and return its contents."""
    with open(os.path.join(data_dir, filename), encoding="utf-8") as f:
        data = json.load(f)
        logging.debug(f"Read file: {filename}")
        return data


def save_embeddings(filename: str, embeddings: List[float]) -> None:
    """Save embeddings to a JSON file."""
    embeddings_dir = os.path.join(data_dir, "embeddings")
    os.makedirs(embeddings_dir, exist_ok=True)
    with open(os.path.join(embeddings_dir, f"{filename}.json"), "w") as f:
        json.dump(embeddings, f)
    logging.info(f"Saved embeddings for file: {filename}")


def load_embeddings(filename: str) -> List[float]:
    """Load embeddings from a JSON file."""
    embeddings_file = os.path.join(data_dir, "embeddings", f"{filename}.json")
    if not os.path.exists(embeddings_file):
        logging.debug(f"No existing embeddings found for file: {filename}")
        return []
    with open(embeddings_file, "r") as f:
        embeddings = json.load(f)
        logging.debug(f"Loaded existing embeddings for file: {filename}")
        return embeddings


def get_embeddings(filename: str, modelname: str) -> List[float]:
    """Get embeddings for a file, either from cache or by generating new ones."""
    if embeddings := load_embeddings(filename):
        return embeddings
    memory_data = read_file(filename)
    combined_text = memory_data.get("prompt", "") + "\n" + memory_data.get("response", "")
    embeddings = ollama.embeddings(model=modelname, prompt=combined_text)["embedding"]
    save_embeddings(filename, embeddings)
    logging.info(f"Generated new embeddings for file: {filename}")
    return embeddings


def find_most_similar(needle: List[float], haystack: List[List[float]]) -> List[Tuple[float, int]]:
    """Find cosine similarity of every file to a given embedding."""
    needle_norm = norm(needle)
    similarity_scores = [
        np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack
    ]
    return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)


def search_memories(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """Search memories and return the most relevant ones with metadata."""
    logging.info(f"Searching memories for query: {query}")
    memory_files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
    embeddings = [get_embeddings(f, "nomic-embed-text") for f in memory_files]
    query_embedding = ollama.embeddings(model="nomic-embed-text", prompt=query)["embedding"]
    most_similar_files = find_most_similar(query_embedding, embeddings)

    relevant_memories = []
    for similarity, index in most_similar_files:
        filename = memory_files[index]
        memory_data = read_file(filename)

        relevant_memories.append({
            "prompt": memory_data.get("prompt", ""),
            "response": memory_data.get("response", ""),
            "similarity": similarity,
            "timestamp": memory_data.get("timestamp", "")
        })

    return relevant_memories


def generate_embeddings_for_existing_files():
    """Generate embeddings for all existing JSON files that don't have embeddings yet."""
    memory_files = [f for f in os.listdir(data_dir) if f.endswith(".json")]
    for filename in memory_files:
        if not load_embeddings(filename):
            get_embeddings(filename, "nomic-embed-text")
    logging.info(f"Generated embeddings for {len(memory_files)} files")


# Run this function when the module is imported to ensure all files have embeddings
generate_embeddings_for_existing_files()

