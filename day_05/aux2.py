puzzle = open("aoc_2023_day_05_input.txt").read()

from functools import reduce
from collections import defaultdict, deque
import re


class GiveSeedFertilizer:
    def __init__(self, input):
        input = input.split("\n\n")
        seeds, *maps = input
        seeds = seeds.split(":").pop()
        self.seeds = [int(x) for x in seeds.split()]
        self.metamap = dict()
        self.maps = reduce(self.processMaps, maps, defaultdict(dict))

    def processMaps(self, maps, map):
        map = map.splitlines()
        regex = r"(\w+)-to-(\w+)"
        mapType, *ranges = map
        sourceType, destType = re.findall(regex, mapType).pop()
        for r in ranges:
            dest, source, size = [int(x) for x in r.split()]
            range = (source, source + size)
            maps[sourceType][range] = dest - source
            self.metamap[sourceType] = destType
        return maps

    def isBetween(self, range, number):
        start, stop = range
        return start <= number < stop

    def partOne(self):
        answer = []
        for seed in self.seeds:
            current = "seed"
            number = seed
            while current != "location":
                entry.append((current, number))
                for range in self.maps[current]:
                    if self.isBetween(range, number):
                        number += self.maps[current][range]
                        break
                current = self.metamap[current]
            answer.append((number, seed))
        print(min(answer))

    def partTwo(self):
        seeds = zip(self.seeds[0::2], self.seeds[1::2])
        seeds = [[start, start + size] for start, size in seeds]
        seeds = deque((x, "seed") for x in seeds)
        answer = []
        while seeds:
            number, current = seeds.popleft()
            if current == "location":
                answer.append(number[0])
                continue

            for range in self.maps[current]:
                lower = self.isBetween(range, number[0])
                upper = self.isBetween(range, number[1] - 1)
                if not lower and not upper: continue
                if lower and upper:
                    number = [x + self.maps[current][range] for x in number]
                    seeds.append((number, self.metamap[current]))
                    break
                if lower: split = range[1]
                if upper: split = range[0]
                seeds.append(((number[0], split), current))
                seeds.append(((split, number[1]), current))
                break
            else:
                seeds.append((number, self.metamap[current]))

        print(min(answer))
