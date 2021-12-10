#!/usr/bin/env python3
with open("6.input") as file:
    data = [int(x) for x in file.read().strip().split(',')]

    days = 80
    fish = data.copy()
    while days > 0:
        l = len(fish)
        for i in range(l):
            fish[i] -= 1
            if fish[i] < 0:
                fish[i] = 6
                fish.append(8)
        days -= 1

    print(len(fish))

    fish = [data.count(x) for x in range(9)]
    print(fish)

    days = 256
    while days > 0:
        new = fish.pop(0)
        fish[6] += new
        fish.append(new)

        days -= 1

    print(sum(fish))
