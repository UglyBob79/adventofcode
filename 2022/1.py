#!/usr/bin/env python3

import bisect

with open("1.input") as file:
    data = [x.strip() for x in file.readlines()]

    max_val = []
    curr = 0

    for val in data:
        if not val:
            bisect.insort(max_val, curr)
            curr = 0
        else:
            curr += int(val)

    if curr > 0:
        bisect.insort(max_val, curr)

    print(max(max_val))
    print(sum(max_val[-3:]))