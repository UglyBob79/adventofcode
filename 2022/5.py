#!/usr/bin/env python3

from more_itertools import sliced
from os import system
import copy
import time

def print_supply(supply):
    print("\033[0;0H")

    for x in range(len(supply)):
        l = len(supply[x])
        for y in range(64):
            if y < l:
                print("[%s]" % supply[x][y], end = '')
            else:
                print("   ", end = '')
        print("")
    print("")

def work(supply, moves, batch = False, visualize = False):
    for move in moves:
        supply[move[2]].extend(supply[move[1]][-move[0]:] if batch else reversed(supply[move[1]][-move[0]:]))
        del supply[move[1]][-move[0]:]

        if visualize:
            print_supply(supply)
            time.sleep(0.01)

    return ''.join([s[-1] for s in supply])


with open("5.input") as file:
    supply = [[] for i in range(9)]
    moves = []

    for row in file.read().splitlines():
        if row:
            if row.startswith('move'):
                parts = row.split(' ')
                moves.append((int(parts[1]), int(parts[3]) - 1, int(parts[5]) - 1))
            elif not row.startswith(' 1   2   3   4   5   6   7   8   9'):
                parts = list(sliced(row, 4))

                for i, p in enumerate(parts):
                    if p[1] != ' ' and not p[1].isnumeric():
                        supply[i].insert(0, p[1])

    system('clear')
    print_supply(supply)

    part1 = work(copy.deepcopy(supply), moves, False, True)
    time.sleep(2)
    part2 = work(copy.deepcopy(supply), moves, True, True)

    print("Part 1: " + part1)
    print("Part 2: " + part2)
