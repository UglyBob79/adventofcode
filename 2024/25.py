#!/usr/bin/env python3

with open("25.input") as file:
    locks = []
    keys = []

    curr = None

    for line in file:
        line = line.strip()

        if line == "":
            curr = None
            continue

        if curr is None:
            curr = [-1] * len(line)
            if line.startswith("#"):
                locks.append(curr)
            else:
                keys.append(curr)

        for i in range(len(line)):
            if line[i] == "#":
                curr[i] += 1

    count = sum(1 for lock in locks for key in keys if all(l + k < 6 for l, k in zip(lock, key)))
    print(count)