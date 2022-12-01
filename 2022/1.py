#!/usr/bin/env python3

import itertools

with open("1.input") as file:
    data = [int(x.strip()) if x.strip() else None for x in file.readlines()]

    elfs = [sum(list(y)) for x, y in itertools.groupby(data, lambda z: z == None) if not x]
    elfs.sort()

    print(elfs[-1])
    print(sum(elfs[-3:]))