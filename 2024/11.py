#!/usr/bin/env python3
from functools import lru_cache

@lru_cache(maxsize=None)
def countFrom(stone, iter):
    if iter == 0:
       return 1

    if stone == 0:
      return countFrom(1, iter - 1)
    elif len(str(stone)) % 2 == 0:
      return countFrom(int(str(stone)[:len(str(stone))//2]), iter - 1) + countFrom(int(str(stone)[len(str(stone))//2:]), iter - 1)
    else:
      return countFrom(stone * 2024, iter - 1)

with open("11.input") as file:
    stones = [int(x) for x in file.readline().strip().split()]

    print(sum(countFrom(stone, 25) for stone in stones))
    print(sum(countFrom(stone, 75) for stone in stones))