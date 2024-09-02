# file_utils.py

import json
from pathlib import Path
from typing import Dict, Any, List
from src.modules.logging_setup import logger
from src.modules.errors import FileOperationError

def read_json_file(file_path: Path) -> Dict[str, Any]:
    """
    Read and parse a JSON file.

    Args:
        file_path (Path): Path to the JSON file.

    Returns:
        Dict[str, Any]: Parsed JSON data as a dictionary.
    """
    logger.info(f"Attempting to read JSON file: {file_path}")
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
        logger.debug(f"Successfully read JSON file: {file_path}")
        return data
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from file: {file_path}. Error: {str(e)}")
        raise FileOperationError(f"Failed to decode JSON from {file_path}: {str(e)}")
    except IOError as e:
        logger.error(f"IOError reading file: {file_path}. Error: {str(e)}")
        raise FileOperationError(f"Failed to read file {file_path}: {str(e)}")

def write_json_file(file_path: Path, data: Dict[str, Any]):
    """
    Write data to a JSON file.

    Args:
        file_path (Path): Path to the JSON file.
        data (Dict[str, Any]): Data to write to the file.
    """
    logger.info(f"Attempting to write JSON file: {file_path}")
    try:
        with file_path.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.debug(f"Successfully wrote JSON file: {file_path}")
    except IOError as e:
        logger.error(f"IOError writing to file: {file_path}. Error: {str(e)}")
        raise FileOperationError(f"Failed to write to file {file_path}: {str(e)}")

def ensure_directory_exists(directory: Path):
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        directory (Path): Path to the directory.
    """
    logger.info(f"Ensuring directory exists: {directory}")
    try:
        directory.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Directory ensured: {directory}")
    except OSError as e:
        logger.error(f"Error creating directory: {directory}. Error: {str(e)}")
        raise FileOperationError(f"Failed to create directory {directory}: {str(e)}")

def get_json_files_in_directory(directory: Path) -> List[Path]:
    """
    Get a list of all JSON files in a directory.

    Args:
        directory (Path): Path to the directory.

    Returns:
        List[Path]: List of paths to JSON files.
    """
    logger.info(f"Getting JSON files from directory: {directory}")
    try:
        json_files = list(directory.glob("*.json"))
        logger.debug(f"Found {len(json_files)} JSON files in {directory}")
        return json_files
    except Exception as e:
        logger.error(f"Error listing JSON files in directory: {directory}. Error: {str(e)}")
        raise FileOperationError(f"Failed to list JSON files in {directory}: {str(e)}")

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
    logger.info(f"Incrementing field '{field_name}' in file: {file_path}")
    try:
        data = read_json_file(file_path)
        if field_name in data:
            data[field_name] = data[field_name] + increment
            logger.debug(f"Incremented '{field_name}' from {data[field_name] - increment} to {data[field_name]}")
        else:
            data[field_name] = increment
            logger.debug(f"Created new field '{field_name}' with value {increment}")
        write_json_file(file_path, data)
        return data
    except FileOperationError as e:
        logger.error(f"Error incrementing field in JSON file: {file_path}. Error: {str(e)}")
        raise
