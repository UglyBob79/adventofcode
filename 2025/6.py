#!/usr/bin/env python3

import operator
from functools import reduce

with open("6.input") as file:
    data = [line.replace('\n', '') for line in file.readlines()]

    grid = [line.split() for line in data]
    total = 0

    for col in range(len(grid[0])):
        s = int(grid[0][col])
        op = operator.add if grid[len(data) - 1][col] == '+' else operator.mul
        for row in range(1, len(grid) - 1):
            s = op(s, int(grid[row][col]))
        total += s

    print(total)


    values = [[]]
    operators = []

    row = 0
    
    for x in range(len(data[0]) - 1, -1, -1):
        curr = 0
        for y in range(0, len(data)):
            if data[y][x].isdigit():
                curr = curr * 10 + int(data[y][x])
            elif data[y][x] == '*':
                operators.append(operator.mul)
            elif data[y][x] == '+':
                operators.append(operator.add)

        if curr == 0:
            values.append([])
            row += 1
        else:
            values[row].append(curr)
    
    total = sum(reduce(op, vals) for vals, op in zip(values, operators))

    print(total)