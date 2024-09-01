# src/modules/memory_search.py

import os
import json
import numpy as np
from numpy.linalg import norm
import ollama
from typing import List, Tuple, Dict, Any
import logging
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent.parent
# Set the data directory relative to the project root
data_dir = project_root / "data" / "json_history"

def read_memory(filename: str) -> Dict[str, Any]:
    file_path = data_dir / filename
    with open(file_path, 'r', encoding="utf-8") as f:
        data = json.load(f)

    # Increment access count
    data['access_count'] = data.get('access_count', 0) + 1

    # Save the updated data
    with open(file_path, 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logging.debug(f"Read memory: {filename}, access count: {data['access_count']}")
    return data

def save_embeddings(filename: str, embeddings: List[float]) -> None:
    embeddings_dir = data_dir / "embeddings"
    embeddings_dir.mkdir(exist_ok=True)
    with open(embeddings_dir / f"{filename}.json", "w") as f:
        json.dump(embeddings, f)
    logging.info(f"Saved embeddings for file: {filename}")

def load_embeddings(filename: str) -> List[float]:
    embeddings_file = data_dir / "embeddings" / f"{filename}.json"
    if not embeddings_file.exists():
        logging.debug(f"No existing embeddings found for file: {filename}")
        return []
    with open(embeddings_file, "r") as f:
        embeddings = json.load(f)
        logging.debug(f"Loaded existing embeddings for file: {filename}")
        return embeddings

def get_embeddings(filename: str, modelname: str) -> List[float]:
    if embeddings := load_embeddings(filename):
        return embeddings
    memory_data = read_memory(filename)
    if 'type' not in memory_data:
        # Handle old format or unknown type
        text = json.dumps(memory_data)
    elif memory_data['type'] == 'interaction':
        if isinstance(memory_data['content'], dict) and 'prompt' in memory_data['content'] and 'response' in memory_data['content']:
            text = f"{memory_data['content']['prompt']}\n{memory_data['content']['response']}"
        else:
            text = str(memory_data['content'])
    else:  # document_chunk or any other type
        text = str(memory_data['content'])
    embeddings = ollama.embeddings(model=modelname, prompt=text)["embedding"]
    save_embeddings(filename, embeddings)
    logging.info(f"Generated new embeddings for file: {filename}")
    return embeddings

def find_most_similar(needle: List[float], haystack: List[List[float]]) -> List[Tuple[float, int]]:
    needle_norm = norm(needle)
    similarity_scores = [
        np.dot(needle, item) / (needle_norm * norm(item)) for item in haystack
    ]
    return sorted(zip(similarity_scores, range(len(haystack))), reverse=True)

def search_memories(query: str, top_k: int = 5, similarity_threshold: float = 0.0) -> List[Dict[str, Any]]:
    logging.info(f"Searching memories for query: {query}")
    memory_files = [f for f in data_dir.glob("*.json") if f.is_file()]
    embeddings = [get_embeddings(f.name, "nomic-embed-text") for f in memory_files]
    query_embedding = ollama.embeddings(model="nomic-embed-text", prompt=query)["embedding"]
    most_similar_files = find_most_similar(query_embedding, embeddings)

    relevant_memories = []
    for similarity, index in most_similar_files:
        if similarity < similarity_threshold:
            break
        if len(relevant_memories) >= top_k:
            break
        filename = memory_files[index].name
        memory_data = read_memory(filename)  # This will now increment the access count

        relevant_memories.append({
            "content": memory_data.get("content", ""),
            "type": memory_data.get("type", "unknown"),
            "similarity": similarity,
            "timestamp": memory_data.get("timestamp", ""),
            "access_count": memory_data.get("access_count", 0),
            "permanent_marker": memory_data.get("permanent_marker", 0),
            "filename": filename
        })

    return relevant_memories

def generate_embeddings_for_existing_files():
    memory_files = [f for f in data_dir.glob("*.json") if f.is_file()]
    for file in memory_files:
        if not load_embeddings(file.name):
            get_embeddings(file.name, "nomic-embed-text")
    logging.info(f"Generated embeddings for {len(memory_files)} files")

# Run this function when the module is imported to ensure all files have embeddings
generate_embeddings_for_existing_files()
