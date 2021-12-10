#!/usr/bin/env python3
with open("10.input") as file:
    data = file.read().splitlines()

    brackets = {']': '[', ')': '(', '}': '{', '>': '<'}

    point = {')': 3, ']': 57, '}': 1197, '>': 25137}
    cPoint = {'(': 1, '[': 2, '{': 3, '<': 4}

    points = 0
    cPoints = []

    for line in data:
        stack = []
        err = False
        for(c) in line:
            if c in brackets.values():
                # open bracket
                stack.append(c)
            else:
                if brackets[c] == stack[-1]:
                    # close bracket
                    stack.pop()
                else:
                    # error
                    points += point[c]
                    err = True
                    break

        # complete
        if not err:
            cPoints.append(0)

            while len(stack) > 0:
                cPoints[-1] *= 5
                cPoints[-1] += cPoint[stack.pop()]

    cPoints.sort()

    print(points)
    print(cPoints[int(len(cPoints)/2)])
