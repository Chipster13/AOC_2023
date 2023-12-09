# Advent of Code 2023
# Day 07
# Jim Kaufman

import argparse
import logging
import sys
from collections import Counter
from collections import defaultdict

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
conversion_p1 = {
    'A': 'M',
    'K': 'L',
    'Q': 'K',
    'J': 'J',
    'T': 'I',
    '9': 'H',
    '8': 'G',
    '7': 'F',
    '6': 'E',
    '5': 'D',
    '4': 'C',
    '3': 'B',
    '2': 'A'
}

conversion_p2 = {
    'A': 'M',
    'K': 'L',
    'Q': 'K',
    'T': 'I',
    '9': 'H',
    '8': 'G',
    '7': 'F',
    '6': 'E',
    '5': 'D',
    '4': 'C',
    '3': 'B',
    '2': 'A',
    'J': '1'
}

def parse_input(data_path: Path) -> list:
    """
    Reads and formats input.
    Should return the input data in a format where it is ready to be worked on.
    """
    with open(data_path, "r") as raw_input:
        return [l.strip() for l in raw_input.readlines()]


def part_1(input_data: list):
    """Solution code for Part 1. Should return the solution."""
    five_bucket = []
    four_bucket = []
    full_bucket = []
    three_bucket = []
    two_pair_bucket = []
    two_bucket = []
    one_bucket = []

    for val in input_data:
        c1 = ''.join(conversion_p1[i] for i in val[:5])
        cnt = Counter(c1)
        if Counter(cnt.values())[5] == 1:
           five_bucket.append((cnt, int(val[5:])))
        elif Counter(cnt.values())[4] == 1:
            four_bucket.append((c1, int(val[5:])))
        elif Counter(cnt.values())[3] == 1 and Counter(cnt.values())[2] == 1:
            full_bucket.append((c1, int(val[5:])))
        elif Counter(cnt.values())[3] == 1:
            three_bucket.append((c1, int(val[5:])))
        elif Counter(cnt.values())[2] == 2:
            two_pair_bucket.append((c1, int(val[5:])))
        elif Counter(cnt.values())[2] == 1:
            two_bucket.append((c1, int(val[5:])))
        else:
            one_bucket.append((c1, int(val[5:])))

    five_bucket = sorted(five_bucket, key = lambda x: x[0])
    four_bucket = sorted(four_bucket, key = lambda x: x[0])
    full_bucket = sorted(full_bucket, key = lambda x: x[0])
    three_bucket = sorted(three_bucket, key = lambda x: x[0])
    two_pair_bucket = sorted(two_pair_bucket, key = lambda x: x[0])
    two_bucket = sorted(two_bucket, key = lambda x: x[0])
    one_bucket = sorted(one_bucket, key = lambda x: x[0])

    total = 0
    i = 1
    while i <= len(input_data):
        for a, b in one_bucket:
            total += b*i
            i += 1
        for a,b in two_bucket:
            total += b*i
            i += 1
        for a,b in two_pair_bucket:
            total += b*i
            i += 1
        for a, b  in three_bucket:
            total += b*i
            i += 1
        for a,b in full_bucket:
            total += b*i
            i += 1
        for a,b in four_bucket:
            total += b*i
            i += 1
        for a,b in five_bucket:
            total += b*i
            i += 1

    return total


def part_2(input_data: list):
    """Solution code for Part 2. Should return the solution."""
    five_bucket = []
    four_bucket = []
    full_bucket = []
    three_bucket = []
    two_pair_bucket = []
    two_bucket = []
    one_bucket = []

    for val in input_data:
        cnt2 = defaultdict(lambda: 0)
        c1 = ''.join(conversion_p2[i] for i in val[:5])
        cnt1 = Counter(c1)
        for k, v in cnt1.items():
            if k == '1':
                cnt2[k] = v

        cnt1.pop('1', None)

        if (Counter(cnt1.values())[5] == 1) or \
                ((Counter(cnt1.values())[4] == 1 and cnt2.get('1', 0) == 1) or \
                (Counter(cnt1.values())[3] == 1 and cnt2.get('1', 0) == 2) or \
                (Counter(cnt1.values())[2] == 1 and cnt2.get('1',0) == 3) or \
                (Counter(cnt1.values())[1] == 1 and cnt2.get('1', 0) == 4) or \
                 cnt2.get('1', 0) == 5):
            five_bucket.append((c1, int(val[5:])))
        elif (Counter(cnt1.values())[4] == 1) or \
                ((Counter(cnt1.values())[3] == 1 and cnt2.get('1',0) == 1) or \
                (Counter(cnt1.values())[2] == 1 and cnt2.get('1', 0) == 2) or \
                (Counter(cnt1.values())[1] == 2 and cnt2.get('1', 0) == 3)):
            four_bucket.append((c1, int(val[5:])))
        elif (Counter(cnt1.values())[3] == 1 and Counter(cnt1.values())[2] == 1) or \
                (Counter(cnt1.values())[2] == 2 and cnt2.get('1', 0) == 1):
            full_bucket.append((c1, int(val[5:])))
        elif (Counter(cnt1.values())[3] == 1) or \
                (Counter(cnt1.values())[2] == 1 and cnt2.get('1', 0) == 1) or \
                (Counter(cnt1.values())[1] == 3 and cnt2.get('1', 0) == 2):
            three_bucket.append((c1, int(val[5:])))
        elif Counter(cnt1.values())[2] == 2 or \
                (Counter(cnt1.values())[2] == 1 and cnt2.get('1', 0) == 1):
            two_pair_bucket.append((c1, int(val[5:])))
        elif (Counter(cnt1.values())[2] == 1) or cnt2.get('1', 0) == 1:
            two_bucket.append((c1, int(val[5:])))
        else:
            one_bucket.append((c1, int(val[5:])))

    five_bucket = sorted(five_bucket, key = lambda x: x[0])
    four_bucket = sorted(four_bucket, key = lambda x: x[0])
    full_bucket = sorted(full_bucket, key = lambda x: x[0])
    three_bucket = sorted(three_bucket, key = lambda x: x[0])
    two_pair_bucket = sorted(two_pair_bucket, key = lambda x: x[0])
    two_bucket = sorted(two_bucket, key = lambda x: x[0])
    one_bucket = sorted(one_bucket, key = lambda x: x[0])

    total = 0
    i = 1
    while i < len(input_data):
        for a, b in one_bucket:
            total += b*i
            i += 1
        for a,b in two_bucket:
            total += b*i
            i += 1
        for a,b in two_pair_bucket:
            total += b*i
            i += 1
        for a, b  in three_bucket:
            total += b*i
            i += 1
        for a,b in full_bucket:
            total += b*i
            i += 1
        for a,b in four_bucket:
            total += b*i
            i += 1
        for a,b in five_bucket:
            total += b*i
            i += 1

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
