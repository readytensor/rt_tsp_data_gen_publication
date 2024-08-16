import json
import random
import hashlib
import numpy as np
from typing import Dict, Any


def load_config(config_file_path: str) -> Dict[str, Any]:
    """
    Load the TSP configuration from a JSON file.

    Args:
        config_file_path (str): The path to the JSON file containing the configuration.

    Returns:
        Dict[str, Any]: The configuration as a dictionary.
    """
    with open(config_file_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


def save_dict_as_json(data: Dict[str, Any], file_path: str) -> None:
    """
    Save a dictionary as a JSON file.

    Args:
        data (Dict[str, Any]): The dictionary to save.
        file_path (str): The path to save the JSON file.
    """
    with open(file_path, "w", encoding="utf-8") as f_h:
        json.dump(data, f_h, separators=(",", ":"))


def load_dict_from_json(file_path: str) -> Dict[str, Any]:
    """
    Load a dictionary from a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        Dict[str, Any]: The dictionary loaded from the JSON file.
    """
    with open(file_path, "r", encoding="utf-8") as f_h:
        data = json.load(f_h)
    return data


def set_seed(seed: int = 123) -> None:
    """
    Set the seed for reproducibility.

    Args:
        seed (int): The seed for the random number generator. Default is 123.
    """
    random.seed(seed)
    np.random.seed(seed)


def generate_hash(input_string: str) -> str:
    """
    Generate a unique hash given a string of text using MD5.

    Args:
        input_string (str): String of text to hash.

    Returns:
        str: Hexadecimal hash code of length 32.
    """
    # Create a new MD5 hash object
    hasher = hashlib.md5()
    # Encode the input string to bytes and update the hash object
    hasher.update(input_string.encode("utf-8"))
    # Return the hexadecimal representation of the digest
    return hasher.hexdigest()
