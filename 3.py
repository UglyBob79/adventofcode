#!/usr/bin/env python3

with open("3.input") as file:
    data = [[int(x) for x in list(row)] for row in file.read().splitlines()]

    count = [sum(b) for b in list(map(list, zip(*data)))]
    gamma = int(''.join([str(i) for i in list(map(lambda x: 1 if x > len(data) / 2 else 0, count))]), 2)
    eps = ~gamma & 0xFFF

    print(gamma*eps)
