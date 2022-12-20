#!/usr/bin/env python3

import sys

DIRS = [
    ( 1, 0, 0),
    (-1, 0, 0),
    ( 0, 1, 0),
    ( 0,-1, 0),
    ( 0, 0, 1),
    ( 0, 0,-1)
]

def get_bounds(cubes):
    bounds = [[sys.maxsize, -sys.maxsize], [sys.maxsize, -sys.maxsize], [sys.maxsize, -sys.maxsize]]

    for cube in cubes:
        for i, v in enumerate(cube):
            bounds[i][0] = min(bounds[i][0], v)
            bounds[i][1] = max(bounds[i][1], v)

    return bounds

def traverse(pos, bounds, cubes, visited):
    # check bounds
    for i, v in enumerate(pos):
        if v < bounds[i][0] or v > bounds[i][1]:
            return

    if pos in visited:
        return

    visited.add(pos)

    for dir in DIRS:
        side = tuple(a+b for a,b in zip(pos ,dir))

        if side in cubes:
            cubes[side] += 1
        else:
            traverse(side, bounds, cubes, visited)

with open('18.input') as file:
    cubes = {row: 6 for row in [tuple(int(v) for v in line.split(',')) for line in file.read().splitlines()]}

    for key in cubes:
        for dir in DIRS:
            side = tuple(a+b for a,b in zip(key ,dir))
            if side in cubes:
                cubes[side] -= 1

    print(sum(cubes.values()))

    cubes = {key: 0 for key in cubes}
    bounds = get_bounds(cubes)

    for bound in bounds:
        bound[0] -= 1
        bound[1] += 1

    sys.setrecursionlimit(6000)

    traverse(tuple(bound[0] for bound in bounds), bounds, cubes, set())

    print(sum(cubes.values()))
