import random
import math
import paths
import numpy as np
from tqdm import tqdm
from math import comb
from typing import List, Tuple, Set
from utils import set_seed, load_config
from save_and_load import save_generated_examples


def generate_grid_nodes(grid_specs: dict) -> List[Tuple[int, int]]:
    """
    Generate a grid of size [(x_end-x_start)/step_size, (y_end-y_start)/step_size].
    Each node is a tuple of x and y coordinates on the grid.
    Grid nodes are returned as a list of tuples.

    Args:
    - grid_specs (dict): Dictionary which contains the following keys:
        - x_start (int): The starting x value
        - x_end (int): The ending x value
        - y_start (int): The starting y value
        - y_end (int): The ending y value
        - step_size (float): The step size of the grid (i.e. the distance between two points
                             in one of the dimensions)

    Returns:
    - grid_nodes (List[Tuple[int, int]]): A list of tuples of x values and y values.
                                         e.g. [(1, 2), (3, 4), (5, 6)]
    """
    step_size = grid_specs["step_size"]
    x_start, x_end = grid_specs["x_start"], grid_specs["x_end"]
    y_start, y_end = grid_specs["y_start"], grid_specs["y_end"]
    if isinstance(step_size, int):
        step_size = float(step_size)
    rounding = len(str(step_size).split(".")[1])
    x_range = np.arange(x_start, x_end, step_size).round(rounding)
    y_range = np.arange(y_start, y_end, step_size).round(rounding).tolist()
    grid_nodes = list((x, y) for x in x_range for y in y_range)
    return grid_nodes


def get_max_feasible_examples(
    grid_nodes: Set[Tuple[int, int]], num_nodes_per_example: int
) -> int:
    """
    Get the maximum number of feasible examples that can be generated from the grid nodes.

    Args:
    - grid_nodes (Set[Tuple[int, int]]): The grid is a set of tuples of x values and y values.
                                         e.g. {(1, 2), (3, 4), (5, 6)}
    - num_nodes_per_example (int): The number of nodes in each example

    Returns:
    - max_feasible_examples (int): The maximum number of feasible examples that can be generated
    """
    max_feasible_examples = comb(len(grid_nodes), num_nodes_per_example)
    return max_feasible_examples


def create_tsp_examples_per_node(
    current_examples, grid_nodes, num_nodes, min_examples_per_node
):
    """
    Generate unique TSP examples such that there are min_examples_per_node examples for each node in the grid.

    Note:
    Since a node can be part of some other node's generated examples, the number of unique examples generated
    per node will be greater than min_examples_per_node for some nodes.
    """
    if isinstance(num_nodes, list):
        num_nodes = min(num_nodes)

    if num_nodes > len(grid_nodes):
        raise ValueError(
            "num_nodes cannot be greater than the number of points in the grid"
        )

    for base_point in grid_nodes:
        examples_for_this_point = 0
        attempts = 0
        rest_of_grid = list(filter(lambda item: item != base_point, grid_nodes))
        while examples_for_this_point < min_examples_per_node:
            if attempts > 10000:
                raise RuntimeError(
                    "Too many attempts to find unique TSP examples. Consider adjusting parameters."
                )
            # Select random points to form a TSP example, including the base point
            potential_example = frozenset(
                set(random.sample(rest_of_grid, num_nodes - 1)) | {base_point}
            )
            # Ensure this example hasn't been created before
            if potential_example not in current_examples:
                current_examples.add(potential_example)
                examples_for_this_point += 1
            attempts += 1
    return current_examples


def create_random_tsp_examples(
    current_examples,
    grid_nodes,
    num_nodes_per_example,
    num_examples,
    exclude_lengths=[],
):
    """
    Create randomly generated tsp examples until we have num_examples unique examples.
    Generated examples are unique and we check for duplicates before adding them to the
    currently generated set of examples.
    """
    if len(current_examples) >= num_examples:
        return current_examples
    # Continue sampling until we have collected enough unique examples
    while len(current_examples) < num_examples:
        current_nodes_per_sample = num_nodes_per_example
        if isinstance(num_nodes_per_example, list):
            current_nodes_per_sample = random.randint(
                num_nodes_per_example[0], num_nodes_per_example[1]
            )
            if current_nodes_per_sample in exclude_lengths:
                continue

        new_example = frozenset(random.sample(grid_nodes, current_nodes_per_sample))
        current_examples.add(new_example)
    return current_examples


def generate_discrete_samples(scenario_specs, num_examples):

    num_nodes_per_example = scenario_specs["num_nodes_per_example"]
    grid_specs = scenario_specs["grid_specs"]
    min_examples_per_node = scenario_specs["min_examples_per_node"]
    exclude_lengths = scenario_specs.get("exclude_lengths", [])

    # generate list of grid nodes
    grid_nodes = generate_grid_nodes(grid_specs)

    # Check feasibility of generating num_examples samples for given grid nodes

    max_nodes_per_example = (
        num_nodes_per_example
        if isinstance(num_nodes_per_example, int)
        else max(num_nodes_per_example)
    )
    max_unique_examples = comb(len(grid_nodes), max_nodes_per_example)
    if num_examples > max_unique_examples:
        raise ValueError("It is not possible to generate that many unique TSP examples")

    # generate unique examples such that there are min_examples_per_node * len(grid_nodes) examples
    # we create `min_examples_per_node` examples for each node in the grid

    tsp_examples = set()
    if min_examples_per_node is not None:
        tsp_examples = create_tsp_examples_per_node(
            current_examples=tsp_examples,
            grid_nodes=grid_nodes,
            num_nodes=num_nodes_per_example,
            min_examples_per_node=min_examples_per_node,
        )

    # create remaining examples randomly to hit num_examples (if we havent already)

    tsp_examples = create_random_tsp_examples(
        current_examples=tsp_examples,
        grid_nodes=grid_nodes,
        num_nodes_per_example=num_nodes_per_example,
        num_examples=num_examples,
        exclude_lengths=exclude_lengths,
    )

    return tsp_examples


def generate_continuous_tsp_examples(
    scenario_specs: dict,
    num_examples: int,
    rounding: int = 4,
):
    x_start = scenario_specs["grid_specs"]["x_start"]
    x_end = scenario_specs["grid_specs"]["x_end"]
    y_start = scenario_specs["grid_specs"]["y_start"]
    y_end = scenario_specs["grid_specs"]["y_end"]
    num_nodes_per_example = scenario_specs["num_nodes_per_example"]

    all_examples = set()
    for _ in range(num_examples):
        example = set()
        num_nodes = num_nodes_per_example
        if isinstance(num_nodes_per_example, list):
            num_nodes = random.randint(
                num_nodes_per_example[0], num_nodes_per_example[1]
            )
        while len(example) < num_nodes:
            x = round(random.uniform(x_start, x_end), rounding)
            y = round(random.uniform(y_start, y_end), rounding)
            if (x, y) in example:
                continue
            example.add((x, y))
            if len(example) == num_nodes and frozenset(example) in all_examples:
                example = set()

        all_examples.add(frozenset(example))
    return frozenset(all_examples)


if __name__ == "__main__":
    tsp_config = load_config(paths.TSP_CONFIG_FILE_PATH)
    gen_config = load_config(paths.GEN_CONFIG_FILE_PATH)
    num_samples_per_file = gen_config["num_samples_per_file"]

    scenario_to_run = gen_config["scenario"]
    given_scenario_specs = tsp_config["generation_scenarios"][scenario_to_run]
    num_cities = given_scenario_specs["num_nodes_per_example"]
    num_examples = given_scenario_specs["num_examples"]
    num_files = math.ceil(num_examples / num_samples_per_file)
    set_seed(given_scenario_specs["seed"])

    for i in tqdm(range(num_files), desc="generating files", total=num_files):
        examples_in_file = min(
            num_samples_per_file, num_examples - i * num_samples_per_file
        )

        if given_scenario_specs["grid_specs"]["step_size"] is None:
            rounding = given_scenario_specs["grid_specs"].get("rounding", 4)

            tsp_examples = generate_continuous_tsp_examples(
                given_scenario_specs, num_examples=examples_in_file, rounding=rounding
            )

        else:
            tsp_examples = generate_discrete_samples(
                scenario_specs=given_scenario_specs,
                num_examples=examples_in_file,
            )

        save_generated_examples(
            scenario=scenario_to_run,
            tsp_examples=list(tsp_examples),
            save_dir_path=paths.DATA_DIR_PATH,
            grid_specs=given_scenario_specs["grid_specs"],
            num_cities_per_example=num_cities,
            total_samples=num_examples,
            total_parts=num_files,
            part_number=i + 1,
        )
