#!/usr/bin/env python3
import operator
import math
import copy

def simulate(monkeys, rounds, divide=True):
    prod = math.prod([monkeys[id]['test']['factor'] for id in monkeys])

    for _round in range(rounds):
        for monkey in monkeys.values():
            while len(monkey['items']) > 0:
                item = monkey['items'].pop(0)
                monkey['inspected'] += 1
                item = (monkey['op'][0](item, monkey['op'][1]))
                item = item // 3 if divide else item % prod
                monkeys[monkey['test'][item % monkey['test']['factor'] == 0]]['items'].append(item)

    return math.prod(sorted([monkeys[id]['inspected'] for id in monkeys])[-2:])

with open("11.input") as file:
    monkeys = {}
    monkey = None

    for line in [l.strip() for l in file.read().splitlines()]:
        if line.startswith('Monkey'):
            monkey = {'id': int(line.split(' ')[1][0]), 'inspected': 0}
        elif line.startswith('Starting items:'):
            monkey['items'] = [int(i) for i in line[16:].split(', ')]
        elif line.startswith('Operation:'):
            parts = line.split(' ')
            if parts[4] == '*':
                monkey['op'] = (operator.pow, 2) if parts[5] == 'old' else (operator.mul, int(parts[5]))
            elif parts[4] == '+':
                monkey['op'] = (operator.add, int(parts[5]))
        elif line.startswith('Test:'):
            monkey['test'] = {'factor': int(line.split(' ')[3])}
        elif line.startswith('If true:'):
            monkey['test'][True] = int(line.split(' ')[5])
        elif line.startswith('If false:'):
            monkey['test'][False] = int(line.split(' ')[5])
            monkeys[monkey['id']] = monkey

    print(simulate(copy.deepcopy(monkeys), 20))
    print(simulate(copy.deepcopy(monkeys), 10000, False))