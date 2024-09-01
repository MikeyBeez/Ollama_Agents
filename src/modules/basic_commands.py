from rich.console import Console
from src.modules.ddg_search import DDGSearch

console = Console()
ddg_search = DDGSearch()

def change_model_command(command: str) -> str:
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
        from src.modules.save_history import save_document_chunk
        from config import USER_NAME, DEFAULT_MODEL
        save_document_chunk(f"DDG_Search_{USER_NAME}", f"Query: {query}\nResults: {result_text}", USER_NAME, DEFAULT_MODEL)
        console.print("\nSearch results added to chat history.", style="bold green")

    except IndexError:
        console.print("Error: Please provide a search query. Usage: /s your search query", style="bold red")
    except Exception as e:
        console.print(f"An error occurred: {str(e)}", style="bold red")

    return 'CONTINUE'
