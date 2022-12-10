#!/usr/bin/env python3

with open("10.input") as file:
    instr = [(i[0], int(i[1]) if len(i) > 1 else None) for i in [line.split(' ') for line in file.read().splitlines()]]

    pipe = []

    for i in instr:
        if i[0] == 'addx':
            pipe.append(('noop', None))
        pipe.append(i)

    x = 1
    strength = 0
    crt = '\n'

    for c in range(1, 241):
        i = pipe.pop(0)

        crt += '#' if ((c - 1) % 40) in [x - 1, x, x + 1] else '.'
        if (c % 40) == 0:
            crt += '\n'

        if c in [20, 60, 100, 140, 180, 220]:
            strength += c * x

        if i[0] == 'addx':
            x += i[1]

    print(strength)
    print(crt)