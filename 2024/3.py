#!/usr/bin/env python3
import re

with open("3.input") as file:
  data = file.read()

  regex = re.compile(r"(?P<oper>(mul|do|don't))\(((?P<val1>\d+),(?P<val2>\d+))?\)")
  operations = [match.groupdict() for match in regex.finditer(data)]

  print(sum([int(oper["val1"]) * int(oper["val2"]) for oper in operations if oper["oper"] == "mul"]))

  do = True
  result = 0

  for oper in operations:
    if oper["oper"] == "do":
      do = True
    elif oper["oper"] == "don't":
      do = False
    elif do:
      result += int(oper["val1"]) * int(oper["val2"])

  print(result)
