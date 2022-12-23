#!/usr/bin/env python3
import sys
import math

NEIGHBORS = [
    (-1, -1),
    ( 0, -1),
    ( 1, -1),
    (-1,  0),
    ( 1,  0),
    (-1,  1),
    ( 0,  1),
    ( 1,  1)
]

DIRS = [
    [(-1, -1), (0, -1), (1, -1)],
    [(-1, 1), (0, 1), (1, 1)],
    [(-1, -1), (-1, 0), (-1, 1)],
    [(1, -1), (1, 0), (1, 1)]
]

def offset(pos, offset):
    return tuple(sum(v) for v in zip(pos, offset))

def count_neighbors(elves, elf):
    c = 0

    for y in [-1, 0, 1]:
        for x in [-1, 0, 1]:
            if x == y == 0:
                continue
            pos = offset(elf, (x, y))
            if pos in elves:
                c += 1
    return c

def dir_count(elves, elf, dir):
    c = 0
    for subdir in dir:
        pos = offset(elf, subdir)
        if pos in elves:
            c += 1
    return c

def consider(elf, elves, step):
    if count_neighbors(elves, elf) == 0:
        return None

    for i in range(len(DIRS)):
        dir = DIRS[(i + step) % len(DIRS)]
        if dir_count(elves, elf, dir) == 0:
            return offset(elf, dir[1])

    return None

def get_bounds(elves):
    bounds = [[sys.maxsize, -sys.maxsize], [sys.maxsize, -sys.maxsize]]

    for elf in elves:
        for i, v in enumerate(elf):
            bounds[i][0] = min(bounds[i][0], v)
            bounds[i][1] = max(bounds[i][1], v + 1)

    return bounds

def get_area(elves):
    return math.prod([b[1] - b[0] for b in get_bounds(elves)])

def print_elves(elves):
    bounds = get_bounds(elves)

    for y in range(*bounds[1]):
        for x in range(*bounds[0]):
            if (x, y) in elves:
                print('#', end='')
            else:
                print('.', end='')
        print()

def simulate(elves, steps, visualize=False):
    if visualize:
        print_elves(elves)
        input()

    step = 0
    while steps == None or step < steps:
        moves = {}

        # propose move
        for elf in elves:
            move = consider(elf, elves, step)
            if move:
                if move not in moves:
                    moves[move] = []
                moves[move].append(elf)

        if len(moves) == 0:
            return step + 1

        # do moves
        for move in moves:
            if len(moves[move]) == 1:
                del elves[moves[move][0]]
                elves[move] = 1

        if visualize:
            print_elves(elves)
            input()

        step += 1

with open('23.input') as file:
    data = file.read().splitlines()

    elves = {}

    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == '#':
                elves[(x, y)] = 1

    elves2 = elves.copy()

    simulate(elves, 10)
    print(get_area(elves) - len(elves))

    print(simulate(elves2, None))