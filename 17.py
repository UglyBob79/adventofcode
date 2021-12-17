#!/usr/bin/env python3
def checkHit(x, y, tRange):
    return tRange[0][0] <= x <= tRange[0][1] and tRange[1][1] >= y >= tRange[1][0]

def hit(xs, ys, tRange):
    x = 0
    y = 0

    while x <= max(tRange[0]) and y >= min(tRange[1]):
        if checkHit(x, y, tRange):
            return True
        x += xs
        y += ys
        if xs > 0:
            xs -= 1
        ys -= 1

with open("17.input") as file:
    tRange = [tuple([int(v) for v in str.split("..")]) for str in file.readline().strip().split(": x=")[1].split(", y=")]
    speedRange = ([0, max(tRange[0])], [min(tRange[1]), -1 * (min(tRange[1]) + 1)])

    y = 0
    ys = speedRange[1][1]
    while ys > 0:
        y += ys
        ys -= 1

    print(y)

    hits = []
    for ys in range(speedRange[1][0], speedRange[1][1] + 1):
        for xs in range(speedRange[0][0], speedRange[0][1] + 1):
            if hit(xs, ys, tRange):
                hits.append(())

    print(len(hits))
