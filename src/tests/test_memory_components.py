# src/tests/test_memory_components.py

import sys
import os
import traceback
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.save_history import save_interaction, get_chat_history, chat_history
from modules.memory_search import search_memories
from modules.kb_graph import create_edge, get_related_nodes, get_db_connection
from modules.assemble import assemble_prompt_with_history
from modules.cognitive_engine import process_query_and_generate_response
from modules.logging_setup import logger
from config import DEFAULT_MODEL

def run_test(test_func):
    try:
        test_func()
        print(f"{test_func.__name__} passed!")
    except Exception as e:
        print(f"{test_func.__name__} failed!")
        print(f"Error: {str(e)}")
        print("Traceback:")
        traceback.print_exc()

def test_save_history():
    logger.info("Starting test_save_history")
    chat_history.clear()
    logger.debug(f"Cleared chat history. Current length: {len(chat_history.history)}")

    save_interaction("What is the capital of France?", "The capital of France is Paris.", "TestUser", "TestModel")
    save_interaction("Tell me about the Eiffel Tower", "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris.", "TestUser", "TestModel")

    history = get_chat_history()
    logger.debug(f"Current chat history length: {len(history)}")

    assert len(history) == 2, f"Expected 2 history entries, but got {len(history)}"
    assert history[0]['prompt'] == "What is the capital of France?", "First prompt doesn't match"
    assert history[1]['response'].startswith("The Eiffel Tower"), "Second response doesn't match"

    logger.info("test_save_history completed")

def test_memory_search():
    logger.info("Starting test_memory_search")
    results = search_memories("Paris", top_k=2)

    logger.debug(f"Search results for 'Paris' (top {len(results)}):")
    for i, result in enumerate(results):
        logger.debug(f"Result {i+1}: {str(result)[:100]}...")

    if len(results) > 0:
        assert any("paris" in str(result.get('content', '')).lower() for result in results), "Expected to find 'Paris' in search results"
    else:
        logger.warning("No search results found. This could be normal if no relevant memories exist.")

    logger.info("test_memory_search completed")

def test_kb_graph():
    logger.info("Starting test_kb_graph")
    create_edge("paris", "france", "CAPITAL_OF", 1.0)
    create_edge("eiffel_tower", "paris", "LOCATED_IN", 1.0)

    paris_relations = get_related_nodes("paris")

    logger.debug("Relations for 'paris':")
    for relation in paris_relations:
        logger.debug(f"  {relation[0]} - {relation[1]} - {relation[2]}")

    assert len(paris_relations) == 2, f"Expected 2 relations for Paris, but got {len(paris_relations)}"
    assert any(relation[1] == "CAPITAL_OF" for relation in paris_relations), "Expected CAPITAL_OF relation"
    assert any(relation[1] == "LOCATED_IN" for relation in paris_relations), "Expected LOCATED_IN relation"

    logger.info("test_kb_graph completed")

def test_assemble_prompt():
    logger.info("Starting test_assemble_prompt")
    chat_history.clear()
    save_interaction("What is the capital of France?", "The capital of France is Paris.", "TestUser", "TestModel")
    save_interaction("Tell me about the Eiffel Tower", "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris.", "TestUser", "TestModel")

    current_prompt = "What are some famous landmarks in Paris?"
    assembled_prompt = assemble_prompt_with_history(current_prompt)

    logger.debug(f"Assembled prompt (first 300 chars):\n{assembled_prompt[:300]}...")

    assert "User: What is the capital of France?" in assembled_prompt, "Expected first interaction in assembled prompt"
    assert "User: Tell me about the Eiffel Tower" in assembled_prompt, "Expected second interaction in assembled prompt"
    assert "User: What are some famous landmarks in Paris?" in assembled_prompt, "Expected current prompt in assembled prompt"
    assert "Relevant Memories:" in assembled_prompt, "Expected relevant memories in assembled prompt"
    assert "Knowledge Graph Relations:" in assembled_prompt, "Expected knowledge graph relations in assembled prompt"

    logger.info("test_assemble_prompt completed")

def test_cognitive_engine():
    logger.info("Starting test_cognitive_engine")
    user_input = "What are some famous landmarks in Paris?"
    model_name = DEFAULT_MODEL
    context = ""
    conversation_history = [
        {"prompt": "What is the capital of France?", "response": "The capital of France is Paris."},
        {"prompt": "Tell me about the Eiffel Tower", "response": "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris."}
    ]
    bullet_points = []
    agent_name = "TestAgent"

    result = process_query_and_generate_response(user_input, model_name, context, conversation_history, bullet_points, agent_name)

    assert 'response' in result, "Expected 'response' in result"
    assert 'input_analysis' in result, "Expected 'input_analysis' in result"
    assert 'query_info' in result, "Expected 'query_info' in result"
    assert 'memory_results' in result, "Expected 'memory_results' in result"
    assert 'kg_relations' in result, "Expected 'kg_relations' in result"

    logger.info("test_cognitive_engine completed")

def run_all_tests():
    logger.info("Starting all tests")
    run_test(test_save_history)
    run_test(test_memory_search)
    run_test(test_kb_graph)
    run_test(test_assemble_prompt)
    run_test(test_cognitive_engine)
    logger.info("All tests completed")

if __name__ == "__main__":
    run_all_tests()
