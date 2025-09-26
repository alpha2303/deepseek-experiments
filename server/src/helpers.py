import json
from pathlib import Path
from typing import Dict


def load_config(file_path: Path) -> Dict[str, Dict[str, str | float | int]]:
    try:
        with open(file_path, "r") as config_file:
            return json.load(config_file)
    except Exception as e:
        raise e
