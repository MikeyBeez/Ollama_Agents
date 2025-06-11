"""
Integration tests for the Memory System
"""

import os
import sys
import json
import asyncio
from datetime import datetime

# Add necessary paths
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
sys.path.insert(0, "/users/bard/mcp/chat_history")

from src.agents.memory_agent import MemoryAgent
from integrations.ollama_integration import OllamaIntegration

async def test_basic_storage():
    """Test basic conversation storage and retrieval."""
    print("\n🧪 Testing basic storage...")
    
    agent = MemoryAgent()
    test_conv = {
        "title": "Test Conversation 1",
        "messages": [
            {"role": "human", "content": "Hello, this is a test message"},
            {"role": "assistant", "content": "Hi! This is a test response"}
        ],
        "topics": ["testing", "memory", "integration"]
    }
    
    try:
        conv_id = agent.process_conversation(test_conv)
        print(f"✅ Successfully stored conversation: {conv_id}")
        return conv_id
    except Exception as e:
        print(f"❌ Storage test failed: {str(e)}")
        return None

async def test_search():
    """Test search functionality."""
    print("\n🧪 Testing search...")
    
    agent = MemoryAgent()
    try:
        results = agent.search_memories("test message")
        print(f"✅ Search successful - found {len(results)} results")
        for r in results:
            print(f"  - {r['title']}: {r['preview']}")
        return len(results) > 0
    except Exception as e:
        print(f"❌ Search test failed: {str(e)}")
        return False

async def test_integration():
    """Test Ollama integration."""
    print("\n🧪 Testing Ollama integration...")
    
    integration = OllamaIntegration()
    test_conv = {
        "title": "Integration Test",
        "messages": [
            {"role": "human", "content": "Testing the integration between systems"},
            {"role": "assistant", "content": "This is a response in the integration test"}
        ]
    }
    
    try:
        result = await integration.process_conversation(test_conv)
        print(f"✅ Integration test result: {result['status']}")
        return result['status'] == 'success'
    except Exception as e:
        print(f"❌ Integration test failed: {str(e)}")
        return False

async def test_topic_extraction():
    """Test automatic topic extraction."""
    print("\n🧪 Testing topic extraction...")
    
    agent = MemoryAgent()
    test_conv = {
        "title": "Topic Test",
        "messages": [
            {"role": "human", "content": "Let's discuss Python programming and artificial intelligence"},
            {"role": "assistant", "content": "Those are interesting topics in software development"}
        ]
    }
    
    try:
        conv_id = agent.process_conversation(test_conv)
        stored_conv = agent.memory_ops.get_conversation(conv_id)
        topics = stored_conv.get('topics', [])
        print(f"✅ Extracted topics: {topics}")
        return len(topics) > 0
    except Exception as e:
        print(f"❌ Topic extraction failed: {str(e)}")
        return False

async def test_summarization():
    """Test conversation summarization."""
    print("\n🧪 Testing summarization...")
    
    integration = OllamaIntegration()
    test_conv = {
        "messages": [
            {"role": "human", "content": "What's the weather like today?"},
            {"role": "assistant", "content": "It's sunny and warm, perfect for outdoor activities."},
            {"role": "human", "content": "Great! Any chance of rain later?"},
            {"role": "assistant", "content": "No rain forecast for today."}
        ]
    }
    
    try:
        result = await integration.summarize_conversation(test_conv)
        print(f"✅ Generated summary: {result.get('summary', 'No summary generated')}")
        return 'summary' in result
    except Exception as e:
        print(f"❌ Summarization failed: {str(e)}")
        return False

async def run_all_tests():
    """Run all tests and report results."""
    print("\n🚀 Starting Memory System Integration Tests...\n")
    
    results = {
        "storage": await test_basic_storage(),
        "search": await test_search(),
        "integration": await test_integration(),
        "topics": await test_topic_extraction(),
        "summary": await test_summarization()
    }
    
    print("\n📊 Test Results Summary:")
    for test, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status} - {test}")
    
    success_rate = sum(1 for r in results.values() if r) / len(results) * 100
    print(f"\nOverall Success Rate: {success_rate:.1f}%")

if __name__ == "__main__":
    asyncio.run(run_all_tests())