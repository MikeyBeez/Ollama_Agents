# file_utils.py

import json
from pathlib import Path
import logging
from typing import Dict, Any, List

def read_json_file(file_path: Path) -> Dict[str, Any]:
    """
    Read and parse a JSON file.

    Args:
        file_path (Path): Path to the JSON file.

    Returns:
        Dict[str, Any]: Parsed JSON data as a dictionary.
    """
    try:
        with file_path.open('r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON from file: {file_path}")
        return {}
    except IOError:
        logging.error(f"Error reading file: {file_path}")
        return {}

def write_json_file(file_path: Path, data: Dict[str, Any]):
    """
    Write data to a JSON file.

    Args:
        file_path (Path): Path to the JSON file.
        data (Dict[str, Any]): Data to write to the file.
    """
    try:
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError:
        logging.error(f"Error writing to file: {file_path}")

def ensure_directory_exists(directory: Path):
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        directory (Path): Path to the directory.
    """
    directory.mkdir(parents=True, exist_ok=True)

def get_json_files_in_directory(directory: Path) -> List[Path]:
    """
    Get a list of all JSON files in a directory.

    Args:
        directory (Path): Path to the directory.

    Returns:
        List[Path]: List of paths to JSON files.
    """
    return list(directory.glob("*.json"))

def increment_json_field(file_path: Path, field_name: str, increment: int = 1) -> Dict[str, Any]:
    """
    Increment a numeric field in a JSON file.

    Args:
        file_path (Path): Path to the JSON file.
        field_name (str): Name of the field to increment.
        increment (int): Value to increment by (default is 1).

    Returns:
        Dict[str, Any]: Updated JSON data.
    """
    data = read_json_file(file_path)
    if field_name in data:
        data[field_name] = data[field_name] + increment
    else:
        data[field_name] = increment
    write_json_file(file_path, data)
    return data
