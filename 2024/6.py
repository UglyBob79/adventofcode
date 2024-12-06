#!/usr/bin/env python3

dirs = [
  (0, -1),
  (1, 0),
  (0, 1),
  (-1, 0)
]

def in_bounds(map, pos):
  return pos[1] >= 0 and pos[1] < len(map) and pos[0] >= 0 and pos[0] < len(map[pos[1]])

def print_map(map):
  for row in map:
    print("".join(row))

def travese_map(map, start, dir):
  pos = start
  visited = set()

  while in_bounds(map, pos):
    visited.add(pos)
    map[pos[1]][pos[0]] = "X"
    new_pos = (pos[0] + dir[0], pos[1] + dir[1])

    if in_bounds(map, new_pos):
      if map[new_pos[1]][new_pos[0]] == "#":
        dir = dirs[(dirs.index(dir) + 1) % len(dirs)]
      else:
        pos = new_pos
    else:
      break

  return visited

def has_loop(map, start, dir):
  pos = start
  visited = set()
  while in_bounds(map, pos):
    visited.add((pos[0], pos[1], dirs.index(dir)))
    new_pos = (pos[0] + dir[0], pos[1] + dir[1])

    if in_bounds(map, new_pos):
      if map[new_pos[1]][new_pos[0]] == "#":
        dir = dirs[(dirs.index(dir) + 1) % len(dirs)]
      else:
        pos = new_pos

        if (pos[0], pos[1], dirs.index(dir)) in visited:
          return True
    else:
      return False

  return False

with open("6.input") as file:
  map = [list(line.strip()) for line in file]

  start = (0, 0)
  dir = dirs[0]

  for y in range(len(map)):
    for x in range(len(map[y])):
      if map[y][x] == "^":
        start = (x, y)
        map[y][x] = "."
        break

  map_copy = [row.copy() for row in map]

  positions = travese_map(map, start, dir)
  print(len(positions))

  count = 0

  for position in positions:
    if position == start:
      continue

    map = map_copy
    map[position[1]][position[0]] = "#"

    pos = start
    dir = dirs[0]
    if has_loop(map, pos, dir):
      count += 1

    map[position[1]][position[0]] = "."

  print(count)