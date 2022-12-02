#!/usr/bin/env python3

# A: Rock, B Paper, C Scissors
shape = {
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

need_map = {
    ('A', 'X'): 'C',
    ('A', 'Y'): 'A',
    ('A', 'Z'): 'B',
    ('B', 'X'): 'A',
    ('B', 'Y'): 'B',
    ('B', 'Z'): 'C',
    ('C', 'X'): 'B',
    ('C', 'Y'): 'C',
    ('C', 'Z'): 'A',
}

with open("2.input") as file:
    data = [tuple(map(str, i.strip().split(' '))) for i in file]

games = [(x, shape_map[y]) for (x, y) in data]
score = [shape[y] + score_map[(x, y)] for (x, y) in games]

print(sum(score))

games = [(x, need_map[(x, y)]) for (x, y) in data]
score = [shape[y] + score_map[(x, y)] for (x, y) in games]

print(sum(score))
