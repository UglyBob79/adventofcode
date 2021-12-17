#!/usr/bin/env python3

with open("2.input") as file:
    data = [([int(y) for y in x.split('-')], y[0], z) for (x, y, z) in [str.strip().split(' ') for str in file.readlines()]]

    print(sum(row[0][0] <= row[2].count(row[1]) <= row[0][1] for row in data))
    print(sum((row[2][row[0][0] - 1] == row[1]) ^ (row[2][row[0][1] - 1] == row[1]) for row in data))
