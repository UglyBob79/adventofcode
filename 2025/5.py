#!/usr/bin/env python3

def is_fresh(ingredient, ranges):
    for (a, b) in ranges:
        if ingredient in range(a, b + 1):
            return True
    return False

def is_overlap(r1, r2):
    return r1[0] <= r2[0] <= r1[1] or r2[0] <= r1[0] <= r2[1]

def merge(r1, r2):
    return (min(r1[0], r2[0]), max(r1[1], r2[1]))

def merge_ranges(ranges):
    out = set()

    while len(ranges) > 0:
        curr = ranges.pop()
        target = None

        for r in ranges:
            if is_overlap(curr, r):
                target = r
                break

        if target:
            ranges.remove(target)
            ranges.add(merge(curr, target))
        else:
            out.add(curr)
    
    return out

with open("5.input") as file:
    data = [line.strip() for line in file.readlines()]

    ranges = {
        (int(a), int(b))
        for line in data
        if '-' in line
        for a, b in [line.split('-')]
    }
    ingredients = [int(line) for line in data if line.isdigit()]
    
    fresh = [ingredient for ingredient in ingredients if is_fresh(ingredient, ranges)]
    print(len(fresh))

    merged = merge_ranges(ranges)
    print(sum((b - a + 1) for (a, b) in merged))
    
    
