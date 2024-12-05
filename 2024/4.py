#!/usr/bin/env python3

dirs = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1] if not (x == 0 and y == 0)]
xmas = "XMAS"
mas = "MAS"

def is_match(map, word, x, y, dir):
  for i in range(len(word)):
    if x < 0 or y < 0 or y >= len(map) or x >= len(map[y]):
      return False
    if map[y][x] != word[i]:
      return False
    x += dir[0]
    y += dir[1]
  return True

with open("4.input") as file:
  map = [list(line.strip()) for line in file]

  count = 0;

  for y in range(len(map)):
    for x in range(len(map[y])):
      for dir in dirs:
        if is_match(map, xmas, x, y, dir):
          count += 1

  print(count)

  count = 0;

  for y in range(len(map)):
    for x in range(len(map[y])):
      if (
        is_match(map, mas, x, y, dirs[7]) and is_match(map, mas, x + 2, y, dirs[2]) or
        is_match(map, mas, x, y, dirs[7]) and is_match(map, mas, x, y + 2, dirs[5]) or
        is_match(map, mas, x + 2, y + 2, dirs[0]) and is_match(map, mas, x + 2, y, dirs[2]) or
        is_match(map, mas, x + 2, y + 2, dirs[0]) and is_match(map, mas, x, y + 2, dirs[5])
      ):
        count += 1

  print(count)