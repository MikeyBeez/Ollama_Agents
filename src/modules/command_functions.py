import os
from typing import List
from rich.console import Console
from rich.text import Text
from src.modules.memory_search import search_memories, save_embeddings
from src.modules.save_history import save_document_chunk, get_chat_history, chat_history
from src.modules.ollama_client import process_prompt
from src.modules.ddg_search import DDGSearch
from config import USER_NAME, DEFAULT_MODEL, CHUNK_SIZE, CHUNK_OVERLAP, AGENT_NAME
import ollama
import traceback

console = Console()
ddg_search = DDGSearch()

def pick_file() -> str:
    current_dir = os.path.expanduser("~")
    while True:
        console.print(f"\nCurrent directory: {current_dir}", style="bold blue")
        console.print("Directories:", style="bold green")
        dirs = [d for d in os.listdir(current_dir) if os.path.isdir(os.path.join(current_dir, d))]
        for i, d in enumerate(dirs, 1):
            console.print(f"{i}. 📁 {d}")
        console.print("\nFiles:", style="bold green")
        files = [f for f in os.listdir(current_dir) if os.path.isfile(os.path.join(current_dir, f))]
        for i, f in enumerate(files, len(dirs)+1):
            console.print(f"{i}. 📄 {f}")

        choice = console.input("\nEnter number to select, '..' to go up, 'q' to quit, or full path of file: ")
        if choice.lower() == 'q':
            return None
        elif choice == '..':
            current_dir = os.path.dirname(current_dir)
        elif choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(dirs):
                current_dir = os.path.join(current_dir, dirs[choice-1])
            elif len(dirs) < choice <= len(dirs) + len(files):
                return os.path.join(current_dir, files[choice-len(dirs)-1])
        elif os.path.isfile(choice):
            return choice
        else:
            console.print("Invalid selection. Please try again.", style="bold red")

def chunk_document(file_path: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    chunks = []
    start = 0
    while start < len(content):
        end = start + chunk_size
        chunk = content[start:end]

        # Ensure chunks end at sentence boundaries
        if end < len(content):
            last_period = chunk.rfind('.')
            if last_period != -1:
                end = start + last_period + 1
                chunk = content[start:end]

        chunks.append(chunk)
        start = end - overlap
    return chunks

def generate_embeddings(text: str, model: str) -> List[float]:
    return ollama.embeddings(model=model, prompt=text)["embedding"]

def upload_document(command: str) -> str:
    file_path = pick_file()
    if not file_path:
        console.print("Upload cancelled.", style="bold red")
        return 'CONTINUE'

    console.print(f"Processing file: {file_path}", style="bold green")
    chunks = chunk_document(file_path)

    for i, chunk in enumerate(chunks):
        chunk_id = f"{os.path.basename(file_path)}_chunk_{i+1}"

        # Save chunk as a separate memory
        save_document_chunk(chunk_id, chunk, USER_NAME, DEFAULT_MODEL)

        # Generate and save embeddings
        embeddings = generate_embeddings(chunk, DEFAULT_MODEL)
        save_embeddings(chunk_id, embeddings)

    console.print(f"Uploaded and processed {len(chunks)} chunks from {os.path.basename(file_path)}", style="bold green")
    return 'CONTINUE'

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

        console.print(f"Searching for top {top_k} memories with similarity above {similarity_threshold*100}%", style="bold yellow")
        memories = search_memories(query, top_k=top_k, similarity_threshold=similarity_threshold)

        console.print(f"Received {len(memories)} memories from search_memories", style="bold cyan")

        if not memories:
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

    except ValueError as e:
        console.print(f"Error: {str(e)}. Usage: /ms n m query (where n is the number of memories, m is the similarity threshold between 0 and 1, and query is your question)", style="bold red")
    except Exception as e:
        console.print(f"An error occurred: {str(e)}", style="bold red")
        console.print("Traceback:", style="bold red")
        console.print(traceback.format_exc(), style="red")

    return 'CONTINUE'

def print_history() -> str:
    history = get_chat_history()
    if not history:
        console.print("No chat history available.", style="bold green")
        return 'CONTINUE'

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

        # Implement the actual truncation logic here
        chat_history.history = chat_history.history[-n:]
        chat_history.save_history()

        console.print(f"Chat history truncated to last {n} entries.", style="bold green")
    except IndexError:
        console.print("Error: Please provide the number of entries to keep. Usage: /tr n", style="bold red")
    except ValueError as e:
        console.print(f"Error: {str(e)}. Please provide a valid non-negative integer.", style="bold red")
    return 'CONTINUE'

def change_model_command(command: str) -> str:
    # Implement the logic to change the model
    console.print("Model change functionality not implemented yet.", style="bold yellow")
    return 'CONTINUE'

def duck_duck_go_search(command: str) -> str:
    try:
        query = command.split(maxsplit=1)[1]
        console.print(f"Searching DuckDuckGo for: {query}", style="bold yellow")
        results = ddg_search.run_search(query)

        if not results:
            console.print("No results found.", style="bold red")
            return 'CONTINUE'

        result_text = "\n".join(results)
        console.print("Search Results:", style="bold green")
        console.print(result_text, style="cyan")

        # Add the search query and results to chat history
        save_document_chunk(f"DDG_Search_{USER_NAME}", f"Query: {query}\nResults: {result_text}", USER_NAME, DEFAULT_MODEL)
        console.print("\nSearch results added to chat history.", style="bold green")

    except IndexError:
        console.print("Error: Please provide a search query. Usage: /s your search query", style="bold red")
    except Exception as e:
        console.print(f"An error occurred: {str(e)}", style="bold red")

    return 'CONTINUE'
