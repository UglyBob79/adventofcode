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
        curr = c
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if (x, y) in coords and neighbours(coords, x, y) < 4:
                    c += 1
                    if remove:
                        coords.remove((x, y))
        if not remove or c == curr:
            break
    
    return c

with open("4.input") as file:
    grid = [list(line.strip()) for line in file.readlines()]
    coords = {(x, y)
                for y, row in enumerate(grid)
                for x, char in enumerate(row)
                if char == '@'}

    print(count(coords))
    print(count(coords, remove=True))


    