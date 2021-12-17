#!/usr/bin/env python3
with open("5.input") as file:
    data = [int(row.strip().translate(row.maketrans("FLBR", "0011")), 2) for row in file.readlines()]

    print(max(data))
    print(sorted(set(range(data[0], data[-1] + 1)).difference(data))[0])
