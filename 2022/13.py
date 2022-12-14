#!/usr/bin/env python3
import ast
from itertools import zip_longest
from functools import cmp_to_key
import math

def compare(a, b):
    if isinstance(a, int) and isinstance(b, list):
        a = [a]
    if isinstance(a, list) and isinstance(b, int):
        b = [b]

    if isinstance(a, int) and isinstance(b, int):
        return a - b
    elif isinstance(a, list) and isinstance(b, list):
        for x, y in zip_longest(a, b):
            if x is None:
                return -1
            elif y is None:
                return 1

            c = compare(x, y)
            if c != 0:
                return c
        return 0

with open('13.input') as file:
    data = [ast.literal_eval(line) for line in file.read().splitlines()if line.strip()]

    print(sum([i // 2 + 1 if compare(data[i], data[i + 1]) <= 0 else 0 for i in range(0, len(data), 2)]))

    dividers = [[[2]], [[6]]]
    data = sorted(data + dividers, key=cmp_to_key(compare))

    print(math.prod([data.index(d) + 1 for d in dividers]))