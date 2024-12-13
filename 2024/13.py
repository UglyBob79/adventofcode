#!/usr/bin/env python3
import re
import numpy as np

button_re = re.compile(r"Button (.): X\+(\d+), Y\+(\d+)")
price_re = re.compile(r"Prize: X=(\d+), Y=(\d+)")

cost = [3, 1]

def solve(machine):
    a = np.array([[machine['buttons'][0][0], machine['buttons'][1][0]], [machine['buttons'][0][1], machine['buttons'][1][1]]])
    b = np.array([machine['price'][0], machine['price'][1]])
    x = np.round(np.linalg.solve(a, b))

    #if np.allclose(np.dot(a, x), b):
    if (x[0] * machine['buttons'][0][0] + x[1] * machine['buttons'][1][0] == machine['price'][0] and
        x[0] * machine['buttons'][0][1] + x[1] * machine['buttons'][1][1] == machine['price'][1]):
        return int(3 * x[0] + x[1])
    else:
        return 0


with open("13.input") as file:
    machines = []
    machine = None

    for line in file:
        match = button_re.match(line)
        if match:
            if match.group(1) == "A":
                machine = {'buttons': [(int(match.group(2)), int(match.group(3)))]}
            elif match.group(1) == "B":
                machine['buttons'].append((int(match.group(2)), int(match.group(3))))
        else:
            match = price_re.match(line)
            if match:
                machine['price'] = (int(match.group(1)), int(match.group(2)))
                machines.append(machine)

    print(sum([solve(machine) for machine in machines]))

    for machine in machines:
        machine['price'] = (machine['price'][0] + 10000000000000, machine['price'][1] + 10000000000000)

    print(sum([solve(machine) for machine in machines]))