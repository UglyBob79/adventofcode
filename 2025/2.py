#!/usr/bin/env python3

def is_invalid(value):
    s = str(value)
    n = len(s)

    if n % 2 == 0:
        n //= 2
        return s[:n] == s[n:]
    else:
        return False

def is_invalid_b(value):
    s = str(value)
    n = len(s) // 2

    for i in range(n, 0, -1):
        if len(set(split_str(s, i))) == 1:
            return True

    return False

def split_str(s, n):
    for i in range(0, len(s), n):
            yield s[i:i + n]

def find_invalids(data, part2=False):
    for a, b in data:
        for i in range(a, b + 1):
            if not part2 and is_invalid(i) or part2 and is_invalid_b(i):
                yield i

with open("2.input") as file:
    data = [tuple(map(int, x.split('-'))) for x in file.readline().split(',')]

    print(sum(list(find_invalids(data))))
    print(sum(list(find_invalids(data, part2=True))))


