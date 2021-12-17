#!/usr/bin/env python3
with open("13.input") as file:
    points = []
    folds = []
    parsePoints = True
    for line in file.read().splitlines():
        if not line:
            parsePoints = False
            continue
        if parsePoints:
            points.append(list(map(int, line.split(','))))
        else:
             folds.append(line.split("fold along ")[1].split('='))

    size = [0, 0]
    for point in points:
        for i in range(len(size)):
            size[i] = max(size[i], point[i] + 1)

    paper = [[0] * (size[1]) for i in range(size[0])]

    for point in points:
        paper[point[0]][point[1]] = 1

    for fold in folds:
        fPos = int(fold[1])
        if fold[0] == 'x':
            for y in range(size[1]):
                paper[fPos][y] = 0
                for x in range(fPos + 1, size[0]):
                    if paper[x][y] == 1:
                        paper[2 * fPos - x][y] = 1
                        paper[x][y] = 0
            size[0] = fPos
        else:
            for x in range(size[0]):
                paper[x][fPos] = 0
                for y in range(fPos + 1, size[1]):
                    if paper[x][y] == 1:
                        paper[x][2 * fPos - y] = 1
                        paper[x][y] = 0
            size[1] = fPos

        if fold == folds[0]:
            print(sum([sum(row) for row in paper]))


    for y in range(size[1]):
        for x in range(size[0]):
            print('#' if paper[x][y] == 1 else '.', end='')
        print()
