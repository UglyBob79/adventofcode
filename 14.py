#!/usr/bin/env python3
from collections import Counter
from functools import lru_cache

@lru_cache(maxsize=None)
def count(polymer, depth):
    if depth == 0:
        return Counter(polymer)
    else:
        new = rules[polymer]
        return count(polymer[0] + new, depth - 1) + count(new + polymer[1], depth - 1) - Counter(new)

def solve(polymer, depth):
    c = sum((count(polymer[i : i + 2], depth) for i in range(len(polymer) - 1)), Counter()) - Counter(polymer[1:-1])
    sorted = c.most_common()
    print(sorted[0][1] - sorted[-1][1])


with open("14.input") as file:
    data = file.readline().strip()
    file.readline()
    rules = dict([line.strip().split(' -> ') for line in file.readlines()])

    solve(data, 10)
    solve(data, 40)
