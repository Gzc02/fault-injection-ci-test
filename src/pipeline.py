"""Sample module for fault injection testing."""

import os
from pathlib import Path


def process_data(input_path: str, output_path: str) -> dict:
    """Process data from input file and write results."""
    input_file = Path(input_path)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    data = input_file.read_text()
    lines = data.strip().split("
")

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
    errors = []
    required_keys = ["name", "version", "entry_point"]

    for key in required_keys:
        if key not in config:
            errors.append(f"Missing required key: {key}")

    if "version" in config:
        parts = config["version"].split(".")
        if len(parts) != 3:
            errors.append("Version must be in format X.Y.Z")

    return errors


class DataPipeline:
    """A simple data processing pipeline."""

    def __init__(self, name: str, steps: list[str] | None = None):
        self.name = name
        self.steps = steps or []
        self.results = {}

    def add_step(self, step_name: str) -> None:
        """Add a processing step."""
        if step_name in self.steps:
            raise ValueError(f"Step already exists: {step_name}")
        self.steps.append(step_name)

    def run(self, data: dict) -> dict:
        """Execute all pipeline steps."""
        current = data.copy()
        for step in self.steps:
            current["last_step"] = step
            current["step_count"] = current.get("step_count", 0) + 1
        self.results = current
        return current
