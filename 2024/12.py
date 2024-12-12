#!/usr/bin/env python3
from collections import defaultdict

dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
visited = set()
plot_id = 0
plots = {}

def count_longest_sequences(lst):
    count = 0
    for i in range(len(lst)):
        # Check if it's the start of a new sequence
        if i == 0 or lst[i] != lst[i - 1] + 1:
            count += 1

    return count

def count_sides(plot):
  plot['sides'] = sum(count_longest_sequences(sorted(part)) for fence_dir in plot['fence_parts'].values() for part in fence_dir.values())

def count_fences(garden, pos, plant, id):
    count = 0

    for i, d in enumerate(dirs):
        new_pos = (pos[0] + d[0], pos[1] + d[1])

        if not (0 <= new_pos[0] < len(garden[0]) and 0 <= new_pos[1] < len(garden)) or garden[new_pos[1]][new_pos[0]] != plant:
            count += 1
            axis = 0 if i % 2 == 0 else 1
            plots[id]['fence_parts'][i][new_pos[axis]].append(new_pos[(axis + 1) % 2])


    return count

def find_plot(garden, pos, plant, id):
    if pos in visited or garden[pos[1]][pos[0]] != plant:
        return

    visited.add(pos)

    if id not in plots:
        plots[id] = {'id': id, 'plant': plant, 'size': 0, 'fence': 0, 'fence_parts': defaultdict(lambda: defaultdict(list))}

    plots[id]['size'] += 1
    plots[id]['fence'] += count_fences(garden, pos, plant, id)

    for d in dirs:
        new_pos = (pos[0] + d[0], pos[1] + d[1])

        if 0 <= new_pos[0] < len(garden[0]) and 0 <= new_pos[1] < len(garden):
            find_plot(garden, new_pos, plant, plot_id)

with open("12.input") as file:
    garden = [list(line.strip()) for line in file]

    for y in range(len(garden)):
        for x in range(len(garden[y])):
            if (x, y) not in visited:
                find_plot(garden, (x, y), garden[y][x], plot_id)
                count_sides(plots[plot_id])
                plot_id += 1

    print(sum(plot['size'] * plot['fence'] for plot in plots.values()))
    print(sum(plot['size'] * plot['sides'] for plot in plots.values()))