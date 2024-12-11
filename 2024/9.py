#!/usr/bin/env python3
import time

def remove(fs, i):
  item = fs[i]
  fs[i] = ('.', item[1])

  return item

def replace(fs, i, item):
  old_len = fs[i][1]
  fs[i] = item

  if old_len > item[1]:
    fs.insert(i + 1, ('.', old_len - item[1]))
    return True
  return False

with open("9.input") as file:
    data = [int(x) for x in file.readline()]

    blocks = []
    fs = []
    empty = []
    files = []

    k = 0
    for i, x in enumerate(data):
        for j in range(x):
            blocks.append(i // 2 if i % 2 == 0 else '.')
        if x != 0:
            fs.append((i // 2 if i % 2 == 0 else '.', x))
            if i % 2 == 0:
              files.append({'pos': k, 'id': i // 2, 'size': x})
            else:
              empty.append({'pos': k, 'id': -1, 'size': x})
            k += x

    # Part 1
    i = 0
    j = len(blocks) - 1

    while i != j:
      if blocks[i] != '.':
          i += 1
          continue
      if blocks[j] == '.':
          j -= 1
          continue

      blocks[i] = blocks[j]
      blocks[j] = '.'

    print(sum([i * b for i, b in enumerate(blocks) if b != '.']))

    # Part 2
    i = len(fs) - 1
    first_empty = 0
    while i > 0:
      if fs[i][0] == '.':
          i -= 1
          continue

      j = first_empty
      first = True

      while j < i:
        if fs[j][0] == '.':
          if fs[j][1] >= fs[i][1]:
            item = remove(fs, i)
            if replace(fs, j, item):
              i += 1
            break
          elif first:
            first_empty = j
            first = False

        j += 1
      i -= 1

    i = 0
    checksum = 0
    blocks = []
    for entry in fs:
      if entry[0] == '.':
        i += entry[1]
      else:
        for j in range(entry[1]):
          checksum += i * entry[0]
          i += 1

    print(checksum)