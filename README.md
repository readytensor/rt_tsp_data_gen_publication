# Traveling Salesman Problem (TSP) Data Generator

## Overview
This repository provides tools for generating synthetic datasets for the Traveling Salesman Problem (TSP). It is designed to allow flexible configuration of scenarios via JSON files to tailor datasets for specific testing or training needs in research or algorithm development.



## Features
- Configurable Scenarios: Define scenarios for different TSP dataset sizes and complexities.
- Scalable Generation: Control the number of examples and nodes per example.
- Grid Specification: Specify the spatial grid for node placement.


## Repository Structure

```bash
/repository_root
|-- .gitignore              # Specifies intentionally untracked files to ignore
|-- LICENCE                 # The license file
|-- README.md               # The file you are currently reading
|-- requirements.txt        # All the dependencies to be installed
|-- data/                   # Folder where generated datasets are stored
|-- src/                    # Source files that include all the scripts for generation
    |-- config/             # Configuration files for defining scenarios
        |-- gen_config.json # General configuration for dataset generation
        |-- tsp_config.json # Configuration for specific TSP scenarios
    |-- generator.py        # Main script for generating datasets
    |-- paths.py            # Script to handle file paths across the project
    |-- save_and_load.py    # Utilities for saving and loading datasets
    |-- utils.py            # Additional helper functions

```

## Configuration Files

`tsp_config.json`
This file defines various TSP generation scenarios. Each scenario is uniquely named and includes parameters such as:

This configuration example provides details for a TSP scenario named "tsp_10_50k_u_100x100", which specifies:

- Number of Examples: 50,000 problem instances are generated.
- Number of Nodes per Example: Each problem instance consists of 10 nodes.
- Minimum Examples per Node: This parameter controls how often a specific node is used across different problem instances. If null, there is no minimum enforced, allowing for flexible node reuse.
- Grid Specifications: Defines the grid on which nodes are placed:
- x_start and y_start are the starting coordinates of the grid.
  - x_end and y_end define the ending coordinates, setting the grid's dimension.
  - step_size determines the grid's discretization. If null, the grid allows for continuous placement of nodes, meaning nodes can be located at any position within the specified dimensions.
- Seed: Used to seed the random number generator for reproducibility.

Example Scenario
```json
"tsp_10_50k_u_100x100": {
    "num_examples": 50000,
    "num_nodes_per_example": 10,
    "min_examples_per_node": null,
    "grid_specs": {
        "x_start": 0,
        "y_start": 0,
        "x_end": 100,
        "y_end": 100,
        "step_size": null
    },
    "seed": 42
    }
```

`gen_config.json`

This file selects a scenario from tsp_config.json and defines the file splitting strategy for large datasets.

- scenario: Specifies the scenario name as defined in tsp_config.json.
- num_samples_per_file: Number of samples per generated file, controlling how the dataset is split across multiple files.

Configuration Example

```json
{
  "scenario": "tsp_20_50k_u_100x100",
  "num_samples_per_file": 10000
}
```

## Dataset JSON Structure
- dataset_name: The identifier for the type of TSP problem scenario (e.g., "tsp_10_50k_u_100x100").
- total_count: Total number of TSP problems generated for this dataset.
- total_parts: The number of parts into which the dataset is divided.
- part_number: The current part number. This helps in organizing the dataset into multiple manageable files.
- samples_in_part: The number of TSP samples contained in the current part.
- number_of_cities: The number of cities (or nodes) in each TSP problem.
- edge_weight_type: Type of the edge weight (e.g., "EUC_2D" for Euclidean distance in a 2-dimensional space).
- grid_specs: Specifications of the grid where cities are placed, including starting and ending coordinates.
- source_attribute: Attributes about the dataset source including a description and citation if applicable.


## Example Problem in Dataset
Each problem within the dataset is represented as an object within the "problems" array:

- name: A unique identifier for the problem instance.
- node_coordinates: An array of coordinates for each city involved in the problem. Coordinates are listed as [x, y] pairs.

Example JSON Snippet
```json
{
    "dataset_name": "tsp_10_50k_u_100x100",
    "total_count": 50000,
    "total_parts": 5,
    "part_number": 1,
    "samples_in_part": 10000,
    "number_of_cities": 10,
    "edge_weight_type": "EUC_2D",
    "grid_specs": {
        "x_start": 0,
        "y_start": 0,
        "x_end": 100,
        "y_end": 100,
        "step_size": null
    },
    "source_attribute": {
        "description": "Synthetic TSP problems generated for algorithm testing.",
        "citation": "Provided by ReadyTensor AI Lab"
    },
    "problems": [
        {
            "name": "476f819e919e34e5e38d08b7ccd0fa7b",
            "node_coordinates": [
                [17.9432, 24.2407],
                [48.4047, 93.5308],
                [48.746, 89.7431],
                ...
            ]
        },
        ...
    ]
}

```


## How to Use

1. Clone the repository:
```bash
git clone https://github.com/readytensor/rt_tsp_data_gen_publication.git
cd rt_tsp_data_gen_publication
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Modify the configuration files to add/choose a configuration

4. Run the generation script:
```bash
python src/generator.py
```

## License
This project is provided under the MIT License. Please see the [LICENSE](LICENSE) file for more information.

## Contact Information
Repository created by Ready Tensor, Inc. (https://www.readytensor.ai/)