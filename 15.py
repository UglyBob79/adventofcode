#!/usr/bin/env python3
import sys

def shortest(grid):
    distance = [[sys.maxsize for x in list(row)] for row in grid]

    dx = [-1, 0, 1, 0]
    dy = [0, -1, 0, 1]

    st = set()

    st.add((0, 0, 0))
    distance[0][0] = grid[0][0]

    while len(st) > 0:
        c = st.pop()

        for i in range(4):
            x = c[0] + dx[i]
            y = c[1] + dy[i]
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
    cavern[0][0] = 0

    print(shortest(cavern))
