# Advent of Code 2023
# Day 15
# Jim Kaufman

import argparse
import logging
import sys

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

def hash(string):
    tot = 0
    for ch in string:
        tot += ord(ch)
        tot *= 17
        tot %= 256
    return tot

def parse_input(data_path: Path) -> list:
    """
    Reads and formats input.
    Should return the input data in a format where it is ready to be worked on.
    """
    with open(data_path, "r") as raw_input:
        return [l.strip() for l in raw_input.readlines()]


def part_1(input_data: list):
    """Solution code for Part 1. Should return the solution."""
    input_data = ''.join(input_data)
    return sum(map(hash, input_data.split(',')))


def part_2(input_data: list):
    """Solution code for Part 2. Should return the solution."""
    input_data = ''.join(input_data)

    boxes = [[] for _ in range(256)]
    lenses = {}
    instruction = input_data.split(',')
    for cmd in instruction:
        if '=' in cmd:
            cleartextbox = cmd.split('=')[0]
            lens = cmd.split('=')[1]
            lens = int(lens)
            index = hash(cleartextbox)
            if not cleartextbox in boxes[index]:
                boxes[index].append(cleartextbox)
            lenses[cleartextbox] = lens
        else:
            cleartextbox = cmd.split('-')[0]
            lens = cmd.split('-')[1]
            if lens.isdigit():
                lens = int(lens)
            index = hash(cleartextbox)
            if cleartextbox in boxes[index]:
                boxes[index].remove(cleartextbox)
                lenses[cleartextbox] = ''

    focus_power = 0
    for i, box in enumerate(boxes, 1):
        for j, contents in enumerate(box, 1):
            focus_power += i * j * lenses[contents]

    return focus_power


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
