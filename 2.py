#!/usr/bin/env python3

with open("2.input") as file:
    data = [row.split(' ') for row in file.read().splitlines()]

    x = sum([int(b) for (a,b) in filter(lambda v: v[0] == "forward", data)])
    y = sum([int(b) if a == "down" else -int(b) for (a,b) in filter(lambda v: v[0] == "up" or v[0] == "down", data)])

    print(x*y)
