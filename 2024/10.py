#!/usr/bin/env python3
from collections import defaultdict

dirs = [
  (1, 0),
  (0, 1),
  (-1, 0),
  (0, -1)
]

def in_bounds(map, pos):
    return 0 <= pos[1] < len(map) and 0 <= pos[0] < len(map[0])

def legal(map, pos, curr_height):
    pass

def move(pos, delta):
    return (pos[0] + delta[0], pos[1] + delta[1])

def height(map, pos):
    return map[pos[1]][pos[0]]

trails = defaultdict(set)

def traverse(map, pos, visited):
    if not in_bounds(map, pos):
        return 0

    if height(map, pos) - height(map, visited[-1]) != 1:
        return 0

    visited.append(pos)

    if height(map, pos) == 9:
        trails[visited[0]].add(pos)
        return 1

    return sum(
        traverse(map, m, visited.copy())
        for d in dirs
        for m in [move(pos, d)]
        if m not in visited
    )

def trail(map, pos):
    return sum(traverse(map, move(pos, d), [pos]) for d in dirs)

with open("10.input") as file:
    map = [[int(x) for x in line.strip()] for line in file]

    total = 0

    for y in range(len(map)):
        for x in range(len(map[0])):
            if height(map, (x, y)) == 0:
              total += trail(map, (x, y))

    print(sum(len(values) for values in trails.values()))
    print(total)