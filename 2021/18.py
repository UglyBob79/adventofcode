#!/usr/bin/env python3
import re

explodeRe = re.compile('\[(?P<v1>[0-9]+)\,(?P<v2>[0-9]+)\]')
splitRe = re.compile('(?P<v>[0-9]{2})')

class Expression:
    data = None
    depth = []
    debug = False

    def __init__(self, data):
        self.data = data
        self.updateDepth()

    def __str__(self):
        return "Expression{\n  data: %s\n}" % (self.data)

    def debugEnable(self, on):
        self.debug = on

    def printIndex(self, data, a, b):
        iStr = ''.join([str(i % 10) for i in range(len(data))])
        if a and b:
            iStr = list(iStr)
            iStr[a] = '['
            iStr[b] = ']'
            iStr = ''.join(iStr)
        print(iStr)
        print(data)

    def add(self, value):
        self.data = "[%s,%s]" % (self.data, value)
        self.updateDepth()
        self.reduce()

    def set(self, data):
        self.data = data
        self.updateDepth()

    def updateDepth(self):
        depth = 0
        self.depth = []

        for c in self.data:
            if c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
            self.depth.append(depth)

    def reduce(self):
        stable = False
        while not stable:
            stable = True
            while self.explode():
                continue
            if self.split():
                stable = False

    def explode(self):
        potentials = [(m.start(0), m.end(0), int(m.group('v1')), int(m.group('v2'))) for m in re.finditer(explodeRe, self.data)]
        self.updateDepth()

        for p in potentials:
            if self.depth[p[0]] > 4:
                if self.debug:
                    print("[explode]")
                    self.printIndex(self.data, p[0], p[1])
                self.set(self.explodeDir(p[2], self.data[:p[0]], -1) + '0' + self.explodeDir(p[3], self.data[p[1]:], 1))
                return True
        return False

    def split(self):
        m = re.search(splitRe, self.data)
        if m:
            v = int(m.group('v'))
            v1 = v // 2
            v2 = v - v1
            if self.debug:
                print("[split]")
                self.printIndex(self.data, m.start() - 1, m.end())
            self.set(self.data[:m.start()] + '[%d,%d]' % (v1, v2) + self.data[m.end():])
            return True
        return False

    def findNumber(self, data, dir):
        pos = 0 if dir == 1 else len(data) - 1
        vs = -1
        for i in range(pos, 0 if dir == -1 else len(data), dir):
            if data[i].isdigit():
                if vs == -1:
                    vs = i
            else:
                if vs != -1:
                    es = i - dir
                    s = vs if dir == 1 else es
                    e = es if dir == 1 else vs
                    return (int(data[s:e + 1]), s, e + 1)

        return None

    def explodeDir(self, value, data, dir):
        find = self.findNumber(data, dir)
        if find:
            n = find[0] + value
            return data[:find[1]] + str(n) + data[find[2]:]
        else:
            return data

    def magnitude(self):
        d = self.data
        return eval(d.translate(d.maketrans({'[': '(3*', ',': '+2*', ']': ')'})))

with open("18.input") as file:
    data = [row.strip() for row in file.readlines()]
    expr = Expression(data[0])
    #expr.debugEnable(True)

    for row in data[1:]:
        expr.add(row)

    print(expr.magnitude())

    maxMag = 0
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            expr.set(data[i])
            expr.add(data[j])
            mag = expr.magnitude()
            maxMag = max(maxMag, mag)
    print(maxMag)
