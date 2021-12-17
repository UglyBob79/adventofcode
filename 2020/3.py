#!/usr/bin/env python3
import math

with open("3.input") as file:
    data = [row.strip() for row in file.readlines()]

    x = 0
    y = 0
    t = 0

    for y in range(1, len(data)):
        x = (x + 3) % len(data[0])
        if data[y][x] == '#':
            t += 1

    print(t)

    step = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    trees = []
    for s in step:
        t = 0
        x = 0
        y = 0
        while y < len(data):
            if data[y][x] == '#':
                t += 1
            x = (x + s[0]) % len(data[0])
            y += s[1]
        trees.append(t)

    print(trees[1])
    print(math.prod(trees))
