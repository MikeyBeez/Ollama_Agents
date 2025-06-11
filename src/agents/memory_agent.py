"""
Memory Agent for processing and managing conversation history.
Integrates with Claude's Chat History system and handles efficient memory operations.
"""

import os
import sys
from typing import Dict, List, Optional
import json
from datetime import datetime

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.modules.base_agent import BaseAgent
from src.modules.logging_setup import logger
from src.modules.errors import OllamaAgentsError
from src.modules.config_manager import ConfigManager
from langchain.llms import Ollama

class MemoryOperations:
    def __init__(self, storage_dir: str = "/users/bard/mcp/chat_history/data"):
        self.storage_dir = storage_dir
        self.conversations_dir = os.path.join(storage_dir, "conversations")
        self.index_path = os.path.join(storage_dir, "index.json")
        self.ensure_directories()

    def ensure_directories(self):
        """Create necessary directories if they don't exist."""
        os.makedirs(self.storage_dir, exist_ok=True)
        os.makedirs(self.conversations_dir, exist_ok=True)
        if not os.path.exists(self.index_path):
            with open(self.index_path, 'w') as f:
                json.dump({
                    "conversations": [],
                    "last_updated": datetime.now().isoformat(),
                    "version": "1.0.0"
                }, f)

    def store_conversation(self, conversation: Dict) -> str:
        """Store a conversation and update the index."""
        conv_id = str(int(datetime.now().timestamp()))
        
        # Prepare conversation data
        conv_data = {
            "id": conv_id,
            "timestamp": datetime.now().isoformat(),
            "title": conversation.get("title", "Untitled Conversation"),
            "summary": conversation.get("summary", ""),
            "topics": conversation.get("topics", []),
            "messages": conversation.get("messages", []),
            "metadata": {
                "message_count": len(conversation.get("messages", [])),
                "participants": list(set(msg["role"] for msg in conversation.get("messages", []))),
                "last_updated": datetime.now().isoformat()
            }
        }

        # Save conversation
        conv_path = os.path.join(self.conversations_dir, f"{conv_id}.json")
        with open(conv_path, 'w') as f:
            json.dump(conv_data, f, indent=2)

        # Update index
        with open(self.index_path, 'r') as f:
            index = json.load(f)
        
        index["conversations"].append({
            "id": conv_id,
            "title": conv_data["title"],
            "timestamp": conv_data["timestamp"],
            "topics": conv_data["topics"]
        })
        index["last_updated"] = datetime.now().isoformat()
        
        with open(self.index_path, 'w') as f:
            json.dump(index, f, indent=2)

        return conv_id

    def get_conversation(self, conv_id: str) -> Optional[Dict]:
        """Retrieve a specific conversation."""
        conv_path = os.path.join(self.conversations_dir, f"{conv_id}.json")
        if os.path.exists(conv_path):
            with open(conv_path, 'r') as f:
                return json.load(f)
        return None

    def search_conversations(self, query: str, topics: Optional[List[str]] = None) -> List[Dict]:
        """Search conversations by content and/or topics."""
        results = []
        with open(self.index_path, 'r') as f:
            index = json.load(f)

        for conv_info in index["conversations"]:
            conv = self.get_conversation(conv_info["id"])
            if not conv:
                continue

            # Check if conversation matches search criteria
            if ((query.lower() in conv["title"].lower() or
                 any(query.lower() in msg["content"].lower() 
                     for msg in conv["messages"])) or
                (topics and any(topic in conv["topics"] 
                              for topic in topics))):
                
                results.append({
                    "id": conv["id"],
                    "title": conv["title"],
                    "timestamp": conv["timestamp"],
                    "preview": next(
                        (msg["content"][:100] + "..."
                         for msg in conv["messages"]
                         if query.lower() in msg["content"].lower()),
                        "No preview available"
                    )
                })

        return results

class MemoryAgent(BaseAgent):
    def __init__(self, config: Optional[ConfigManager] = None):
        super().__init__(config or ConfigManager())
        self.memory_ops = MemoryOperations()
        self.llm = Ollama(model=self.config.OLLAMA_MODEL)
        self.system_prompt = """You are a memory management agent. Your role is to:
1. Process and store conversations
2. Generate summaries
3. Extract relevant topics
4. Help retrieve relevant information
Be precise and efficient in your operations."""
        
    def summarize_conversation(self, messages: List[Dict]) -> str:
        """Generate a summary of the conversation using the local LLM."""
        try:
            conversation_text = "\n".join(
                f"{msg['role']}: {msg['content']}" for msg in messages
            )
            prompt = f"""Please summarize this conversation concisely:

Conversation:
{conversation_text}

Summary:"""
            
            response = self.llm(prompt)
            return response.strip()
        except Exception as e:
            logger.error(f"Error summarizing conversation: {str(e)}")
            return "Error generating summary"

    def extract_topics(self, messages: List[Dict]) -> List[str]:
        """Extract relevant topics from the conversation using the local LLM."""
        try:
            conversation_text = "\n".join(
                f"{msg['role']}: {msg['content']}" for msg in messages
            )
            
            prompt = f"""Extract 3-5 main topics from this conversation. 
            Return only the topics as a comma-separated list.
            Example output: python, machine learning, data analysis
            
            Conversation:
            {conversation_text}
            
            Topics:"""
            
            response = self.llm(prompt)
            
            # Process the response
            topics = [
                topic.strip() 
                for topic in response.split(',') 
                if topic.strip()
            ]
            
            # Ensure we have at least some topics
            if not topics:
                # Extract basic topics based on keyword frequency
                words = conversation_text.lower().split()
                # Filter out common words and get most frequent
                common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
                word_freq = {}
                for word in words:
                    if word not in common_words and len(word) > 3:
                        word_freq[word] = word_freq.get(word, 0) + 1
                topics = [word for word, _ in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:3]]
            
            logger.info(f"Extracted topics: {topics}")
            return topics[:self.config.MAX_TOPICS_PER_CONV]
            
        except Exception as e:
            logger.error(f"Error extracting topics: {str(e)}")
            # Return basic topics based on the first message
            first_msg = messages[0]['content'] if messages else ""
            words = first_msg.split()[:3]
            return [word for word in words if len(word) > 3][:3]

    def process_conversation(self, conversation: Dict) -> str:
        """Process and store a conversation with enhanced metadata."""
        try:
            # Generate summary if not provided
            if not conversation.get("summary"):
                conversation["summary"] = self.summarize_conversation(
                    conversation.get("messages", [])
                )

            # Extract topics if not provided
            if not conversation.get("topics"):
                conversation["topics"] = self.extract_topics(
                    conversation.get("messages", [])
                )

            # Store the enhanced conversation
            conv_id = self.memory_ops.store_conversation(conversation)
            return conv_id

        except Exception as e:
            logger.error(f"Error processing conversation: {str(e)}")
            raise OllamaAgentsError(f"Failed to process conversation: {str(e)}")

    def search_memories(self, query: str, topics: Optional[List[str]] = None) -> List[Dict]:
        """Search through stored conversations."""
        try:
            results = self.memory_ops.search_conversations(query, topics)
            return results
        except Exception as e:
            logger.error(f"Error searching memories: {str(e)}")
            raise OllamaAgentsError(f"Failed to search memories: {str(e)}")

    async def process_input(self, user_input: str) -> str:
        """Process user input and return appropriate response."""
        try:
            if user_input.lower().startswith('search:'):
                query = user_input[7:].strip()
                results = self.search_memories(query)
                return self.format_search_results(results)
            
            elif user_input.lower().startswith('store:'):
                content = user_input[6:].strip()
                conv = {
                    "title": "User Input Storage",
                    "messages": [
                        {"role": "human", "content": content}
                    ]
                }
                conv_id = self.process_conversation(conv)
                return f"Stored conversation with ID: {conv_id}"
            
            elif user_input.lower() == 'help':
                return self.get_help_text()
            
            else:
                return ("Invalid command. Type 'help' for available commands.\n"
                       "Available commands:\n"
                       "- search: <query>\n"
                       "- store: <content>\n"
                       "- help")

        except Exception as e:
            logger.error(f"Error processing input: {str(e)}")
            return f"Error processing your request: {str(e)}"

    def format_search_results(self, results: List[Dict]) -> str:
        """Format search results for display."""
        if not results:
            return "No matching conversations found."
        
        formatted = "Found conversations:\n\n"
        for result in results:
            formatted += f"ID: {result['id']}\n"
            formatted += f"Title: {result['title']}\n"
            formatted += f"Time: {result['timestamp']}\n"
            formatted += f"Preview: {result['preview']}\n\n"
        return formatted

    def get_help_text(self) -> str:
        """Return help text for the memory agent."""
        return """
Memory Agent Help:

Commands:
- search: <query>    Search through stored conversations
- store: <content>   Store new content in memory
- help              Show this help message

Examples:
- search: python programming
- store: This is an important note about AI
        """

def main():
    """Main function to run the memory agent."""
    try:
        agent = MemoryAgent()
        logger.info("Memory Agent initialized")
        
        # Example usage
        conv = {
            "title": "Test Conversation",
            "messages": [
                {"role": "human", "content": "Hello, this is a test."},
                {"role": "assistant", "content": "Hi! Yes, I'm here to help test the memory system."}
            ]
        }
        
        # Process and store the conversation
        conv_id = agent.process_conversation(conv)
        logger.info(f"Stored conversation with ID: {conv_id}")
        
        # Search test
        results = agent.search_memories("test")
        logger.info(f"Search results: {results}")

    except Exception as e:
        logger.error(f"Error in memory agent: {str(e)}")
        raise

if __name__ == "__main__":
    main()