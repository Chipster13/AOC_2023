# Advent of Code 2023
# Day 02
# Jim Kaufman

import argparse
import logging
import sys
import re
from functools import reduce
import operator

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

valid_cubes = {
    'red' : 12,
    'green': 13,
    'blue': 14
}

def check_cube(games: list) -> int:
    i = 0
    game_number = int(games.pop(0))
    while i < len(games):
        v = games[i]
        if v == ';':
            i += 1
            continue
        k = games[i + 1]
        v = int(v)
        i += 2
        if v > valid_cubes[k]:
            return 0

    return game_number

def get_min_cubes(games: list) -> dict:
    cube = {}
    i = 0
    while i < len(games):
        v = games[i]
        if v == ';':
            i += 1
            continue
        k = games[i + 1]
        v = int(v)
        i += 2
        if k in cube.keys():
            if v > cube[k]:
                cube[k] = v
        else:
            cube[k] = v

    return cube

def parse_input(data_path: Path) -> list:
    """
    Reads and formats input.
    Should return the input data in a format where it is ready to be worked on.
    """
    with open(data_path, "r") as raw_input:
        return [l.strip() for l in raw_input.readlines()]


def part_1(input_data: list):
    """Solution code for Part 1. Should return the solution."""
    invalid_ids = []
    for game in input_data:
        games = re.findall(r'\d+|blue|red|green|(?:;)', game)
        cube = check_cube(games)
        invalid_ids.append(cube)

    return sum(invalid_ids)


def part_2(input_data: list):
    """Solution code for Part 2. Should return the solution."""
    total_power = 0
    for game in input_data:
        games = re.findall(r'\d+|blue|red|green|(?:;)', game)
        game_number = int(games.pop(0))
        cube = get_min_cubes(games)
        vals = list(cube.values())
        power = reduce(operator.mul, vals, 1)
        total_power += power

    return total_power


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
