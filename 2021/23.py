#!/usr/bin/env python3
import sys
from functools import lru_cache

#
#    0   1    2    3    4    5    6    7    8    9   10
# 0 [ ]-[ ]-[   ]-[ ]-[   ]-[ ]-[   ]-[ ]-[   ]-[ ]-[ ]
# 1         [   ]     [   ]     [   ]     [   ]
# 2         [   ]     [   ]     [   ]     [   ]
# 3         [   ]     [   ]     [   ]     [   ]
# 4         [   ]     [   ]     [   ]     [   ]
#

corridor = [0, 1, 3, 5, 7, 9, 10]
burrows = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
burrow = [None, None, 'A', None, 'B', None, 'C', None, 'D', None, None]
cost = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

minCost = sys.maxsize

@lru_cache(maxsize=None)
def getMoves(board):
    moves = []
    for i in range(len(board)):
        # corridor to burrow
        if i in corridor:
            b = board[i][0]
            if b != ' ':
                d = burrows[b]
                for j in range(4, 0, -1):
                    if board[d][j]:
                        if board[d][j] == ' ':
                            # move to burrow
                            path = [a for a in corridor if min(i, d) <= a <= max(i, d)]
                            blocked = False
                            for p in path:
                                if p != i and board[p][0] != ' ': # no passage
                                    blocked = True
                                    break
                            if not blocked:
                                moves.append(((i, 0), (d, j)))
                            break
                        elif board[d][j] != burrow[d]:
                            # no move possible
                            break
        # burrow to corridor
        if burrow[i]:
            top = None
            move = False
            for j in range(1, 5):
                if board[i][j] and board[i][j] != ' ':
                    if not top:
                        top = j
                    if board[i][j] != burrow[i]:
                        move = True
            if move:
                for c in corridor:
                    path = [d for d in corridor if min(i, c) <= d <= max(i, c)]
                    blocked = False
                    for p in path:
                        if board[p][0] != ' ': # no passage
                            blocked = True
                            break
                    if not blocked:
                        blocked = True
                        moves.append(((i, top), (c, 0)))
    return tuple(moves)

def done(board):
    for i in [2, 4, 6, 8]:
        for j in range(1, 5):
            if board[i][j] and board[i][j] != burrow[i]:
                return False
    return True

@lru_cache(maxsize=None)
def getCost(type, move):
    return cost[type] * (abs(move[0][0] - move[1][0]) + abs(move[0][1] - move[1][1]))

def findOptMove(board, moves):
    for move in moves:
        if move[0][1] == 0: # corridor
            return move

@lru_cache(maxsize=None)
def traverse(board, move, totCost):
    global minCost

    totCost += getCost(board[move[0][0]][move[0][1]], move)

    if totCost >= minCost:
        return

    board = tuple(tuple(a if (i, j) not in move
        else (' ' if (i, j) == move[0]
        else board[move[0][0]][move[0][1]])
        for j, a in enumerate(b)) for i, b in enumerate(board))

    if done(board):
        minCost = min(minCost, totCost)
        return

    moves = getMoves(board)
    if len(moves) == 0:
        return

    optMove = findOptMove(board, moves)
    if optMove:
        traverse(board, optMove, totCost)
    else:
        for move in moves:
            traverse(board, move, totCost)

def simulate(board):
    global corridor
    d = max([len([a for a in b if a]) for b in board])
    corridor = [1, 3, 5, 7, 9] if d == 3 else [0, 1, 3, 5, 7, 9, 10]
    for move in getMoves(board):
        traverse(board, move, 0)

if __name__ == '__main__':
    with open("23.input") as file:
        data = [row.strip() for row in file.readlines()]

        board = []
        for i in range(11):
            if 2 <= i <= 8 and i % 2 == 0:
                board.append(tuple((' ', data[2].split('#')[3:][:4][(i -2) // 2], data[3].split('#')[1:][:4][(i - 2) // 2], None, None)))
            else:
                board.append(tuple(' '))
        simulate(tuple(board))
        print(minCost)

        data.append('#D#C#B#A#')
        data.append('#D#B#A#C#')
        minCost = sys.maxsize
        board = []
        for i in range(11):
            if 2 <= i <= 8 and i % 2 == 0:
                board.append(tuple((' ', data[2].split('#')[3:][:4][(i -2) // 2], data[5].split('#')[1:][:4][(i -2) // 2], data[6].split('#')[1:][:4][(i -2) // 2], data[3].split('#')[1:][:4][(i - 2) // 2])))
            else:
                board.append(tuple(' '))
        simulate(tuple(board))
        print(minCost)
