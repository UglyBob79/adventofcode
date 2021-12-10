#!/usr/bin/env python3

def findValue(data, bit):
    i = 0
    while len(data) > 1:
        v = bit if sum([b[i] for b in data]) >= len(data) / 2 else ~bit & 0x1
        data = list(filter(lambda b, v=v, i=i: b[i] == v, data))
        i += 1

    return int(''.join([str(i) for i in data[0]]), 2)

with open("3.input") as file:
    data = [[int(x) for x in list(row)] for row in file.read().splitlines()]
    count = [sum(b) for b in list(map(list, zip(*data)))]
    gamma = int(''.join([str(i) for i in list(map(lambda x: 1 if x > len(data) / 2 else 0, count))]), 2)
    eps = ~gamma & (1 << len(data[0])) - 1

    print(gamma*eps)

    ogr = findValue(data.copy(), 1)
    csr = findValue(data.copy(), 0)

    print(ogr*csr)
