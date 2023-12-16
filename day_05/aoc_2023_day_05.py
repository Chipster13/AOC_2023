# Advent of Code 2023
# Day 05
# Jim Kaufman

import argparse
import logging
import sys
import regex as re
from collections import defaultdict
from dataclasses import dataclass

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

@dataclass
class Garden:
    def __init__(self, line_number, data):
        self.line_number = line_number
        self.data = data

    def get_next_line(self):
        if self.line_number < len(self.data):
            line = self.data[self.line_number]
            self.increment_line(1)
            return line
        else:
            return None

    def increment_line(self, count=1):
        self.line_number += count

    def fill_dict(self, dictname: dict) -> dict:
        line = self.get_next_line()
        while not (line == '' or line is None):
            nums = re.findall(r'\d+', line)
            dest_map_start = int(nums[0])
            source_map_start = int(nums[1])
            count = int(nums[2])
            dictname[(source_map_start, source_map_start+count-1)] = dest_map_start
            line = self.get_next_line()

        return dictname


def calculate_next_in_line(testval: int, indict) -> int:
    outval = testval
    k = indict.keys()
    for k1 in k:
        if k1[0] <= testval <= k1[1]:
            diff = testval - k1[0]
            outval = indict[(k1[0], k1[1])] + diff
            break

    return outval

def parse_input(data_path: Path) -> list:
    """
    Reads and formats input.
    Should return the input data in a format where it is ready to be worked on.
    """
    with open(data_path, "r") as raw_input:
        return [l.strip() for l in raw_input.readlines()]


def part_1(input_data: list):
    """Solution code for Part 1. Should return the solution."""
    seed_to_soil_map = defaultdict(int)
    soil_to_fertilizer_map = defaultdict(int)
    fertilizer_to_water_map = defaultdict(int)
    water_to_light_map = defaultdict(int)
    light_to_temp_map = defaultdict(int)
    temp_to_humidity_map = defaultdict(int)
    humidity_to_location_map = defaultdict(int)
    garden = Garden(0, input_data)

    while True:
        line = garden.get_next_line()
        if line is None:
            break
        if line.startswith('seeds:'):
            seeds = re.findall(r'\d+', line)
            seeds = list(map(int, seeds))
            garden.increment_line()
        elif line.startswith('seed-to-soil map:'):
            seed_to_soil_map = garden.fill_dict(seed_to_soil_map)
        elif line.startswith('soil-to-fertilizer map:'):
            soil_to_fertilizer_map = garden.fill_dict(soil_to_fertilizer_map)
        elif line.startswith('fertilizer-to-water map:'):
            fertilizer_to_water_map = garden.fill_dict(fertilizer_to_water_map)
        elif line.startswith('water-to-light map:'):
            water_to_light_map = garden.fill_dict(water_to_light_map)
        elif line.startswith('light-to-temperature map:'):
            light_to_temp_map = garden.fill_dict(light_to_temp_map)
        elif line.startswith('temperature-to-humidity map:'):
            temp_to_humidity_map = garden.fill_dict(temp_to_humidity_map)
        elif line.startswith('humidity-to-location map:'):
            humidity_to_location_map = garden.fill_dict(humidity_to_location_map)
        else:
            garden.increment_line()

    lowest = []
    for seed in seeds:
        soil = calculate_next_in_line(seed, seed_to_soil_map)
        fertilizer = calculate_next_in_line(soil, soil_to_fertilizer_map)
        water = calculate_next_in_line(fertilizer, fertilizer_to_water_map)
        light = calculate_next_in_line(water, water_to_light_map)
        temp = calculate_next_in_line(light, light_to_temp_map)
        humidity = calculate_next_in_line(temp, temp_to_humidity_map)
        location = calculate_next_in_line(humidity, humidity_to_location_map)
        lowest.append(location)

    return min(lowest)


def part_2(input_data: list):
    """Solution code for Part 2. Should return the solution."""
    seed_dict = defaultdict()
    seed_to_soil_map = defaultdict(int)
    soil_to_fertilizer_map = defaultdict(int)
    fertilizer_to_water_map = defaultdict(int)
    water_to_light_map = defaultdict(int)
    light_to_temp_map = defaultdict(int)
    temp_to_humidity_map = defaultdict(int)
    humidity_to_location_map = defaultdict(int)
    garden = Garden(0, input_data)

    while True:
        line = garden.get_next_line()
        if line is None:
            break
        if line.startswith('seeds:'):
            seeds = re.findall(r'\d+', line)
            seeds = list(map(int, seeds))
            for i in range(0, len(seeds), 2):
                seed_dict[seeds[i]] = seeds[i+1]
            garden.increment_line()
        elif line.startswith('seed-to-soil map:'):
            seed_to_soil_map = garden.fill_dict(seed_to_soil_map)
        elif line.startswith('soil-to-fertilizer map:'):
            soil_to_fertilizer_map = garden.fill_dict(soil_to_fertilizer_map)
        elif line.startswith('fertilizer-to-water map:'):
            fertilizer_to_water_map = garden.fill_dict(fertilizer_to_water_map)
        elif line.startswith('water-to-light map:'):
            water_to_light_map = garden.fill_dict(water_to_light_map)
        elif line.startswith('light-to-temperature map:'):
            light_to_temp_map = garden.fill_dict(light_to_temp_map)
        elif line.startswith('temperature-to-humidity map:'):
            temp_to_humidity_map = garden.fill_dict(temp_to_humidity_map)
        elif line.startswith('humidity-to-location map:'):
            humidity_to_location_map = garden.fill_dict(humidity_to_location_map)
        else:
            print(line)
            garden.increment_line()

    lowest = []
    for keys, value in seed_dict.items():
        for seed in range(keys, keys+value):
            soil = calculate_next_in_line(seed, seed_to_soil_map)
            fertilizer = calculate_next_in_line(soil, soil_to_fertilizer_map)
            water = calculate_next_in_line(fertilizer, fertilizer_to_water_map)
            light = calculate_next_in_line(water, water_to_light_map)
            temp = calculate_next_in_line(light, light_to_temp_map)
            humidity = calculate_next_in_line(temp, temp_to_humidity_map)
            location = calculate_next_in_line(humidity, humidity_to_location_map)
            lowest.append(location)

    return min(lowest)


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
