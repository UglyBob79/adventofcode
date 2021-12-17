#!/usr/bin/env python3

with open("1.input") as file:
    data = [int(x) for x in file.readlines()]
    diff = [(y-x) for (x,y) in zip(data, data[1:])]
    count = len(list(filter(lambda x: (x > 0), diff)))

    print(count)

    filtered = [(x+y+z) for (x,y,z) in zip(data, data[1:], data[2:])]
    diff = [(y-x) for (x,y) in zip(filtered, filtered[1:])]
    count = len(list(filter(lambda x: (x > 0), diff)))

    print(count)
