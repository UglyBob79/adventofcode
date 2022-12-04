#!/usr/bin/env python3

with open("3.input") as file:
    data = file.read().splitlines()

    score = sum(map(lambda a: ord(a) + (-96 if a.islower() else -38), [set.intersection(set(l[:int(len(l)/2)]), set(l[int(len(l)/2):])).pop() for l in data]))
    print(score)

    score = sum(map(lambda a: ord(a) + (-96 if a.islower() else -38), [set.intersection(*[set(y) for y in x]).pop() for x in zip(*(iter(data),) * 3)]))
    print(score)
