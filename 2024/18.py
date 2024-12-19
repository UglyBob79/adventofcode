#!/usr/bin/env python3
from collections import deque

def dfs(dim, start, bytes, find_shortest=True):
    end = tuple(d - 1 for d in dim)

    queue = deque([(start, 0)])
    visited = {}
    shortest = None

    while queue:
        pos, dist = queue.popleft()

        if pos == end:
            if find_shortest:
              if shortest is None or dist < shortest:
                  shortest = dist
            else:
                return dist

        if find_shortest:
          if pos in visited and visited[pos] <= dist:
              continue
        elif pos in visited:
            continue

        visited[pos] = dist

        for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_pos = (pos[0] + delta[0], pos[1] + delta[1])

            if 0 <= new_pos[0] < dim[0] and 0 <= new_pos[1] < dim[1] and new_pos not in bytes:
                queue.append((new_pos, dist + 1))

    return shortest

with open("18.input") as file:
    bytes = [tuple(int(x) for x in line.strip().split(',')) for line in file]

    dim = (7, 7) if file.name.endswith('.example') else (71, 71)
    start = (0, 0)

    first_bytes = bytes[:12 if file.name.endswith('.example') else 1024]

    print(dfs(dim, start, first_bytes))

    min = 0
    max = len(bytes) - 1

    while min != max:
        mid = (min + max) // 2
        if dfs(dim, start, bytes[:mid], False) is None:
            max = mid
        else:
            min = mid + 1

    print(bytes[min - 1])
