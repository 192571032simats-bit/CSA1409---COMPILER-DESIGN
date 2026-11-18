import csv
import time
from pathlib import Path

from opt import optimize


def measure(level, count=10000):
    instructions = [f"T{i} = {i} + 1" for i in range(count)]
    start = time.perf_counter()
    for _ in range(3):
        optimize(instructions, level)
    return (time.perf_counter() - start) / 3


def main():
    output = Path(__file__).parent.parent / "Measurements"
    output.mkdir(parents=True, exist_ok=True)
    with (output / "optimization_levels.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["level", "instruction_count", "average_seconds"])
        for level in (0, 1, 2):
            elapsed = measure(level)
            writer.writerow([level, 10000, f"{elapsed:.6f}"])


if __name__ == "__main__":
    main()
