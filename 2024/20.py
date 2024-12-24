#!/usr/bin/env python3
import sys
import time
from collections import defaultdict

def init_anim():
    print("\033[2J\033[H", end="")  # Clear the screen and move the cursor to the top-left corner
    print("\033[?25l", end="")  # Hide the cursor for better animation visuals

def exit_anim():
    print("\033[?25h", end="")  # Show the cursor again after animation


def print_map(map, visited, use_dist = False):
    for y in range(len(map)):
        for x in range(len(map[0])):
            if map[y][x] == 1:
                print('#', end='')
            elif (x, y) in visited:
                if use_dist:
                    print(visited[(x, y)] % 10, end='')
                else:
                    print('O', end='')
            else:
                print('.', end='')
        print('')

def animate(map, visited, use_dist = False):
    print("\033[H", end="")  # Move cursor to the top-left of the console
    print_map(map, visited, use_dist)

def traverse(map, start, end, animated=False):
    visited = {start: 0}
    queue = [(start, 0)]

    while queue:
        pos, steps = queue.pop(0)

        if pos == end:
            return visited

        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_pos = (pos[0] + dx, pos[1] + dy)

            if new_pos in visited:
                continue

            if new_pos[0] < 0 or new_pos[1] < 0 or new_pos[1] >= len(map) or new_pos[0] >= len(map[0]):
                continue

            if map[new_pos[1]][new_pos[0]] == 1:
                continue

            visited[new_pos] = steps + 1
            queue.append((new_pos, steps + 1))

            if animated:
                animate(map, visited, True)
                time.sleep(0.01)

    return visited

def inside(map, pos):
    return 0 <= pos[0] < len(map[0]) and 0 <= pos[1] < len(map)

def manhattan_neighbors(pos, n):
    for dx in range(-n, n + 1):  # dx ranges from -n to n
        for dy in range(-n, n + 1):  # dy ranges from -n to n
            dist = abs(dx) + abs(dy)  # Calculate the Manhattan distance
            if dist <= n:  # Manhattan distance condition
                yield ((pos[0] + dx, pos[1] + dy), dist)  # Yield position and distance

def calc_cheats(map, visited, cheat):
    paths = defaultdict(set)
    for pos, dist in visited.items():
        for pos, cheat_dist in manhattan_neighbors(pos, cheat):
            if pos in visited:
                if visited[pos] > (dist + cheat_dist):
                    diff = visited[pos] - (dist + cheat_dist)
                    paths[diff].add((pos, dist, cheat_dist))
    return paths

with open("20.input") as file:
    map = []
    player = (None, None)
    end = (None, None)

    for y, line in enumerate(file):
        row_walls = [1 if char == '#' else 0 for char in line.strip()]

        if 'S' in line:
            x = line.index('S')
            player = (x, y)
        elif 'E' in line:
            x = line.index('E')
            end = (x, y)

        map.append(row_walls)

    animated = file.name.endswith('.example')

    if animated:
        init_anim()
    visited = traverse(map, end, player, animated)
    if animated:
        exit_anim()

    best = visited[player]

    threshold = 0 if file.name.endswith('.example') else 100
    paths = calc_cheats(map, visited, 2)
    print(sum(len(value) for key, value in paths.items() if key >= threshold))

    threshold = 50 if file.name.endswith('.example') else 100
    paths = calc_cheats(map, visited, 20)
    print(sum(len(value) for key, value in paths.items() if key >= threshold))
