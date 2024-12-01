#!/usr/bin/env python3

with open("1.input") as file:
  list1, list2 = zip(*(map(int, line.split()) for line in file))

  print(sum(abs(b - a) for a, b in zip(sorted(list1), sorted(list2))))
  print(sum([x * list2.count(x) for x in list1]))
