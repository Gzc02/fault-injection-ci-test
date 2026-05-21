"""Sample module for fault injection testing."""

from pathlib import Path


def process_data(input_path: str, output_path: str) -> dict:
    """Process data from input file and write results."""
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    data = input_file.read_text()
    lines = data.strip().splitlines()

    results = {
        "total_lines": len(lines),
        "non_empty": sum(1 for line in lines if line.strip()),
        "avg_length": sum(len(line) for line in lines) / max(len(lines), 1),
    }

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(str(results))

    return results


def validate_config(config: dict) -> list[str]:
    """Validate configuration dictionary."""
    errors: list[str] = []
    required_keys = ["name", "version", "entry_point"]

    for key in required_keys:
        if key not in config:
            errors.append(f"Missing required key: {key}")

    if "version" in config:
        parts = config["version"].split(".")
        if len(parts) != 3:
            errors.append("Version must be in format X.Y.Z")

    return errors
