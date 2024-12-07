#!/usr/bin/env python3

from operator import add, mul

def merge(a, b):
  return a * (10 ** len(str(b))) + b

operations = {
  '+': add,
  '*': mul,
  '||': merge
}

def calc(total, op, values, i, test, ops):
  if total > test:
    return False

  total = operations[op](total, values[i])

  if i == len(values) - 1:
    return total == test
  else:
    # any() was too slow...
    for op in ops:
      if calc(total, op, values, i + 1, test, ops):
        return True
    return False

cache = set()

def check(test, values, ops):
  if test in cache:
    return True

  for op in ops:
    if calc(values[0], op, values, 1, test, ops):
      cache.add(test)
      return True
  return False

with open("7.input") as file:
  data = {
    int(key.strip()): tuple(int(x) for x in value.strip().split())
    for key, value in (line.split(":", 1) for line in file)
  }

  print(sum(test for test, values in data.items() if check(test, values, ('+', '*'))))
  print(sum(test for test, values in data.items() if check(test, values, ('+', '*', '||'))))