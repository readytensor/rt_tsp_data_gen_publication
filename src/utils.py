import json
import random
import hashlib
import numpy as np
from typing import Dict


def load_config(config_file_path: str) -> Dict:
    """
    Load the TSP configuration from a JSON file.

    Args:
    - config_file_path (str): The path to the JSON file containing the configuration.

    Returns:
    - config (Dict): The configuration as a dictionary.
    """
    with open(config_file_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    return config


def save_dict_as_json(data: Dict, file_path: str) -> None:
    """
    Save a dictionary as a JSON file.

    Args:
    - data (Dict): The dictionary to save.
    - file_path (str): The path to save the JSON file.
    """

    with open(file_path, "w", encoding="utf-8") as f_h:
        json.dump(data, f_h, separators=(",", ":"))


def load_dict_from_json(file_path: str) -> Dict:
    """
    Load a dictionary from a JSON file.

    Args:
    - file_path (str): The path to the JSON file.

    Returns:
    - data (Dict): The dictionary loaded from the JSON file.
    """
    with open(file_path, "r") as f_h:
        data = json.load(f_h)
    return data


def set_seed(seed: int = 123):
    """
    Set the seed for reproducibility.

    Args:
    - seed (int): The seed for the random number generator.
    """
    random.seed(seed)
    np.random.seed(seed)


def generate_hash(input_string):
    """
    Generate a unique hash given a string of text.
    md5 is used to generate the hash code.

    Args:
        input_string (str): String of text to hash.

    Returns:
        str: hexadecimal hash code of length 32.
    """
    # Create a new MD5 hash object
    hasher = hashlib.md5()
    # Encode the input string to bytes and update the hash object with the bytes
    hasher.update(input_string.encode("utf-8"))
    # Return the hexadecimal representation of the digest - 32 character length
    return hasher.hexdigest()
