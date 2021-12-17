#!/usr/bin/env python3
with open("6.input") as file:
    data = [row.strip() for row in file.readlines()]

    groups = []
    group = set()
    for i, row in enumerate(data):
        if row:
            group.update([a for a in row])
        if not row or i == len(data) - 1:
            groups.append(group)
            group = set()
            continue

    print(sum(len(group) for group in groups))

    groups = []
    group = set()
    first = True
    for i, row in enumerate(data):
        if row:
            if first:
                group.update([a for a in row])
                first = False
            else:
                group = {x for x in group if x in row}
        if not row or i == len(data) - 1:
            if len(group) > 0:
                groups.append(group)
            group = set()
            first = True
            continue

    print(sum(len(group) for group in groups))
