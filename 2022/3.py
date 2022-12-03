#!/usr/bin/env python3

with open("3.input") as file:
    data = file.read().splitlines()

    score = sum([sum(map(lambda a: ord(a) + (-96 if ord(a) > 90 else -38), x)) for x in [set(x).intersection(y) for (x,y) in [(l[:int(len(l)/2)], l[int(len(l)/2):]) for l in data]]])
    print(score)

    score = sum([sum(map(lambda a: ord(a) + (-96 if ord(a) > 90 else -38), b)) for b in [set.intersection(*[set(y) for y in x]) for x in zip(*(iter(data),) * 3)]])
    print(score)