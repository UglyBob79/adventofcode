#!/usr/bin/env python3
import operator
import copy

OPERATORS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def parse_row(row):
    parts = row.split(' ')

    if len(parts) == 2:
        return (parts[0][:-1], int(parts[1]))
    else:
        return (parts[0][:-1], [parts[1], OPERATORS[parts[2]], parts[3]])

def calculate(data, target):
    constants = {}

    while not type(data[target]) == int:
        change = False
        for key in reversed(data):
            if type(data[key]) == int:
                if key not in constants:
                    change = True
                    constants[key] = data[key]
            else:
                if not type(data[key][0]) == int and data[key][0] in constants:
                    data[key][0] = constants[data[key][0]]
                    change = True
                if not type(data[key][2]) == int and data[key][2] in constants:
                    data[key][2] = constants[data[key][2]]
                    change = True
                if type(data[key][0]) == int and type(data[key][2]) == int:
                    data[key] = int(data[key][1](data[key][0], data[key][2]))
                    constants[key] = data[key]
        if not change:
            return None

    return data[target]

def reverse_calc(data, target, other, value):
    rev_data = dict()

    for key in data:
        if type(data[key]) != int:
            if type(data[key][0]) == int:
                if data[key][1] == operator.add:
                    rev_data[data[key][2]] = [key, operator.sub, data[key][0]]
                elif data[key][1] == operator.sub:
                    rev_data[data[key][2]] = [data[key][0], operator.sub, key]
                elif data[key][1] == operator.mul:
                    rev_data[data[key][2]] = [key, operator.truediv, data[key][0]]
                elif data[key][1] == operator.truediv:
                     rev_data[data[key][2]] = [data[key][0], operator.truediv, key]
            else:
                if data[key][1] == operator.add:
                    rev_data[data[key][0]] = [key, operator.sub, data[key][2]]
                elif data[key][1] == operator.sub:
                    rev_data[data[key][0]] = [key, operator.add, data[key][2]]
                elif data[key][1] == operator.mul:
                    rev_data[data[key][0]] = [key, operator.truediv, data[key][2]]
                elif data[key][1] == operator.truediv:
                     rev_data[data[key][0]] = [data[key][2], operator.mul, key]
        else:
            rev_data[key] = data[key]

    rev_data[other] = value
    return calculate(rev_data, target)

with open('21.input') as file:
    data = dict([parse_row(line) for line in file.read().splitlines()])

    print(calculate(copy.deepcopy(data), 'root'))

    del data['humn']

    value1 = calculate(copy.deepcopy(data), data['root'][0])
    value2 = calculate(copy.deepcopy(data), data['root'][2])

    value = value1 if value1 else value2
    this = data['root'][0] if value2 else data['root'][2]

    calculate(data, this)

    print(reverse_calc(data, 'humn', this, value))
