#!/usr/bin/env python3

def find(line, m):
    return [len(set(line[i:i+m])) == m for i in range(len(line))].index(True) + m

with open("6.input") as file:
    line = file.readline()

    print(find(line, 4))
    print(find(line, 14))
