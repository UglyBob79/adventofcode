#!/usr/bin/env python3

import numpy as np
import sys
import math
from copy import deepcopy

MOVES = {
    ( 1,  0),
    (-1,  0),
    ( 0, -1),
    ( 0,  1),
    ( 0,  0)
}

BLIZZ_MOVES = {
    '<': (-1,  0),
    '>': ( 1,  0),
    '^': ( 0, -1),
    'v': ( 0,  1)
}

blizz_cache = []

def move(pos, dir):
    return tuple(sum(v) for v in zip(pos, dir))

def calc_blizzards(first):
    w = len(first[0]) - 2
    h = len(first) - 2
    period = (w * h) // math.gcd(w, h)

    curr = first

    for i in range(0, period):
        next = [[[] for c in row] for row in curr]

        for y in range(len(curr)):
            for x in range(len(curr[y])):
                for i in range(len(curr[y][x])):
                    b_pos = np.array((x, y))
                    b = curr[y][x][i]
                    dir = BLIZZ_MOVES[b]
                    b_pos += dir
                    if b_pos[0] == 0:
                        b_pos[0] = len(curr[y]) - 2
                    if b_pos[0] == len(curr[y]) - 1:
                        b_pos[0] = 1
                    if b_pos[1] == 0:
                        b_pos[1] = len(curr) - 2
                    if b_pos[1] == len(curr) - 1:
                        b_pos[1] = 1

                    next[b_pos[1]][b_pos[0]].append(b)

        blizz_cache.append(next)
        curr = next

def get_blizzard(index):
    return blizz_cache[index]

def inside(map, start, end, pos):
    return (0 < pos[0] < (len(map[0]) - 1) and 0 < pos[1] < (len(map) - 1)) or (pos == start) or (pos == end)

def walk(map, blizzards, start, end, step=0):
    pos = np.array(start)
    w = len(map[0]) - 2
    h = len(map) - 2
    period = (w * h) // math.gcd(w, h)

    q = [(step, start)]

    while q:
        step, pos = q.pop(0)

        if map[pos[1]][pos[0]] == '.':
            map[pos[1]][pos[0]] = [sys.maxsize] * period


        if step < map[pos[1]][pos[0]][step % period]:
            map[pos[1]][pos[0]][step % period] = step

            if pos == end:
                continue

            blizzards = get_blizzard(step % period)

            # for dir blaha
            for dir in MOVES:
                dest = (pos[0] + dir[0], pos[1] + dir[1])

                if inside(map, start, end, dest) and not blizzards[dest[1]][dest[0]]:
                    q.append((step + 1, dest))

    return min(map[end[1]][end[0]])

def simulate(map, blizzards):
    calc_blizzards(blizzards)

    start = ([i for i,v in enumerate(map[0]) if v[0] == '.'][0], 0)
    end = ([i for i,v in enumerate(map[len(map) - 1]) if v[0] == '.'][0], len(map) - 1)

    step = walk(deepcopy(map), blizzards, start, end)
    print(step)

    step = walk(deepcopy(map), get_blizzard(step % 700), end, start, step)
    step = walk(map, get_blizzard(step % 700), start, end, step)
    print(step)

with open('24.input') as file:
    map = [[c for c in line] for line in file.read().splitlines()]
    blizzards = [[[c] if c in ['<', '>', '^', 'v'] else [] for c in row] for row in map]
    map = [[c if c in ['.', '#'] else '.' for c in row] for row in map]

    simulate(map, blizzards)
