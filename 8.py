#!/usr/bin/env python3
import re

def parseLine(line):
    (signals, output) = line.split('|')
    signals = [''.join(sorted(s)) for s in signals.split()]
    output = [''.join(sorted(o)) for o in output.split()]

    return (signals, output)

def diff(c1, c2):
    o = ''
    for c in c1:
        if c not in c2:
            o += c
    for c in c2:
        if c not in c1:
            o += c
    return ''.join(sorted(o))

def common(codes):
    segments = ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    sets = [set(x) for x in codes]
    return ''.join(sorted(list(sets[0].intersection(*sets[1:]))))

def decode(row, count):
    codes = [None] * 10
    segments = [None] * 7

    for signal in row[0]:
        if len(signal) == 2:
            codes[1] = signal
        elif len(signal) == 4:
            codes[4] = signal
        elif len(signal) == 3:
            codes[7] = signal
        elif len(signal) == 7:
            codes[8] = signal

    # top segment
    c = diff(codes[1], codes[7])
    segments[0] = c

    # mid segment
    segments[3] = common(list(filter(lambda x : len(x) == 5 or len(x) == 4, row[0])))

    # top left segment
    segments[1] = diff(diff(codes[4], codes[1]), segments[3])

    # bottom segment
    segments[6] = common(list(filter(lambda x : len(x) == 5 or len(x) == 6, row[0]))).replace(segments[0], "")

    codes[5] = [i for i in list(filter(lambda x : len(x) == 5, row[0])) if segments[1] in i][0]
    codes[0] = [i for i in list(filter(lambda x : len(x) == 6, row[0])) if segments[3] not in i][0]

    # bottom right segment
    segments[5] = common([codes[5], codes[1]])

    # top right segment
    segments[2] = diff(codes[1], segments[5])

    # bottom left segment
    segments[4] = diff(codes[0], codes[5]).replace(segments[3], "").replace(segments[2], "")

    codes[2] = ''.join(sorted([segments[0], segments[2], segments[3], segments[4], segments[6]]))
    codes[3] = ''.join(sorted([segments[0], segments[2], segments[3], segments[5], segments[6]]))
    codes[6] = ''.join(sorted([segments[0], segments[1], segments[3], segments[4], segments[5], segments[6]]))
    codes[9] = ''.join(sorted([segments[0], segments[1], segments[2], segments[3], segments[5], segments[6]]))

    value = 0
    for output in row[1]:
        if output in codes:
            i = codes.index(output)
            count[i] += 1
            value *= 10
            value += i

    return value

with open("8.input") as file:
    data = [parseLine(line) for line in file.read().splitlines()]

    count = [0] * 10
    sum = 0
    for row in data:
        v = decode(row, count)
        sum += v

    print(count[1] + count[4] + count[7] + count[8])
    print(sum)
