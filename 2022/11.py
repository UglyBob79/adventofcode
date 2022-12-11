#!/usr/bin/env python3
import operator
import math
import copy
import re

MONKEY_RE = re.compile('^Monkey (?P<id>\d):\n.*: (?P<items>[^\n]+)\n.*old (?P<op>.) (?P<factor>[^\n]+)\n.*by (?P<div>\d+)\n.*monkey (?P<true>\d+)\n.*monkey (?P<false>\d+)')

def parse_monkey(blob):
    m = re.match(MONKEY_RE, blob)
    if m:
        return {
            'id': int(m.group('id')),
            'inspected': 0,
            'items': [int(i) for i in m.group('items').split(', ')],
            'op': ((operator.pow if m.group('factor') == 'old' else operator.mul) if m.group('op') == '*' else operator.add, 2 if m.group('factor') == 'old' else int(m.group('factor'))),
            'test': {'factor': int(m.group('div')), True: int(m.group('true')), False: int(m.group('false'))}
        }

def simulate(monkeys, rounds, divide=True):
    prod = math.prod([monkey['test']['factor'] for monkey in monkeys])

    for _ in range(rounds):
        for monkey in monkeys:
            while len(monkey['items']) > 0:
                item = monkey['items'].pop(0)
                monkey['inspected'] += 1
                item = (monkey['op'][0](item, monkey['op'][1]))
                item = item // 3 if divide else item % prod
                monkeys[monkey['test'][item % monkey['test']['factor'] == 0]]['items'].append(item)

    return math.prod(sorted([monkey['inspected'] for monkey in monkeys])[-2:])

with open("11.input") as file:
    monkeys = []

    for blob in file.read().split('\n\n'):
        monkeys.append(parse_monkey(blob))

    print(simulate(copy.deepcopy(monkeys), 20))
    print(simulate(copy.deepcopy(monkeys), 10000, False))