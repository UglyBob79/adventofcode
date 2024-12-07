#!/usr/bin/env python3
from collections import defaultdict

def count_updates(rules, updates):
  total = 0
  incorrect = []

  for update in updates:
    #print("test " + str(update))
    for i, value in enumerate(update):
      ok = True
      if value in rules and i > min([1000] + [update.index(x) for x in rules[value] if x in update]):
        ok = False
        break
    if not ok:
      incorrect.append(update)
    else:
      total += update[len(update) // 2]

  return (total, incorrect)

def fix_updates(rules, updates):
  results = []
  for update in updates:
    #print(update)
    result = []
    for value in update:
      if value in rules:
        pos = min([1000] + [result.index(x) for x in rules[value] if x in result])
        #print("result: " + str(result) + " place " + str(value) + " at pos " + str(pos))
        result.insert(pos, value)
      else:
        result.append(value)
    #print(result)
    results.append(result)
  return results

with open("5.input") as file:
  data = [line.strip() for line in file if line.strip()]

  rules = defaultdict(set, {
      rule[0]: rule[1] for rule in [[int(value) for value in line.split("|")] for line in data if "|" in line]
  })
  rules = [[int(value) for value in line.split("|")] for line in data if "|" in line]
  updates = [[int(value) for value in line.split(",")] for line in data if not "|" in line]

  opt_rules = defaultdict(set)

  for rule in rules:
    opt_rules[rule[0]].add(rule[1])

  total, incorrect = count_updates(opt_rules, updates)
  print(total)

  updates = fix_updates(opt_rules, incorrect)
  print(count_updates(rules, updates)[0])