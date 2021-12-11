#!/usr/bin/env python3
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
    totalFlashes = 0
    step = 0
    while flashes != len(data) * len(data[0]):
        flashes = update(data)
        totalFlashes += flashes
        step += 1
        if step == 100:
            print(totalFlashes)

    print(step)
