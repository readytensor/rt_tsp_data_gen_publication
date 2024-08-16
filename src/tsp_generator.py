import random
import math
from tqdm import tqdm
from typing import List, Tuple, FrozenSet
from dataclasses import dataclass

import paths
from utils import set_seed, load_config
from save_and_load import save_generated_examples


@dataclass
class CoordinateSpace:
    x_start: float
    x_end: float
    y_start: float
    y_end: float


def generate_tsp_examples(
    space: CoordinateSpace, num_nodes: int, num_examples: int, rounding: int = 4
) -> List[FrozenSet[Tuple[float, float]]]:
    """
    Generate TSP examples within the specified coordinate space.

    Args:
        space (CoordinateSpace): The coordinate space for node generation.
        num_nodes (int): Number of nodes per example.
        num_examples (int): Number of examples to generate.
        rounding (int): Number of decimal places to round coordinates.

    Returns:
        List[FrozenSet[Tuple[float, float]]]: List of unique TSP examples.
    """
    all_examples = set()
    while len(all_examples) < num_examples:
        example = set()
        while len(example) < num_nodes:
            x = round(random.uniform(space.x_start, space.x_end), rounding)
            y = round(random.uniform(space.y_start, space.y_end), rounding)
            example.add((x, y))

        frozen_example = frozenset(example)
        if frozen_example not in all_examples:
            all_examples.add(frozen_example)

    return list(all_examples)


def main():
    tsp_config = load_config(paths.TSP_CONFIG_FILE_PATH)
    gen_config = load_config(paths.GEN_CONFIG_FILE_PATH)

    scenario_to_run = gen_config["scenario"]
    scenario_specs = tsp_config["generation_scenarios"][scenario_to_run]

    num_nodes = scenario_specs["num_nodes"]
    num_examples = scenario_specs["num_examples"]
    space = CoordinateSpace(**scenario_specs["coordinate_space"])
    rounding = scenario_specs.get("rounding", 4)

    set_seed(scenario_specs["seed"])

    num_samples_per_file = gen_config["num_samples_per_file"]
    num_files = math.ceil(num_examples / num_samples_per_file)

    for i in tqdm(range(num_files), desc="Generating files", total=num_files):
        examples_in_file = min(
            num_samples_per_file, num_examples - i * num_samples_per_file
        )

        tsp_examples = generate_tsp_examples(
            space, num_nodes, examples_in_file, rounding
        )

        save_generated_examples(
            scenario=scenario_to_run,
            description=scenario_specs["description"],
            tsp_examples=tsp_examples,
            save_dir_path=paths.DATA_DIR_PATH,
            coordinate_space_specs=scenario_specs["coordinate_space"],
            num_nodes=num_nodes,
            total_samples=num_examples,
            total_parts=num_files,
            part_number=i + 1,
            sampling_method=scenario_specs["sampling_method"],
            metadata=gen_config["metadata"],
            version=gen_config["version"],
        )


if __name__ == "__main__":
    main()
