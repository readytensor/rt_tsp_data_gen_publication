import os
from typing import List, Dict, Union, FrozenSet, Tuple
from utils import (
    generate_hash,
    save_dict_as_json,
    load_dict_from_json,
)


def save_generated_examples(
    scenario: str,
    description: str,
    tsp_examples: List[FrozenSet[Tuple[float, float]]],
    save_dir_path: str,
    coordinate_space_specs: Dict[str, float],
    num_nodes: int,
    total_samples: int,
    total_parts: int,
    part_number: int,
    sampling_method: str,
    metadata: Dict[str, Union[str, Dict[str, str]]]
) -> None:
    """
    Save generated TSP examples in JSON format.

    Args:
        scenario (str): The scenario name for the TSP problem.
        description (str): A description of the TSP scenario.
        tsp_examples (List[FrozenSet[Tuple[float, float]]]): List of TSP examples.
        save_dir_path (str): The directory path to save the JSON file.
        coordinate_space_specs (Dict[str, float]): Specifications of the coordinate space.
        num_nodes (int): The number of nodes in each example.
        total_samples (int): The total number of samples in the dataset.
        total_parts (int): The total number of files that will be generated.
        part_number (int): The number of the current part being generated.
        sampling_method (str): The method used for sampling points (e.g., "uniform").
        metadata (Dict[str, Union[str, Dict[str, str]]]): Metadata for the dataset.
    """
    json_save_dir = os.path.join(save_dir_path, scenario)
    os.makedirs(json_save_dir, exist_ok=True)

    tsp_problems = []
    for points in tsp_examples:
        sorted_points_list = sorted(list(points), key=lambda x: (x[0], x[1]))
        node_data = "\n".join(f"{i + 1} {x} {y}" for i, (x, y) in enumerate(sorted_points_list))
        tsp_hash = generate_hash("EUC_2D" + node_data)

        tsp_dict = {
            "name": tsp_hash,
            "node_coordinates": [[x, y] for x, y in sorted_points_list],
        }
        tsp_problems.append(tsp_dict)

    data = {
        "dataset_name": scenario,
        "description": description,
        "total_count": total_samples,
        "total_parts": total_parts,
        "part_number": part_number,
        "samples_in_part": len(tsp_problems),
        "number_of_nodes": num_nodes,
        "coordinate_space": coordinate_space_specs,
        "sampling_method": sampling_method,
        "metadata": metadata,
        "problems": tsp_problems
    }

    f_path = os.path.join(json_save_dir, f"{scenario}_{part_number}.json")
    save_dict_as_json(data, f_path)


def load_examples(file_path: str) -> Dict:
    """
    Load TSP examples from a file in the JSON format.

    Args:
        file_path (str): Path of the data file.

    Returns:
        Dict: Dictionary of examples.
    """
    return load_dict_from_json(file_path)
