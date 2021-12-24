#!/usr/bin/env python3
from functools import lru_cache
import sys

# game board:
# [ ]-[ ]-|-[ ]-|-[ ]-|-[ ]-|-[ ]-[ ]
#        [ ]   [ ]   [ ]   [ ]
#        [ ]   [ ]   [ ]   [ ]
#  0   1    2     3    4    5     6    7    8     9    10   11    12   13  14
# [ ]-[ ]-[b00]-[b01]-[ ]-[b10]-[b11]-[ ]-[b20]-[b21]-[ ]-[b30]-[b31]-[ ]-[ ]
#

corridor = [0, 1, 4, 7, 10, 13, 14]
burrow = [None, None, 'A', 'A', None, 'B', 'B', None, 'C', 'C', None, 'D', 'D', None, None]
burrows = {'A': [2, 3], 'B': [5, 6], 'C': [8, 9], 'D': [11, 12]}
top = [2, 5, 8, 11]
bottom = [3, 6, 9, 12]
cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

minCost = sys.maxsize

@lru_cache(maxsize=None)
def getMoves(board):
    moves = []

    for c in corridor: # from corridor to burrow
        a = board[c]
        if a != ' ':
            b = burrows[a][1]
            path = [d for d in corridor if min(b, c) <= d <= max(b, c) and d != c]
            blocked = False
            for p in path:
                if board[p] != ' ': # no passage
                    blocked = True
                    break
            if not blocked:
                if board[burrows[a][1]] == ' ':
                    moves.append((c, burrows[a][1]))
                elif board[burrows[a][0]] == ' ' and board[burrows[a][1]] == a:
                    moves.append((c, burrows[a][0]))
    for a in top: # from top burrow to corridor
        b = board[a]
        if b != ' ' and (burrows[b][0] != a or burrows[board[a + 1]][1] != a + 1):
            for c in corridor:
                path = [d for d in corridor if min(a, c) <= d <= max(a, c)]
                blocked = False
                for p in path:
                    if board[p] != ' ': # no passage
                        blocked = True
                        break
                if not blocked:
                    moves.append((a, c))
    for a in bottom: # from bottom burrow to corridor
        b = board[a]
        if b != ' ' and board[a - 1] == ' ' and burrows[b][1] != a: # not blocked by top burrow
            for c in corridor:
                path = [d for d in corridor if min(a, c) <= d <= max(a, c)]
                blocked = False
                for p in path:
                    if board[p] != ' ': # no passage
                        blocked = True
                        break
                if not blocked:
                    moves.append((a, c))
    return moves

@lru_cache(maxsize=None)
def getCost(type, move):
    s = move[0] if burrow[move[0]] else move[1]
    e = move[1] if burrow[move[0]] else move[0]
    step = 0
    if s in bottom:
        step += 1
        s -= 1
    if s in top:
        path = [d for d in corridor if min(s, e) <= d <= max(s, e)]
        for p in path:
            step += 2 if p != 0 and p != 14 else 1

    return step * cost[type]

@lru_cache(maxsize=None)
def traverse(board, move, totCost):
    global minCost

    c = getCost(board[move[0]], move)
    totCost += c

    if totCost > minCost:
        return

    board = board[:move[1]] + board[move[0]] + board[move[1] + 1:]
    board = board[:move[0]] + ' ' + board[move[0] + 1:]

    if board == '  AA BB CC DD  ':
        minCost = min(minCost, totCost)
        return

    moves = getMoves(board)

    for move in moves:
        traverse(board, move, totCost)

def simulate(board):
    moves = getMoves(board)

    for move in moves:
        traverse(board, move, 0)

if __name__ == '__main__':
    with open("23.input") as file:
        data = [row.strip() for row in file.readlines()]

        board = [' '] * 15

        for i in range(4):
            board[2 + 3 * i] = data[2].split('#')[3:][:4][i]
            board[2 + 3 * i + 1] = data[3].split('#')[1:][:4][i]

        board = ''.join(board)

        simulate(board)

        print(minCost)
