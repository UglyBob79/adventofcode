#!/usr/bin/env python3
import copy

dir = [
    (-1, -1),
    (-1,  0),
    (-1,  1),
    (0,  -1),
    (0,   1),
    (1,  -1),
    (1,   0),
    (1,   1)
]

def flash(x, y, board):
    if x < 0 or x == len(board[0]) or y < 0 or y == len(board) or board[x][y] > 9:
        return

    board[x][y] += 1

def update(board):
    for y in range(len(board)):
        for x in range(len(board[0])):
            board[x][y] += 1

    while True:
        flashing = False
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[x][y] == 10:
                    board[x][y] += 1
                    for (dx, dy) in dir:
                        flash(x + dx, y + dy, board)
                    flashing = True
        if not flashing:
            break

    flashes = 0
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[x][y] > 9:
                board[x][y] = 0
                flashes += 1

    return flashes

with open("11.input") as file:
    data = [[int(x) for x in list(row)] for row in file.read().splitlines()]

    flashes = 0
    board = copy.deepcopy(data)
    for step in range(100):
        flashes += update(board)

    print(flashes)

    flashes = 0
    step = 0
    board = copy.deepcopy(data)
    while flashes != len(board) * len(board[0]):
        flashes = update(board)
        step += 1

    print(step)
