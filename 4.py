#!/usr/bin/env python3
import sys

def checkWin(board):
    for row in board:
        if not any(row):
            return True

    flip = list(map(list, zip(*board)))

    for row in flip:
        if not any(row):
            return True

def winTurn(board, numbers):
    for i in range(len(numbers)):
        for y in range(len(board)):
            for x in range(len(board[0])):
                if board[y][x] == numbers[i]:
                    board[y][x] = None
                    if checkWin(board):
                        return i

    return sys.maxsize

def winScore(board, winTurn):


def readFile(filename):
    with open(filename) as file:
        numbers = [int(x) for x in file.readline().strip().split(',')]
        boards = [list(map(int, line.split())) for line in file.read().splitlines() if line]
        boards = [boards[i:i + 5] for i in range(0, len(boards), 5)]

        return (numbers, boards)

(numbers, boards) = readFile("4.input")

winTurns = [winTurn(board, numbers) for board in boards]

winTurn = min(winTurns)
winner = winTurns.index(winTurn)
unmarked = sum([num for row in boards[winner] for num in row if num is not None])

print(unmarked * numbers[winTurn])

winTurn = max(winTurns)
winner = winTurns.index(winTurn)
unmarked = sum([num for row in boards[winner] for num in row if num is not None])

print(unmarked * numbers[winTurn])
