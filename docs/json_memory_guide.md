# 📁 Ollama_Agents: JSON Memory Files Guide

## 1. 📊 Overview

Ollama_Agents uses JSON files to store memories, which include conversation history, document chunks, and other relevant information. These files are crucial for the AI's long-term memory and context understanding.

## 2. 🗂️ File Structure

Each memory is stored as a separate JSON file in the `data/json_history` directory. The filename format is:

```
YYYYMMDD_HHMMSS_<memory_type>.json
```

For example: `20230515_143022_interaction.json`

## 3. 📄 JSON Structure

Here's a typical structure of a memory JSON file:

```json
{
  "timestamp": "2023-05-15T14:30:22.123456",
  "username": "User123",
  "model_name": "llama3.1:latest",
  "type": "interaction",
  "content": {
    "prompt": "What is the capital of France?",
    "response": "The capital of France is Paris."
  },
  "access_count": 3,
  "permanent_marker": 0,
  "embedding": [0.1, 0.2, 0.3, ..., 0.9]
}
```

## 4. 🔑 Key Fields

### 4.1 timestamp
- Format: ISO 8601 (YYYY-MM-DDTHH:MM:SS.mmmmmm)
- Purpose: Used for chronological ordering and age-based pruning

### 4.2 username
- Purpose: Identifies the user associated with the memory

### 4.3 model_name
- Purpose: Specifies the AI model used for this interaction

### 4.4 type
- Possible values: "interaction", "document_chunk"
- Purpose: Distinguishes between different types of memories

### 4.5 content
- For interactions: Contains "prompt" and "response"
- For document chunks: Contains the text content of the chunk

### 4.6 access_count
- Purpose: Tracks how often this memory has been accessed
- Usage: Can be used for relevance-based pruning (higher count = more relevant)

### 4.7 permanent_marker
- Values: 0 (not permanent) or 1 (permanent)
- Purpose: Flags memories that should never be pruned

### 4.8 embedding
- Purpose: Vector representation of the memory content for similarity search

## 5. 🔄 Memory Management

### 5.1 Updating Access Count
- The `access_count` is incremented each time the memory is retrieved or used in a search

### 5.2 Setting Permanent Marker
- Important memories can be marked as permanent (e.g., user preferences, critical information)
- Set `permanent_marker` to 1 for these memories

## 6. 🗑️ Future Pruning Strategies

These fields can be used to implement various pruning strategies:

1. **Age-based pruning**: Remove memories older than a certain date using the `timestamp`
2. **Relevance-based pruning**: Remove memories with low `access_count`
3. **Type-based pruning**: Prune certain types of memories based on the `type` field
4. **Model-specific pruning**: Remove memories associated with deprecated models using `model_name`
5. **Selective preservation**: Never prune memories with `permanent_marker` set to 1

## 7. 📈 Memory Analytics

The JSON structure allows for easy analytics:

- Track user activity by analyzing memories per `username`
- Measure model usage patterns using the `model_name` field
- Identify frequently accessed information via `access_count`

## 8. 🔒 Security Considerations

- Ensure that sensitive information is not stored in plain text in the `content` field
- Implement access controls to protect user-specific memories

## 9. 🚀 Future Enhancements

- Implement a scoring system combining `timestamp` and `access_count` for more nuanced pruning
- Add a `last_accessed` field to track recency of memory usage
- Introduce a `relevance_score` field updated by the AI based on context relevance

Remember to update this guide as new fields or management strategies are implemented in the Ollama_Agents system.
