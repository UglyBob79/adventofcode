#!/usr/bin/env python3

def find_best(bank, n):
    a = 0
    b = len(bank) - n + 1
    out = 0
    
    for _ in range(0, n):
        search = bank[a:b]
        m = max(search)
        out = out * 10 + m
        a = a + search.index(m) + 1
        b += 1

    return out

def total_output(batteries, n):
    return sum(find_best(bank, n) for bank in batteries)

with open("3.input") as file:
    data = [list(int(x) for x in line.strip()) for line in file.readlines()]

    print(total_output(data, 2))
    print(total_output(data, 12))
