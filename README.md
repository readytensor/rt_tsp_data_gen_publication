# Traveling Salesman Problem (TSP) Data Generator

## Overview

This repository provides tools for generating synthetic datasets for the Traveling Salesman Problem (TSP). It is designed to allow flexible configuration of scenarios via JSON files to tailor datasets for specific testing or training needs in research or algorithm development.

## Features

- Configurable Scenarios: Define scenarios for different TSP dataset sizes and complexities.
- Scalable Generation: Control the number of examples and nodes per example.
- Flexible Coordinate Space: Specify the coordinate space for node placement.
- Uniform Sampling: Generate nodes using uniform random sampling within the specified space.
- JSON Output: Generate datasets in a structured JSON format for easy parsing and use.
- Customizable Metadata: Include relevant metadata with each generated dataset.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/readytensor/rt_tsp_data_gen_publication.git
cd rt_tsp_data_gen_publication
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Use

1. Navigate to the `src/config/` directory and modify `tsp_config.json` and `gen_config.json` to set up your desired TSP scenarios and generation parameters.

2. Run the generation script:

```bash
python src/tsp_generator.py
```

3. The generated datasets will be saved in the `data/` directory.

## Configuration Files

### `tsp_scenarios.json`

This file defines various TSP generation scenarios. Each scenario is uniquely named and includes parameters such as:

```json
{
  "version": "1.1.0",
  "generation_scenarios": {
    "tsp_10_50k_u_100x100": {
      "description": "TSP with 10 nodes, 50,000 examples, uniformly sampled in a 100x100 coordinate space.",
      "num_examples": 50000,
      "num_nodes": 10,
      "sampling_method": "uniform",
      "coordinate_space": {
        "x_start": 0,
        "x_end": 100,
        "y_start": 0,
        "y_end": 100
      },
      "seed": 42
    }
  }
}
```

### `dataset_gen_config.json`

This file selects a scenario from `tsp_config.json` and defines the file splitting strategy for large datasets. It also contains the metadata for the dataset which can be customized as needed.

```json
{
  "scenario": "tsp_10_50k_u_100x100",
  "num_samples_per_file": 10000,
  "metadata": {
    "description": "Synthetic TSP problems generated for algorithm testing.",
    "creator": {
      "name": "ReadyTensor Inc.",
      "url": "https://www.readytensor.ai",
      "email": "contact@readytensor.ai"
    },
    "license": "CC BY-SA 4.0"
  }
}
```

## Scenario Naming Convention

We recommend following this format for scenario names:
`tsp_N_P_S_WxH`

Where:

- N is the number of nodes in each TSP instance
- P is the number of problem instances (use 'k' for thousands, e.g., 50k for 50,000)
- S is the sampling method (e.g., 'u' for uniform)
- W and H are the width and height of the coordinate space

Example: "tsp_100_50k_u_100x100" for a scenario with 100 nodes, 50,000 problem instances, uniform sampling, in a 100x100 coordinate space.

## Dataset JSON Structure

The generated dataset is saved in JSON format with the following structure:

```json
{
  "dataset_name": "tsp_10_50k_u_100x100",
  "description": "TSP with 10 nodes, 50,000 examples, uniformly sampled in a 100x100 coordinate space.",
  "total_count": 50000,
  "total_parts": 5,
  "part_number": 1,
  "samples_in_part": 10000,
  "number_of_nodes": 10,
  "coordinate_space": {
    "x_start": 0,
    "x_end": 100,
    "y_start": 0,
    "y_end": 100
  },
  "sampling_method": "uniform",
  "metadata": {
    "description": "Synthetic TSP problems generated for algorithm testing.",
    "creator": {
      "name": "ReadyTensor Inc.",
      "url": "https://www.readytensor.ai",
      "email": "contact@readytensor.ai"
    },
    "license": "CC BY-SA 4.0"
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

## Repository Structure

```bash
/repository_root
├── data/                            # Folder where generated datasets are stored
├── src/                             # folder with all the source code
│   ├── config/                      # Configuration files for defining scenarios
│   │   ├── dataset_gen_config.json  # General configuration for dataset generation
│   │   └── tsp_scenarios.json       # Configuration for specific TSP scenarios
│   ├── generator.py                 # Main script for generating datasets
│   ├── paths.py                     # File paths across the project
│   ├── save_and_load.py             # Utilities for saving and loading datasets
│   └── utils.py                     # Additional helper functions
├── .gitignore                       # gitignore file
├── LICENSE                          # The license file
├── README.md                        # The file you are currently reading
└── requirements.txt                 # All the dependencies to be installed
```

## License

This project is provided under the MIT License. Please see the LICENSE file for more information.

## Contact Information

Repository created by Ready Tensor, Inc. (https://www.readytensor.ai/)
