#!/usr/bin/env python3

# A: Rock, B Paper, C Scissors
shape_score = {
    'A': 1,
    'B': 2,
    'C': 3
}

shape_map = {
    'X': 'A',
    'Y': 'B',
    'Z': 'C'
}

score_map = {
    ('A', 'A'): 3,
    ('A', 'B'): 6,
    ('A', 'C'): 0,
    ('B', 'A'): 0,
    ('B', 'B'): 3,
    ('B', 'C'): 6,
    ('C', 'A'): 6,
    ('C', 'B'): 0,
    ('C', 'C'): 3
}

need = {
    'X': 2,
    'Y': 0,
    'Z': 1
}

with open("2.input") as file:
    data = [tuple(map(str, i.strip().split(' '))) for i in file]

games = [(x, shape_map[y]) for (x, y) in data]
score = [shape_score[y] + score_map[(x, y)] for (x, y) in games]

print(sum(score))

games = [(x, chr(ord('A') + (ord(x) - ord('A') + need[y]) % 3)) for (x, y) in data]
score = [shape_score[y] + score_map[(x, y)] for (x, y) in games]

print(sum(score))