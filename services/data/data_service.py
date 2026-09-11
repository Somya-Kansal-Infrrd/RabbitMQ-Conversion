"""Services for loading JSON data."""

import json


def load_json_file(file_name: str) -> list[dict]:
    """Load and return data from a JSON file."""

    with open(file_name, "r") as file:
        return json.load(file)