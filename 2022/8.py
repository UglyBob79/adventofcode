#!/usr/bin/env python3

import numpy as np

with open("8.input") as file:
    world = [list(map(int, [a for a in line])) for line in file.read().splitlines()]

    map = [[0 for col in range(len(world[0]))] for row in range(len(world))]

    # left/right
    for y in range(len(world)):
        for r in [range(len(world[0])), reversed(range(len(world[0])))]:
            h = -1
            for x in r:
                if world[y][x] > h:
                    map[y][x] = 1
                    h = world[y][x]

    # up/down
    for x in range(len(world[0])):
        for r in [range(len(world)), reversed(range(len(world)))]:
            h = -1
            for y in r:
                if world[y][x] > h:
                    map[y][x] = 1
                    h = world[y][x]

    print(sum([sum(row) for row in map]))

    map = [[0 for col in range(len(world[0]))] for row in range(len(world))]

    for y in range(len(world)):
        for x in range(len(world[0])):
            for dir in [[1, 0], [0, 1], [-1, 0], [0, -1]]:
                p = np.array([x, y]) + dir
                c = 0

                while p[0] in range(len(world[0])) and p[1] in range(len(world)):
                    c += 1

                    if world[p[1]][p[0]] >= world[y][x]:
                        break

                    p += dir

                map[y][x] = map[y][x] * c if map[y][x] else c

    print(max([max(row) for row in map]))