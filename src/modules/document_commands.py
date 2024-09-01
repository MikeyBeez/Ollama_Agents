# src/modules/document_commands.py

import os
from typing import List
from rich.console import Console
from src.modules.memory_search import save_embeddings
from src.modules.save_history import save_document_chunk
from src.modules.chunk_history import add_to_chunk_history, get_chunk_history
from config import USER_NAME, DEFAULT_MODEL, CHUNK_SIZE, CHUNK_OVERLAP
import ollama

console = Console()

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

        # Add chunk to chunk history
        add_to_chunk_history(chunk)

    console.print(f"Uploaded and processed {len(chunks)} chunks from {os.path.basename(file_path)}", style="bold green")
    return 'CONTINUE'

def print_chunk_history(command: str = '') -> str:
    chunks = get_chunk_history()
    if not chunks:
        console.print("No chunk history available.", style="bold green")
        return 'CONTINUE'

    console.print("Chunk History:", style="bold green")
    for i, chunk in enumerate(chunks, 1):
        console.print(f"\n--- Chunk {i} ---", style="bold blue")
        console.print(chunk[:100] + "..." if len(chunk) > 100 else chunk, style="yellow")

    console.print(f"\nTotal chunks in history: {len(chunks)}", style="bold purple")

    return 'CONTINUE'