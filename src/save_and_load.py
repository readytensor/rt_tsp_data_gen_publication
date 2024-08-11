import os
from typing import List, Dict, Union
from utils import (
    generate_hash,
    save_dict_as_json,
    load_dict_from_json,
)


def save_generated_examples(
    scenario: str,
    tsp_examples: list,
    save_dir_path: str,
    grid_specs: dict,
    total_samples: int,
    total_parts: int,
    part_number: int,
    num_cities_per_example: Union[int, List[int]],
) -> None:
    """
    Save all TSP examples in the specified format.

    Args:
    - scenario (str): The scenario for the TSP problem
    - tsp_examples (list of sets of tuples): Each element is a set of tuples with x, y coordinates.
    - save_dir_path (str): The directory path to save the examples.
    - grid_specs (dict): Grid specifications used for generating the nodes.
    - total_samples (int): The total number of samples in the dataset.
    - total_parts (int): The total number of files that will be generated.
    - part_number (int): The number of the part to be generated.
    - num_cities_per_example (int): The number of cities in a sample.
    """

    save_all_examples_in_json_format(
        scenario,
        tsp_examples,
        save_dir_path,
        grid_specs,
        num_cities_per_example=num_cities_per_example,
        total_samples=total_samples,
        part_number=part_number,
        total_parts=total_parts,
    )


def save_all_examples_in_json_format(
    scenario: str,
    tsp_examples: list,
    save_dir_path: str,
    grid_specs: dict,
    num_cities_per_example: Union[int, List[int]],
    total_samples: int,
    total_parts: int,
    part_number: int,
) -> None:
    """
    Save all TSP examples in a single JSON file.

    Args:
    - tsp_examples (list of sets of tuples): Each element is a set of tuples with x, y coordinates.
    - save_dir_path (str): The directory path to save the JSON file.
    - grid_specs (dict): Grid specifications used for generating the nodes.
    - num_cities_per_example (int): The number of cities in a sample.
    - total_samples (int): The total number of samples in the dataset.
    - total_parts (int): The total number of files that will be generated.
    - part_number (int): The number of the part to be generated.
    """
    # List to hold all the TSP problem dictionaries
    tsp_problems = []
    json_save_dir = os.path.join(save_dir_path, scenario)
    os.makedirs(json_save_dir, exist_ok=True)
    tsp_examples = set(tsp_examples)
    original_length = len(tsp_examples)

    for _ in range(original_length):
        points = tsp_examples.pop()
        # Sorting the points
        # Generate unique hashcode for the set of coordinates
        sorted_points_list = sorted(list(points), key=lambda x: (x[0], x[1]))
        node_data = "\n".join(
            f"{i + 1} {x} {y}" for i, (x, y) in enumerate(sorted_points_list)
        )
        tsp_hash = generate_hash("EUC_2D" + node_data)

        # Dictionary for the TSP problem
        tsp_dict = {
            "name": tsp_hash,
            "node_coordinates": [[x, y] for x, y in sorted_points_list],
        }
        tsp_problems.append(tsp_dict)

    data = {
        "dataset_name": scenario,
        "total_count": total_samples,
        "total_parts": total_parts,
        "part_number": part_number,
        "samples_in_part": len(tsp_problems),
        "number_of_cities": num_cities_per_example,
        "edge_weight_type": "EUC_2D",
        "grid_specs": grid_specs,
        "source_attribute": {
            "description": "Synthetic TSP problems generated for algorithm testing.",
            "citation": "Provided by ReadyTensor AI Lab",
        },
    }

    f_path = os.path.join(json_save_dir, f"{scenario}_{part_number}.json")

    data["problems"] = tsp_problems
    save_dict_as_json(data, f_path)


def load_examples(file_path: str) -> Dict:
    """
    Load a TSP examples from a file in the JSON format.

    Args:
    - file_path (str): Path of the data file.

    Returns:
        Dict: Dictionary of examples.
        {
        "dataset_name": "tsp_15_1M_u_100x100",
        "total_count": 1000000,
        "total_parts": 32,
        "part_number": 1,
        "number_of_cities": 15,
        "edge_weight_type": "EUC_2D",
        "grid_specs":{"x_start":0,"x_end":99,"y_start":0,"y_end":99,"step_size":1},
        "source_attribute":{"description":"Synthetic TSP problems generated for algorithm testing.","citation":"Provided by ReadyTensor AI Lab"},
        "problems": [...]
        }
    """

    examples = load_dict_from_json(file_path)
    return examples
