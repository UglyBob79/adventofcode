#!/usr/bin/env python3
import sys

# y|      /z 3
# 2|    /
#  |  /
#  |/_______
#          x 1
#

rot = [
    # top up
    None, # ( 1,  2,  3), #normal
    ( 2, -1,  3), # rot 90 around z
    (-1, -2,  3), # rot 180 around z
    (-2,  1,  3), # rot 270 around z
    # bottom up
    ( 1, -2, -3), # rot 180 around x
    (-2, -1, -3), # rot 180 around x, rotate 90 around z
    (-1,  2, -3), # rot 180 around x, rotate 180 around z
    ( 2,  1, -3), # rot 180 around x, rotate 270 around z
    # front up
    (-3,  2,  1), # rot 90 around y,
    ( 2,  3,  1), # rot 90 around y, rotate 90 around z
    ( 3, -2,  1), # rot 90 around y, rotate 180 around z
    (-2, -3,  1), # rot 90 around y, rotate 270 around z
    # back up
    ( 3,  2, -1), # rot 270 around y
    ( 2, -3, -1), # rot 270 around y, rotate 90 around z
    (-3, -2, -1), # rot 270 around y, rotate 180 around z
    (-2,  3, -1), # rot 270 around y, rotate 270 around z
    # right up
    ( 1,  3, -2), # rot 90 around x
    ( 3, -1, -2), # rot 90 around x, rotate 90 around z
    (-1, -3, -2), # rot 90 around x, rotate 180 around z
    (-3,  1, -2), # rot 90 around x, rotate 270 around z
    # left up
    ( 1, -3,  2), # rot 270 around x
    (-3, -1,  2), # rot 270 around x, rotate 90 around z
    (-1,  3,  2), # rot 270 around x, rotate 180 around z
    ( 3,  1,  2), # rot 270 around x, rotate 270 around z
]

def rotate(a, r):
    (xr, yr, zr) = tuple((-1 if v < 0 else 1, abs(v) - 1) for v in r)
    return [(xr[0] * v[xr[1]], yr[0] * v[yr[1]], zr[0] * v[zr[1]]) for v in a]

def checkMatch(a1, a2):
    count = 0
    for e1 in a1:
        for e2 in a2:
            if e1 == e2:
                count += 1
                if count >= 12:
                    return True
    return False

def translate(a, d):
    return [(p[0] + d[0], p[1] + d[1], p[2] + d[2]) for p in a]

def findMatch(a1, a2):
    for e1 in a1:
        for e2 in a2:
            delta = (e1[0] - e2[0], e1[1] - e2[1], e1[2] - e2[2])
            at = translate(a2, delta)
            if checkMatch(a1, at):
                return (at, delta)
    return None

def matchScanners(s1, s2):
    # Only check if enough points have the same internal distances
    if len([dist for dist in s1['dists'] if dist in s2['dists']]) < 12:
        return

    a1 = s1['solution'][0]
    for a2 in s2['points']:
        m = findMatch(a1, a2)
        if m:
            print("Match: %d,%d" % (s1['id'], s2['id']))
            s2['solution'] = m
            s2['done'] = True
            break
        s2['checked'].add(s1['id'])

def calcRotations(s):
    for r in rot:
        if r:
            s['points'].append(rotate(s['points'][0], r))

def calcDistances(s):
    p = s['points'][0]
    for i in range(len(p)):
        for j in range(i + 1, len(p)):
            s['dists'].append((p[i][0] - p[j][0]) ** 2 + (p[i][1] - p[j][1]) ** 2 + (p[i][2] - p[j][2]) ** 2)

with open("19.input") as file:
    data = [row.strip() for row in file.readlines()]

    scanners = []
    scanner = None
    points = []
    for line in data:
        if line.startswith('---'):
            scanner = {'id': int(line.split(' ')[2]), 'done': False, 'solution': None, 'checked': set(), 'dists': [], 'points': []}
            scanner['points'].append([]) # unrotated data first
        elif not line:
            scanners.append(scanner)
        else:
            scanner['points'][0].append(tuple(map(int, line.split(','))))
    scanners.append(scanner)

    for s in scanners:
        calcRotations(s)
        calcDistances(s)

    # pick first scanner as reference and mark it done
    scanners[0]['solution'] = (scanners[0]['points'][0], (0, 0, 0))
    scanners[0]['done'] = True

    while sum([s['done'] for s in scanners]) < len(scanners):
        for s1 in filter(lambda s: s['done'] == True, scanners):
            for s2 in filter(lambda s: s['done'] == False, scanners):
                if not s1['id'] in s2['checked']:
                    matchScanners(s1, s2)

    scanPoints = set()
    for s in scanners:
        for p in s['solution'][0]:
            scanPoints.add(p)
    print(len(scanPoints))

    maxDist = 0
    for i in range(len(scanners)):
        for j in range(i + 1, len(scanners)):
            t1 = scanners[i]['solution'][1]
            t2 = scanners[j]['solution'][1]
            dist = abs(t1[0] - t2[0]) + abs(t1[1] - t2[1]) + abs(t1[2] - t2[2])
            maxDist = max(maxDist, dist)
    print(maxDist)
