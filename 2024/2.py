#!/usr/bin/env python3

def check(diff):
  return all(x > 0 and x <= 3 for x in diff) or all(x < 0 and x >= -3 for x in diff)

def diff(levels):
  return [b - a for a, b in zip(levels, levels[1:])]

with open("2.input") as file:
  reports = [list(map(int, line.split())) for line in file]

  count = sum(1 for diff in [diff(levels) for levels in reports] if check(diff))
  print(count)

  permutations = [[report] + [report[:i] + report[i+1:] for i in range(len(report))] for report in reports]
  count = sum([1 for diffs in [[diff(levels) for levels in reports] for reports in permutations] if any(check(diff) for diff in diffs)])
  print(count)
