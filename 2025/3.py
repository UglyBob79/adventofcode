#!/usr/bin/env python3

def find_best(bank, n):
    a = 0
    out = 0
    
    for b in range(len(bank) - n + 1, len(bank) + 1):
        i, m = max(enumerate(bank[a:b]), key=lambda x: x[1])
        out = out * 10 + m
        a = a + i + 1

    return out

def total_output(batteries, n):
    return sum(find_best(bank, n) for bank in batteries)

with open("3.input") as file:
    data = [list(int(x) for x in line.strip()) for line in file.readlines()]

    print(total_output(data, 2))
    print(total_output(data, 12))
