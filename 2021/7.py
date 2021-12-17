#!/usr/bin/env python3
with open("7.input") as file:
    data = [int(x) for x in file.read().strip().split(',')]

    r = range(min(data), max(data) + 1)

    fuel = []
    for i in r:
        fuel.append(sum([abs(d - i) for d in data]))

    print(min(fuel))

    fuelCost = [sum(range(i)) for i in range(1, r.stop + 1)]

    fuel = []
    for i in r:
        fuel.append(sum([fuelCost[abs(d - i)] for d in data]))

    print(min(fuel))
