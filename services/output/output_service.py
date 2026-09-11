"""Services for saving reconstructed output."""


import json


def save_output(
    document_id: str,
    data: dict
) -> str:
    """Save reconstructed request body to a JSON file."""

    output_file = f"reconstructed_{document_id}.json"

    with open(output_file, "w") as file:
        json.dump(
            data,
            file,
            indent=2,
            default=str
        )

    return output_file