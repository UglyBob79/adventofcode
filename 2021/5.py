#!/usr/bin/env python3
import re

p = re.compile("(?P<xs>[0-9]+),(?P<ys>[0-9]+) -> (?P<xe>[0-9]+),(?P<ye>[0-9]+)")

def parseLine(str):
    m = p.match(str)
    return [(int(m.group("xs")), int(m.group("ys"))), (int(m.group("xe")), int(m.group("ye")))]

def drawLine(board, line):
    if line[0][0] == line[1][0]:
        x = line[0][0]
        ys = min(line[0][1], line[1][1])
        ye = max(line[0][1], line[1][1])

        for y in range(ys, ye + 1):
            board[x][y] += 1
    elif line[0][1] == line[1][1]:
        y = line[0][1]
        xs = min(line[0][0], line[1][0])
        xe = max(line[0][0], line[1][0])

        for x in range(xs, xe + 1):
            board[x][y] += 1
    else:
        if  line[0][0] < line[1][0]:
            ps = line[0]
            pe = line[1]
        else:
            ps = line[1]
            pe = line[0]

        dy = 1 if ps[1] < pe[1] else -1
        y = ps[1]
        for x in range(ps[0], pe[0] + 1):
            board[x][y] += 1
            y += dy

with open("5.input") as file:
    lines = [parseLine(line) for line in file.read().splitlines()]

    size = [0, 0]
    for line in lines:
        for point in line:
            for i in range(len(size)):
                size[i] = max(size[i], point[i] + 1)

    straightLines = list(filter(lambda line: line[0][0] == line[1][0] or line[0][1] == line[1][1], lines))
    diagLines = list(filter(lambda line: not (line[0][0] == line[1][0] or line[0][1] == line[1][1]), lines))

    board = [[0] * (size[1]) for i in range(size[0])]

    for line in straightLines:
        drawLine(board, line)

    count = 0
    for y in range(size[1]):
        for x in range(size[0]):
            if board[x][y] > 1:
                count += 1

    print(count)

    for line in diagLines:
        drawLine(board, line)

    count = 0
    for y in range(size[1]):
        for x in range(size[0]):
            if board[x][y] > 1:
                count += 1

    print(count)
