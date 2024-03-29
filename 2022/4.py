#!/usr/bin/env python3

with open("4.input") as file:
    data = [[tuple(eval(i) for i in b.split('-')) for b in l.split(',')] for l in file.read().splitlines()]

    print(len([[a, b] for a, b in data if (a[0] >= b[0] and a[1] <= b[1] or b[0] >= a[0] and b[1] <= a[1])]))

    print(len([[a, b] for a, b in data if set(range(a[0], a[1] + 1)).intersection(set(range(b[0], b[1] + 1)))]))
