# src/modules/save_history.py

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Tuple
from config import MEMORY_LENGTH, DATA_DIR, CHAT_HISTORY_FILE
from .file_utils import read_json_file, write_json_file, ensure_directory_exists
from .logging_setup import logger
from .kb_graph import create_edge, get_db_connection

class ChatHistory:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ChatHistory, cls).__new__(cls)
            cls._instance.max_length = MEMORY_LENGTH
            cls._instance.history = []
            cls._instance.file_path = CHAT_HISTORY_FILE
            cls._instance.load_history()
        return cls._instance

    def add_entry(self, prompt: str, response: str):
        logger.debug(f"Adding new entry to chat history: prompt='{prompt[:50]}...', response='{response[:50]}...'")
        self.history.append({"prompt": prompt, "response": response})
        if len(self.history) > self.max_length:
            self.history.pop(0)
        self.save_history()
        logger.info(f"Added new entry to chat history. Total entries: {len(self.history)}")

        # Add entry to edge-based knowledge graph
        self.add_to_edge_kb(prompt, response)

    def get_history(self):
        return self.history

    def clear(self):
        self.history = []
        self.save_history()
        logger.info("Chat history cleared")

    def save_history(self):
        logger.debug(f"Saving chat history to {self.file_path}")
        write_json_file(self.file_path, self.history)
        logger.info(f"Saved chat history to {self.file_path}")

    def load_history(self):
        if self.file_path.exists():
            loaded_history = read_json_file(self.file_path)
            self.history = [
                {"prompt": entry["prompt"], "response": entry["response"]}
                for entry in loaded_history
                if isinstance(entry, dict) and "prompt" in entry and "response" in entry
            ][-self.max_length:]
            logger.info(f"Loaded {len(self.history)} entries from chat history")
        else:
            logger.warning(f"Chat history file not found at {self.file_path}")

    def add_to_edge_kb(self, prompt: str, response: str):
        """
        Add the prompt-response pair to the edge-based knowledge graph.
        """
        prompt_id = hashlib.md5(prompt.encode()).hexdigest()
        response_id = hashlib.md5(response.encode()).hexdigest()

        # Create edges for prompt and response
        create_edge(prompt_id, response_id, "PROMPT_RESPONSE", 1.0)

        # TODO: Implement more sophisticated edge creation based on content analysis
        # For example, extract entities or topics from prompt and response
        # and create edges between them and the prompt/response nodes

chat_history = ChatHistory()

def save_memory(memory_type: str, content: Dict[str, Any], username: str, model_name: str, metadata: Dict[str, Any] = None):
    ensure_directory_exists(DATA_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{memory_type}.json"
    data = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "model_name": model_name,
        "type": memory_type,
        "content": content,
        "access_count": 0,
        "permanent_marker": 0
    }
    if metadata:
        data.update(metadata)
    file_path = DATA_DIR / filename
    write_json_file(file_path, data)
    logger.info(f"Saved {memory_type} memory: {filename}")

    # Add to edge-based knowledge graph
    add_memory_to_edge_kb(data)

def save_interaction(prompt: str, response: str, username: str, model_name: str):
    logger.debug(f"Saving interaction: prompt='{prompt[:50]}...', response='{response[:50]}...', username='{username}', model='{model_name}'")
    chat_history.add_entry(prompt, response)
    save_memory("interaction", {"prompt": prompt, "response": response}, username, model_name)
    logger.debug(f"Saved interaction for user {username}")

def save_document_chunk(chunk_id: str, chunk_content: str, username: str, model_name: str):
    save_memory("document_chunk", chunk_content, username, model_name, {"chunk_id": chunk_id})
    logger.debug(f"Saved document chunk {chunk_id} for user {username}")

def get_chat_history():
    return chat_history.get_history()

def add_memory_to_edge_kb(memory_data: Dict[str, Any]):
    """
    Add a memory entry to the edge-based knowledge graph.
    """
    memory_id = hashlib.md5(json.dumps(memory_data, sort_keys=True).encode()).hexdigest()

    # Create edges based on memory type
    if memory_data['type'] == 'interaction':
        prompt_id = hashlib.md5(memory_data['content']['prompt'].encode()).hexdigest()
        response_id = hashlib.md5(memory_data['content']['response'].encode()).hexdigest()
        create_edge(memory_id, prompt_id, "CONTAINS_PROMPT", 1.0)
        create_edge(memory_id, response_id, "CONTAINS_RESPONSE", 1.0)
    elif memory_data['type'] == 'document_chunk':
        chunk_id = memory_data['chunk_id']
        create_edge(memory_id, chunk_id, "CONTAINS_CHUNK", 1.0)

    # Create edges for metadata
    create_edge(memory_id, memory_data['username'], "CREATED_BY", 1.0)
    create_edge(memory_id, memory_data['model_name'], "USED_MODEL", 1.0)

    # TODO: Implement more sophisticated edge creation based on content analysis
    # For example, extract entities or topics from the memory content
    # and create edges between them and the memory node

def get_related_memories(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve related memories from the edge-based knowledge graph.
    """
    query_id = hashlib.md5(query.encode()).hexdigest()
    conn = get_db_connection()
    cursor = conn.cursor()

    # This is a simplified query. In a more advanced implementation,
    # you might want to use more sophisticated graph traversal algorithms.
    cursor.execute("""
        SELECT e.target_id, e.relationship_type, e.strength
        FROM edges e
        WHERE e.source_id = ?
        ORDER BY e.strength DESC
        LIMIT ?
    """, (query_id, top_k))

    related_nodes = cursor.fetchall()
    conn.close()

    related_memories = []
    for node_id, relationship_type, strength in related_nodes:
        memory_data = read_json_file(DATA_DIR / f"{node_id}.json")
        related_memories.append({
            "content": memory_data.get("content", ""),
            "type": memory_data.get("type", "unknown"),
            "relationship": relationship_type,
            "strength": strength
        })

    return related_memories
