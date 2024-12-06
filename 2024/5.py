#!/usr/bin/env python3

def count_updates(rules, updates):
  total = 0
  incorrect = []

  for update in updates:
    ok = True
    for value in update:
      for rule in rules:
        if value == rule[0] and (rule[1] in update and update.index(rule[1]) < update.index(rule[0])):
          ok = False
          break
      if not ok:
        incorrect.append(update)
        break
    if ok:
      total += update[len(update) // 2]

  return (total, incorrect)

def fix_updates(rules, updates):
  for update in updates:
    done = False
    while not done:
      done = True
      for rule in rules:
        if rule[0] in update and rule[1] in update:
            idx_0 = update.index(rule[0])
            idx_1 = update.index(rule[1])
            if idx_1 < idx_0:
                update.insert(idx_1, update.pop(idx_0))
                done = False

  return updates

with open("5.input") as file:
  data = [line.strip() for line in file if line.strip()]

  rules = [[int(value) for value in line.split("|")] for line in data if "|" in line]
  updates = [[int(value) for value in line.split(",")] for line in data if not "|" in line]

  total, incorrect = count_updates(rules, updates)
  print(total)

  updates = fix_updates(rules, incorrect)
  print(count_updates(rules, updates)[0])