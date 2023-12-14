# Advent of Code 2023
# Day 11
# Jim Kaufman

import argparse
import logging
import sys
from itertools import combinations

from pathlib import Path

PARENT_FOLDER = Path(__file__).parent
BASE_FILE_NAME = Path(__file__).stem
INPUT_FILE_NAME = f"{BASE_FILE_NAME}_input.txt"
SAMPLE_FILE_NAME = f"{BASE_FILE_NAME}_sample.txt"

INPUT_PATH = PARENT_FOLDER / INPUT_FILE_NAME
SAMPLE_PATH = PARENT_FOLDER / SAMPLE_FILE_NAME


logger = logging.getLogger("aoc_logger")
log_handler = logging.StreamHandler()
log_handler.setLevel("DEBUG")
logger.addHandler(log_handler)


# ---=== PROBLEM CODE BELOW ===---


man_dist = lambda point1, point2: abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

def insert_string_in_column(matrix, column_indices, string_to_insert):
    j = 0
    while j < len(column_indices):
        current_index = column_indices[j]
        for i in range(len(matrix)):
            matrix[i] = matrix[i][:current_index+j] + string_to_insert + matrix[i][current_index +j + len(string_to_insert)-1:]
        j += 1
def insert_rows(matrix, insert_indices, row_value):
    i = 0
    while i < len(insert_indices):
        current_index = insert_indices[i]
        matrix.insert(current_index + i, row_value)
        i += 1

def parse_input(data_path: Path) -> list:
    """
    Reads and formats input.
    Should return the input data in a format where it is ready to be worked on.
    """
    with open(data_path, "r") as raw_input:
        return [l.strip() for l in raw_input.readlines()]


def part_1(input_data: list):
    """Solution code for Part 1. Should return the solution."""
    empty_rows = [r for r, row in enumerate(input_data) if all(ch == '.' for ch in row)]
    empty_cols = [c for c, col in enumerate(zip(*input_data)) if all(ch == '.' for ch in col)]

    insert_rows(input_data, empty_rows, '.' * len(input_data[0]))
    insert_string_in_column(input_data, empty_cols, '.')

    galaxies = [(r, c) for r, row in enumerate(input_data) for c, col in enumerate(row) if input_data[r][c] == '#']
    combs = list(combinations(galaxies, 2))

    total = 0
    for combo in combs:
        r1, c1 = combo[0]
        r2, c2 = combo[1]
        dist = man_dist((r1, c1), (r2, c2))
        total += dist

    return total

def part_2(input_data: list):
    """Solution code for Part 2. Should return the solution."""
    empty_rows = [r for r, row in enumerate(input_data) if all(ch == '.' for ch in row)]
    empty_cols = [c for c, col in enumerate(zip(*input_data)) if all(ch == '.' for ch in col)]
    galaxies = [(r, c) for r, row in enumerate(input_data) for c, col in enumerate(row) if input_data[r][c] == '#']
    combs = list(combinations(galaxies, 2))

    total = 0
    scale = 1_000_000
    for combo in combs:
        r1, c1 = combo[0]
        r2, c2 = combo[1]
        for r in range(r1, r2):
            total += scale if r in empty_rows else 1
        for c in range(min(c1, c2), max(c1, c2)):
            total += scale if c in empty_cols else 1

    return total

def run_direct():
    """
    This function runs if this file is executed directly, rather than using the
    justfile interface. Useful for quick debugging and checking your work.
    """
    print(parse_input(SAMPLE_PATH))


# ---=== PROBLEM CODE ABOVE ===---


def problem_dispatch(mode: str, part: int, log_level: str = None):
    if log_level is not None:
        logger.setLevel(log_level.upper())
    parts = {1: part_1, 2: part_2}
    inputs = {"check": parse_input(SAMPLE_PATH), "solve": parse_input(INPUT_PATH)}
    return parts[part](inputs[mode])


def run_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, choices={"check", "solve"})
    parser.add_argument("part", type=int, choices={1, 2})
    parser.add_argument(
        "--log-level",
        type=str,
        required=False,
        choices={"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"},
    )
    args = parser.parse_args()
    print(problem_dispatch(args.mode, args.part, args.log_level))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise SystemExit(run_direct())
    else:
        raise SystemExit(run_cli())
