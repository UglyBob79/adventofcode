#!/usr/bin/env python3
from collections import defaultdict

def should_merge(set1, set2, adj_map):
    for n1 in set1:
        for n2 in set2:
            if n2 not in adj_map[n1] or n1 not in adj_map[n2]:
                return False
    return True

def merge_sets(sets, adj_map):
    sets = list(sets)
    merged = True

    while merged:
        merged = False
        i = 0
        while i < len(sets):
            j = i + 1
            while j < len(sets):
                if should_merge(sets[i], sets[j], adj_map):
                    sets[i] = sets[i].union(sets[j])
                    del sets[j]
                    merged = True
                else:
                    # Only increment if no merge occurred
                    j += 1
            i += 1
    return sets

def map_connections(pairs):
    connections = defaultdict(set)

    for pair in pairs:
        connections[pair[0]].update(pair)
        connections[pair[1]].update(pair)

    return connections

def filter(sets, start_char):
    return [s for s in sets if any(str(item).startswith(start_char) for item in s)]

def part1(conns):
    nodes = list(conns.keys())

    count = 0
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            for k in range(j + 1, len(nodes)):
                if (
                    nodes[j] in conns[nodes[i]]
                    and nodes[k] in conns[nodes[j]]
                    and nodes[i] in conns[nodes[k]]
                    and any(str(item).startswith('t') for item in [nodes[i], nodes[j], nodes[k]])
                ):
                    count += 1
    return count

def part2(conns, pairs):
    networks = merge_sets([set(l) for l in pairs], conns)
    return ','.join(sorted(max(networks, key=len)))

with open("23.input") as file:
    pairs = [line.strip().split('-') for line in file]

    conns = map_connections(pairs)

    print(part1(conns))
    print(part2(conns, pairs))