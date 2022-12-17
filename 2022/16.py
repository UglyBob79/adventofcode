#!/usr/bin/env python3

import re
import networkx as nx
from itertools import combinations

VALVE_RE = re.compile('^Valve (?P<from>[A-Z]{2}) has flow rate=(?P<rate>[^;]+); tunnel[s]? lead[s]? to valve[s]? (?P<to>.*)')

def parse_data(line):
    m = re.match(VALVE_RE, line)
    if m:
        return {
            'valve': m.group('from'),
            'rate': int(m.group('rate')),
            'to': m.group('to').split(', ')
        }

def gen_graph(data):
    g = nx.DiGraph()

    for valve in data:
        g.add_node(valve, rate = data[valve]['rate'])

    for valve in data:
        for dest in data[valve]['to']:
            g.add_edge(valve, dest, cost=1) # cost is 1 min

    return g

def traverse(g, node, valves_closed, pressure, time, delta_time):
    time -= delta_time

    if node in valves_closed:
        valves_closed.remove(node)
        delta_pressure = g.nodes[node]['rate'] * time
        pressure += delta_pressure
        time -= 1

    if len(valves_closed) > 0:
        candidates = []
        for v in valves_closed:
            dist = nx.shortest_path_length(g, node, v)
            if time - dist > 0:
                candidates.append((v, dist))

        if len(candidates) > 0:
            return max([traverse(g, v, valves_closed.copy(), pressure, time, dist) for v, dist in candidates])
        else:
            return pressure
    else:
        return pressure

def print_graph(g):
    print('Graph {')
    for node in g.nodes(data=True):
        print(node, list(g.neighbors(node[0])))
    print('}')

with open('16.input') as file:
    data = dict([(row['valve'], row) for row in [parse_data(line) for line in file.read().splitlines()]])

    g = gen_graph(data)

    valves = [node[0] for node in g.nodes(data=True) if node[1]['rate'] > 0]
    print(traverse(g, 'AA', valves.copy(), 0, 30, 1))

    pressure = 0

    for valves1 in combinations(valves, len(valves) // 2):
        valves2 = [v for v in valves if v not in valves1]
        pressure = max(pressure, traverse(g, 'AA', list(valves1), 0, 26, 1) + traverse(g, 'AA', valves2, 0, 26, 1))

    print(pressure)