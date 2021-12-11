#!/usr/bin/env python3
import math
def mapFunc(x, y, size):
    if x == 0 or x == size[0] - 1:
        if y == 0 or y == size[1] - 1:
            return 2
        else:
            return 3
    elif y == 0 or y == size[1] - 1:
        if x == 0 or x == size[0] - 1:
            return 2
        else:
            return 3
    else:
        return 4

def updateMap(x, y, value, m, data):
    if x < 0 or x == len(m[0]) or y < 0 or y == len(m):
        return

    if data[x][y] < value:
        m[x][y] -= 1

def calcBasin(x, y, data):
    if x < 0 or x == len(data[0]) or y < 0 or y == len(data) or data[x][y] >= 9:
        return 0

    data[x][y] = 10
    return 1 + calcBasin(x - 1, y, data) + calcBasin(x + 1, y, data) + calcBasin(x, y - 1, data) + calcBasin(x, y + 1, data)

with open("9.input") as file:
    data = [[int(x) for x in list(row)] for row in file.read().splitlines()]

    sizeX = len(data[0])
    sizeY = len(data)

    match = [[mapFunc(x,y,(sizeX,sizeY)) for x in range(sizeX)] for y in range(sizeY)]

    for y in range(sizeY):
        for x in range(sizeX):
            v = data[x][y]
            updateMap(x - 1, y, v, match, data)
            updateMap(x + 1, y, v, match, data)
            updateMap(x, y - 1, v, match, data)
            updateMap(x, y + 1, v, match, data)

    risk = 0
    lows = []

    for y in range(sizeY):
        for x in range(sizeX):
            if match[x][y] == 0:
                risk += 1 + data[x][y]
                lows.append((x, y))

    print(risk)

    basins = []

    for low in lows:
        basins.append(calcBasin(low[0], low[1], data))

    basins.sort()

    print(math.prod(basins[-3:]))
