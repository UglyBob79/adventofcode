#!/usr/bin/env python3

with open("1.input") as file:
    data = [int(v) for v in file.readlines()]

    done = False
    for x in data:
        for y in data:
            if x + y == 2020:
                print(x * y)
                done = True
                break
        if done:
            break

    for x in data:
        for y in data:
            for z in data:
                if x + y + z == 2020:
                    print(x * y * z)
                    exit()
