#!/usr/bin/env python3
from collections import defaultdict

def inBounds(pos):
    return 0 <= pos[0] < bounds[0] and 0 <= pos[1] < bounds[1]

def diff(pair):
    return (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1])

def add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])

bounds = (None, None)

with open("8.input") as file:
    raw_data = [line.strip() for line in file]
    bounds = (len(raw_data[0]), len(raw_data))

    data = defaultdict(list)
    for y, line in enumerate(raw_data):
      for x, char in enumerate(line):
         if char != '.':
            data[char].append((x, y))

    antinodes = {
        elem
        for positions in data.values()
        for pair in ((positions[i], positions[j]) for i in range(len(positions)) for j in range(i + 1, len(positions)))
        for d in [diff(pair)]
        for elem in ([op(pos, d) for op in [sub, add] for pos in pair])
        if inBounds(elem) and elem not in pair
    }

    print(len(antinodes))

    antinodes = set()

    for positions in data.values():
      for pos1, d in ((positions[i], diff([positions[i], positions[j]])) for i in range(len(positions)) for j in range(i + 1, len(positions))):
        p = pos1
        while inBounds(p):
            antinodes.add(p)
            p = add(p, d)

        p = pos1
        while inBounds(p):
            antinodes.add(p)
            p = sub(p, d)

    print(len(antinodes))