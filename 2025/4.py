#!/usr/bin/env python3

offsets = [
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1)
]

def neighbours(coords, x, y):
    return sum([(x + a, y + b) in coords for (a, b) in offsets])

def count(coords, remove=False):
    c = 0
    
    while True:
        to_remove = {(x, y) for (x, y) in coords if neighbours(coords, x, y) < 4}
        c += len(to_remove)

        if remove:
            coords -= to_remove

        if not remove or len(to_remove) == 0:
            break

    return c

with open("4.input") as file:
    grid = [list(line.strip()) for line in file.readlines()]
    coords = {(x, y) for y, row in enumerate(grid) for x, char in enumerate(row) if char == '@'}

    print(count(coords))
    print(count(coords, remove=True))


    