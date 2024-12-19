#!/usr/bin/env python3

cache = {}

def clothible(cloth, patterns):
    if cloth in cache:
        return cache[cloth]

    if len(cloth) == 0:
        return 1
    else:
        res = sum([clothible(cloth[len(pattern):], patterns) for pattern in patterns if cloth.startswith(pattern)])
        cache[cloth] = res
        return res

with open("19.input") as file:
    patterns = [part.strip() for part in file.readline().split(', ')]
    file.readline()

    cloths = [line.strip() for line in file if line]

    print(sum([clothible(cloth, patterns) > 0 for cloth in cloths]))
    print(sum([clothible(cloth, patterns) for cloth in cloths]))
