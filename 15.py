#!/usr/bin/env python3
import sys

def shortest(grid):
    distance = [[sys.maxsize for x in list(row)] for row in grid]
    delta = [[-1, 0, 1, 0], [0, -1, 0, 1]]

    st = set()

    st.add((0, 0, 0))
    distance[0][0] = 0

    while len(st) > 0:
        c = st.pop()

        for i in range(len(delta[0])):
            (x , y) = (c[0] + delta[0][i], c[1] + delta[1][i])

            if x < 0 or x == len(grid) or y < 0 or y == len(grid[0]):
                continue

            if distance[x][y] > distance[c[0]][c[1]] + grid[x][y]:
                if distance[x][y] != sys.maxsize:
                    try:
                        st.remove((x, y, distance[x][y]))
                    except KeyError:
                        pass

                distance[x][y] = distance[c[0]][c[1]] + grid[x][y]
                st.add((x, y, distance[x][y]))

    return distance[len(grid) - 1][len(grid[0]) - 1]

with open("15.input") as file:
    cavern = [[int(x) for x in list(row)] for row in file.read().splitlines()]

    print(shortest(cavern))

    expand = list()

    for i in range(5):
        for x in range(len(cavern)):
            expand.append([])
            for j in range(5):
                for y in range(len(cavern[0])):
                    expand[i * len(cavern) + x].append((cavern[x][y] + i + j - 1) % 9 + 1)

    print(shortest(expand))
