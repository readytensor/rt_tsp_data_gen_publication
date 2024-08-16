import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR_PATH = os.path.join(ROOT_DIR, "data")

SRC_DIR = os.path.dirname(os.path.abspath(__file__))

TSP_CONFIG_FILE_PATH = os.path.join(SRC_DIR, "config", "tsp_scenarios.json")

GEN_CONFIG_FILE_PATH = os.path.join(SRC_DIR, "config", "dataset_gen_config.json")
