#!/usr/bin/env python3
import numpy as np
import copy

def srange(start, end, step=1, inclusive=False):
    sign = np.sign(end - start)
    return range(start, end + sign if inclusive else end, step * sign)

def draw_line(world, start, end, chr):
    if start[0] == end[0]:
        for y in srange(start[1], end[1], 1, True):
            draw_point(world, (start[0], y), chr)
    else:
        for x in srange(start[0], end[0], 1, True):
            draw_point(world, (x, start[1]), chr)

def draw_point(world, pos, chr):
    world[pos] = chr

def rain_sand(world, pos, max_y=None):
    count = 0
    while True:
        if pos in world: # full to generator
            break

        sand = np.array(pos)

        for i in range(1000):
            if max_y is not None and (sand + (0,1))[1] == max_y:
                draw_point(world, tuple(sand), 'o')
                count += 1
                break

            if not tuple(sand + (0,1)) in world:
                sand += (0,1)
            elif not tuple(sand + (-1, 1)) in world:
                sand += (-1,1)
            elif not tuple(sand + (1, 1)) in world:
                sand += (1,1)
            else:
                draw_point(world, tuple(sand), 'o')
                count += 1
                break

        if i == 999: # out of bounds
            break

    return count

with open('14.input') as file:
    data = [list(zip(row, row[1:])) for row in [[tuple([int(v) for v in point.split(',')]) for point in line.split(' -> ')] for line in file.read().splitlines()]]

    world = {}

    for row in data:
        for seg in row:
            draw_line(world, seg[0], seg[1], '#')

    print(rain_sand(copy.deepcopy(world), (500, 0)))
    print(rain_sand(copy.deepcopy(world), (500, 0), max(pos[1] for pos in world.keys()) + 2))
