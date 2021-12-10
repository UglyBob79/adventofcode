#!/usr/bin/env python3
with open("10.input") as file:
    data = file.read().splitlines()

    brackets = {']': '[', ')': '(', '}': '{', '>': '<'}
    point = {')': 3, ']': 57, '}': 1197, '>': 25137}

    points = 0

    for line in data:
        stack = []
        for(c) in line:
            if c in brackets.values():
                stack.append(c)
            else:
                if brackets[c] == stack[-1]:
                    stack.pop()
                else:
                    points += point[c]
                    break

    print(points)
