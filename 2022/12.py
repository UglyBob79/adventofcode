#!/usr/bin/env python3

def walk(world, map):
    for y in range(len(world)):
        for x in range(len(world[0])):
            if world[y][x] == 'S':
                start = (x, y)
                world[y][x] = 'a'
            elif world[y][x] == 'E':
                end = (x, y)
                world[y][x] = 'z'

    q = [(0, end)]

    while q:
        steps, pos = q.pop(0)

        if not map[pos[1]][pos[0]] or steps < map[pos[1]][pos[0]]:
            map[pos[1]][pos[0]] = steps

            for dir in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                dest = (pos[0] + dir[0], pos[1] + dir[1])
                if dest[0] >= 0 and dest[0] < len(map[0]) and dest[1] >= 0 and dest[1] < len(map):
                    if ord(world[pos[1]][pos[0]]) - ord(world[dest[1]][dest[0]]) <= 1:
                        q.append((steps + 1, dest))

    print(map[start[1]][start[0]])
    print(min([map[y][x] for y in range(len(world)) for x in range(len(world[y])) if world[y][x] == 'a' and map[y][x]]))

with open('12.input') as file:
    world = [[*line] for line in file.read().splitlines()]
    map = [[None for _ in range(len(world[0]))] for _ in range(len(world))]

    walk(world, map)