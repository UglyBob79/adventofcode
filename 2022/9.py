#!/usr/bin/env python3

import numpy as np

dir = {
    'U' : (0, -1),
    'D' : (0, 1),
    'L' : (-1, 0),
    'R' : (1, 0)
}

def move(rope, move):
    rope[0] += dir[move]

    for i in range(1, len(rope)):
        delta = rope[i - 1] - rope[i]

        if sum(x*x for x in delta) > 2:
            rope[i] += np.sign(delta)

    return tuple(rope[-1])

with open("9.input") as file:
    moves = [(m[0], int(m[1])) for m in [line.split(' ') for line in file.read().splitlines()]]

    rope = np.zeros((2, 2))
    print(len(set([move(rope, m[0]) for m in moves for i in range(m[1])])))

    rope = np.zeros((10, 2))
    print(len(set([move(rope, m[0]) for m in moves for i in range(m[1])])))