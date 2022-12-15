#!/usr/bin/env python3
import re

def overlap(r1, r2):
    return r1[0] <= r2[0] <= r1[0] or r1[0] <= r2[1] <= r1[1] or r2[0] <= r1[0] <= r2[1] or r2[0] <= r1[1] <= r2[1]

def append_line(world, size, xr, y):

    if size:
        if y < 0 or y > size[1]:
            return
        xr = (max(xr[0], 0), min(xr[1], size[0]))

    if y in world:
        overlaps = [r for r in world[y] if overlap(xr, r)]

        if len(overlaps) > 0:
            for o in overlaps:
                world[y].remove(o)

            overlaps.append(xr)
            xlist = [x for o in overlaps for x in o]
            xr = (min(xlist), max(xlist))
        world[y].append(xr)
    else:
        world[y] = [xr]


def append_reading(world, size, sensor, beacon):
    dist = sum((abs(beacon[0] - sensor[0]), abs(beacon[1] - sensor[1])))

    for y in range(sensor[1] - dist, sensor[1] + dist + 1):
        w = dist - abs(y - sensor[1])
        append_line(world, size, (sensor[0] - w, sensor[0] + w + 1), y)

def append_line_on_y(sensor, beacon, line, y):
    bdist = sum((abs(beacon[0] - sensor[0]), abs(beacon[1] - sensor[1])))
    ldist = y - sensor[1]
    lwidth = bdist - abs(ldist)

    if lwidth >= 0:
        for x in range(sensor[0] - lwidth, sensor[0] + lwidth + 1):
            if not (beacon[0] == x and beacon[1] == y):
                line.add(x)

with open('15.input') as file:
    data = [[int(part) for part in re.split(', |: |=| ', line.strip()) if part.lstrip('-').isdigit()] for line in file]

    line = set()

    for d in data:
        append_line_on_y((d[0], d[1]), (d[2], d[3]), line, 2000000 if file.name == '15.input' else 10)

    print(len(line))

    world = {}
    size = (4000000, 4000000) if file.name == '15.input' else (20, 20)

    for d in data:
        append_reading(world, size, (d[0], d[1]), (d[2], d[3]))

    pos = [(sorted([x for xr in world[y] for x in xr])[1], y) for y in world if len(world[y]) > 1][0]

    print(pos[0] * 4000000 + pos[1])