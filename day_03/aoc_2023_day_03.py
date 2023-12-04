# Advent of Code 2023
# Day 03
# Jim Kaufman

import argparse
import logging
import sys
from collections import defaultdict
import regex as re

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

symbols = set()
stars = defaultdict()

def create_grid(lines: list[str]) -> dict[tuple[int, int]: str]:
    grid = defaultdict(lambda: '.')
    for y, line in enumerate(lines):
        for x, val in enumerate(line):
            grid[(x, y)] = val

    return grid

def scan_grid_for_parts(lines: list) -> dict[tuple[int, int]: str]:
        part_numbers = defaultdict(int)
        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                if not (val.isalpha() or val.isdigit() or val == '.'):
                    symbols.add(val)
                if val == '*':
                    stars[x,y] = []
            matches = re.finditer('\d+', line)
            for match in matches:
                part_numbers[(match.start(), y)] = match[0]
        return part_numbers


def check_for_adjacent_symbol(lines: list[str], partdict: dict[(int, int): str]) -> list:
    grid = create_grid(lines)
    parts = []
    for i, j in partdict.keys():
        found = False
        for l in range(len(partdict[(i,j)])):
            if found:
                break
            for x, y in [(i+l-1, j), (i+l+1, j), (i+l, j-1), (i+l, j+1), (i+l-1, j-1), (i+l-1, j+1), (i+l+1, j-1), (i+l+1, j+1)]:
                if grid[(x,y)] in symbols:
                    parts.append(int(partdict[(i, j)]))
                    found = True
                    break
    return parts

def scan_grid_for_stars(lines: list[str], partdict: dict[(int, int): str]) -> dict:
    grid = create_grid(lines)
    gears = defaultdict(int)
    for i, j in partdict.keys():
        found = False
        for l in range(len(partdict[(i,j)])):
            if found:
                break
            for x, y in [(i+l-1, j), (i+l+1, j), (i+l, j-1), (i+l, j+1), (i+l-1, j-1), (i+l-1, j+1), (i+l+1, j-1), (i+l+1, j+1)]:
                if grid[(x,y)] == '*':
                    val = stars[(x, y)]
                    partno = partdict[(i, j)]
                    val.append(partno)
                    gears[(x, y)] = val
                    found = True
                    break
    return gears

def parse_input(data_path: Path) -> list:
    """
    Reads and formats input.
    Should return the input data in a format where it is ready to be worked on.
    """
    with open(data_path, "r") as raw_input:
        return [l.strip() for l in raw_input.readlines()]


def part_1(input_data: list):
    """Solution code for Part 1. Should return the solution."""
    part_no_dict = scan_grid_for_parts(input_data)
    part_nos = check_for_adjacent_symbol(input_data, part_no_dict)
    return sum(part_nos)


def part_2(input_data: list):
    """Solution code for Part 2. Should return the solution."""
    part_no_dict = scan_grid_for_parts(input_data)
    gear_dict = scan_grid_for_stars(input_data, part_no_dict)
    gear_ratio_total = 0
    for v in gear_dict.values():
        if len(v) == 2:
            gear_ratio_total += int(v[0]) * int(v[1])

    return gear_ratio_total


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
