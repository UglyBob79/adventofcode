#!/usr/bin/env python3
import numpy as np

with open("2.input") as file:
    data = [row.split(' ') for row in file.read().splitlines()]
    v_dir = {'forward' : 0, 'up' : -1, 'down' : 1}

    x = sum([int(b) for (a,b) in filter(lambda v: v[0] == "forward", data)])
    vert = [v_dir[a]*int(b) for (a,b) in data]
    y = sum(vert)

    print(x*y)

    aim = np.cumsum(vert)
    y = sum([int(a[1])*b for (a,b) in filter(lambda d: d[0][0] == "forward", zip(data, aim))])

    print(x*y)
