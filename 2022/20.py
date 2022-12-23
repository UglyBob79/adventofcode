#!/usr/bin/env python3

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __str__(self):
        return "Node(data: %s)" % (str(self.data))

class CircularList():

    def __init__(self, array):
        self.start = None
        self.length = 0

        for v in array:
            self.append(Node(v))

    def append(self, n):
        self.length += 1

        if not self.start:
            self.start = n
            n.next = n
            n.prev = n
            return

        prev = self.start.prev
        next = self.start

        prev.next = n
        n.prev = prev
        next.prev = n
        n.next = next

    def remove(self, n):
        n.prev.next = n.next
        n.next.prev = n.prev
        self.length -= 1

    def insert_after(self, target, n):
        next = target.next

        target.next = n
        n.prev = target
        next.prev = n
        n.next = next

        self.length += 1

    def find_by_value(self, value, offset=0):
        node = self.start

        while node and node.data != value:
            node = node.next
            if node == self.start:
                return None

        if offset:
            while offset > 0:
                node = node.next
                offset -= 1

        return node if node else None

    def move(self, node):
        offset = node.data

        if offset != 0:
            self.remove(node)

            if offset < 0:
                offset = -(-offset % self.length)

                prev = node.prev

                while offset < 0:
                    prev = prev.prev
                    offset += 1
                next = prev.next
            else:
                offset = offset % self.length

                next = node.next

                while offset > 0:
                    next = next.next
                    offset -= 1
                prev = next.prev

            self.insert_after(prev, node)

        return self

    def to_list(self):
        l = []

        node = self.start

        while node:
            l.append(node.data)
            node = node.next
            if node == self.start:
                break

        return l

    def reflist(self):
        l = []

        node = self.start

        while node:
            l.append(node)
            node = node.next
            if node == self.start:
                break

        return l

with open('20.input') as file:
    data = [int(line) for line in file.read().splitlines()]
    values = CircularList(data)
    reflist = values.reflist()

    for ref in reflist:
        values.move(ref)

    print(sum([values.find_by_value(0, i).data for i in [1000, 2000, 3000]]))

    values2 = CircularList(data)
    reflist = values2.reflist()

    for ref in reflist:
        ref.data = ref.data * 811589153

    for _ in range(10):
        for ref in reflist:
            values2.move(ref)

    print(sum([values2.find_by_value(0, i).data for i in [1000, 2000, 3000]]))