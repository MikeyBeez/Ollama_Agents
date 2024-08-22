import json
import os
from datetime import datetime
from pathlib import Path

def save_interaction(prompt, response, username, model_name):
    # Create the data directory if it doesn't exist
    project_root = Path(__file__).parent.parent.parent
    data_dir = project_root / "data" / "json_history"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.json"

    # Prepare the data to be saved
    data = {
        "timestamp": datetime.now().isoformat(),
        "username": username,
        "model_name": model_name,
        "prompt": prompt,
        "response": response,
        # Additional fields can be added here in the future
        # "chat_name": "",
        # "tool_results": [],
    }

    # Save the data as a JSON file
    file_path = data_dir / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

#    print(f"Interaction saved to {file_path}")

