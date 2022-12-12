#!/usr/bin/env python3
import sys

start = None
end = None

dir = ((1, 0), (-1, 0), (0, 1), (0, -1))

def inside(map, pos):
    return pos[0] >= 0 and pos[0] < len(map[0]) and pos[1] >= 0 and pos[1] < len(map)

def traverse(world, map, steps, pos):
    if not map[pos[1]][pos[0]] or steps < map[pos[1]][pos[0]]:
        map[pos[1]][pos[0]] = steps

        for d in dir:
            dest = (pos[0] + d[0], pos[1] + d[1])
            if inside(map, dest):
                if ord(world[pos[1]][pos[0]]) - ord(world[dest[1]][dest[0]]) <= 1:
                    traverse(world, map, steps + 1, dest)

def walk(world, map):
    global start, end

    for y in range(len(world)):
        for x in range(len(world[0])):
            if world[y][x] == 'S':
                start = (x, y)
                world[y][x] = 'a'
            elif world[y][x] == 'E':
                end = (x, y)
                world[y][x] = 'z'

    traverse(world, map, 0, end)

    print(map[start[1]][start[0]])

    res = None

    for y in range(len(world)):
        for x in range(len(world[0])):
            if world[y][x] == 'a':
                if not res or map[y][x] and map[y][x] < res:
                    res = map[y][x]

    print(res)

with open('12.input') as file:
    sys.setrecursionlimit(2000) # :-O

    world = [[*line] for line in file.read().splitlines()]
    map = [[None for col in range(len(world[0]))] for row in range(len(world))]

    walk(world, map)