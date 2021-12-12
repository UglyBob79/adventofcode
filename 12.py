#!/usr/bin/env python3
from copy import deepcopy

def parseGraph(lines):
    graph = { 'doubleVisit' : False, 'doubleNode' : None, 'nodes' : {} }

    for line in lines:
        nodes = line.split('-')

        for node in nodes:
            if node not in graph['nodes']:
                graph['nodes'][node] = { 'name' : node, 'small' : node.islower(), 'paths' : [x for x in nodes if x != node], 'visited' : False }
            else:
                graph['nodes'][node]['paths'].append([x for x in nodes if x != node][0])

    return graph

def travel(graph, to):
    global pathCount

    if graph['nodes'][to]['small'] and graph['nodes'][to]['visited']:
        if graph['doubleVisit'] and graph['doubleNode'] is None and to not in ['start', 'end']:
            graph['doubleNode'] = to
        else:
            return

    graph['nodes'][to]['visited'] = True

    if to == 'end':
        pathCount += 1
        return

    for path in graph['nodes'][to]['paths']:
        travel(deepcopy(graph), path)

def countPaths(graph):
    global pathCount
    pathCount = 0

    start = graph['nodes']['start']
    start['visited'] = True

    for path in start['paths']:
        travel(deepcopy(graph), path)

    return pathCount

with open("12.input") as file:
    graph = parseGraph(file.read().splitlines())
    print(countPaths(graph))

    graph['doubleVisit'] = True
    print(countPaths(graph))
