#!/usr/bin/env python3
from copy import deepcopy

def parseGraph(lines):
    graph = { 'doubleVisit' : False, 'nodes' : {} }

    for line in lines:
        nodes = line.split('-')

        for node in nodes:
            if node not in graph['nodes']:
                graph['nodes'][node] = { 'name' : node, 'small' : node.islower(), 'paths' : [x for x in nodes if x != node] }
            else:
                graph['nodes'][node]['paths'].append([x for x in nodes if x != node][0])

    return graph

def travel(graph, to, visited):
    global pathCount

    if to == 'end':
        pathCount += 1
        return

    if graph['nodes'][to]['small'] and visited[to] > 0:
        if graph['doubleVisit'] and not visited['double'] and to != 'start':
            visited['double'] = to
        else:
            return

    visited[to] += 1

    for path in graph['nodes'][to]['paths']:
        if path != 'start':
            travel(graph, path, deepcopy(visited))

def countPaths(graph):
    global pathCount
    pathCount = 0

    visited = { node : 0 for node in graph['nodes'] }
    visited['double'] = None

    travel(graph, 'start', deepcopy(visited))

    return pathCount

with open("12.input") as file:
    graph = parseGraph(file.read().splitlines())
    print(countPaths(graph))

    graph['doubleVisit'] = True
    print(countPaths(graph))
