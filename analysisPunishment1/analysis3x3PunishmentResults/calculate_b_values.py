#!/usr/bin/env python3
"""Calculate b values for the 3x3 punishment comparison raw batch data."""

from __future__ import annotations

import csv
import math
from pathlib import Path


MAX_STEPS_PER_TRIAL = 150
CONDITIONS = [
    "regular",
    "punishment_1.0",
    "punishment_0.5",
    "punishment_0.25",
]


def batch_number(path: Path) -> int:
    return int(path.stem.replace("batch", ""))


def read_steps(path: Path) -> list[float]:
    return [float(line.strip()) for line in path.read_text().splitlines() if line.strip()]


def calculate_b_value(steps: list[float], a: int = MAX_STEPS_PER_TRIAL) -> float:
    """Fit y = a * e^(-bt) using Lada's linearized equation."""
    t_values = range(1, len(steps) + 1)
    numerator = sum(t * math.log(y / a) for t, y in zip(t_values, steps) if y > 0)
    denominator = sum(t * t for t in t_values)
    return -(numerator / denominator)


def main() -> None:
    root = Path(__file__).resolve().parent
    raw_data = root / "raw_data"

    b_rows: list[dict[str, str | int]] = []
    summary_rows: list[dict[str, str | int]] = []

    for condition in CONDITIONS:
        values: list[float] = []
        condition_dir = raw_data / condition
        for path in sorted(condition_dir.glob("batch*.txt"), key=batch_number):
            steps = read_steps(path)
            b_value = calculate_b_value(steps)
            values.append(b_value)
            b_rows.append(
                {
                    "condition": condition,
                    "batch": batch_number(path),
                    "trials": len(steps),
                    "b_value": f"{b_value:.8f}",
                }
            )

        summary_rows.append(
            {
                "condition": condition,
                "batches": len(values),
                "avg_b_value": f"{sum(values) / len(values):.8f}",
                "min_b_value": f"{min(values):.8f}",
                "max_b_value": f"{max(values):.8f}",
            }
        )

    with (root / "b_values.csv").open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["condition", "batch", "trials", "b_value"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(b_rows)

    with (root / "b_value_summary.csv").open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["condition", "batches", "avg_b_value", "min_b_value", "max_b_value"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(summary_rows)


if __name__ == "__main__":
    main()
