#!/usr/bin/env dart

import 'dart:io';
import 'dart:math';

void part1(Map<String, List<Map<String, dynamic>>> flows, List<Map<String, int>> parts) {
  List<Map<String, int>> accepted = [];

  for (var part in parts) {
    String dest = 'in';

    while (true) {
      if (dest == 'A') {
        accepted.add(part);
        break;
      } else if (dest == 'R') {
        break;
      }

      var rules = flows[dest]!;

      for (var rule in rules) {
        if (rule['var'] != null) {
          int val1 = part[rule['var']]!;
          int val2 = rule['val'];
          String op = rule['op'];

          if (op == '<' && val1 < val2 || op == '>' && val1 > val2) {
            dest = rule['dest'];
            break;
          }
        } else {
          dest = rule['dest'];
          break;
        }
      }
    }
  }

  int sum = 0;

  accepted.forEach((map) {
    map.values.forEach((value) {
      sum += value;
    });
  });

  print(sum);
}

Map<String, List<int>> cloneRanges(Map<String, List<int>> ranges) {
  Map<String, List<int>> newRanges = {};

  ranges.forEach((key, value) {
    newRanges[key] = [...value];
  });

  return newRanges;
}

int sum = 0;

void traverse(String dest, Map<String, List<int>> ranges, Map<String, List<Map<String, dynamic>>> flows) {
  if (dest == 'A') {
    int subSum = 1;

    for (var key in ranges.keys) {
      subSum *= (ranges[key]![1] - ranges[key]![0] + 1);
    }

    sum += subSum;
    return;
  } else if (dest == 'R') {
    return;
  }

  var rules = flows[dest]!;

  for (var rule in rules) {
    if (rule['var'] != null) {
      var rangesCopy = cloneRanges(ranges);

      String op1 = rule['var'];
      int op2 = rule['val'];
      String op = rule['op'];

      if (op == '<') {
        rangesCopy[op1]![1] = min(rangesCopy[op1]![1], op2 - 1);
        ranges[op1]![0] = max(ranges[op1]![0], op2);
        traverse(rule['dest'], rangesCopy, flows);
      } else { // '>'
        rangesCopy[op1]![0] = max(rangesCopy[op1]![0], op2 + 1);
        ranges[op1]![1] = min(ranges[op1]![1], op2);
        traverse(rule['dest'], rangesCopy, flows);
      }
    } else {
      traverse(rule['dest'], ranges, flows);
    }
  }
}

void part2(Map<String, List<Map<String, dynamic>>> flows) {
  Map<String, List<int>> ranges = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]};

  traverse('in', ranges, flows);

  print(sum);
}

void main() {
  List<String> data = new File("19.input")
      .readAsLinesSync()
      .toList();

  bool flow = true;
  Map<String, List<Map<String, dynamic>>> flows = {};
  List<Map<String, int>> parts = [];

  for (String row in data) {
    if (row.isEmpty) {
      flow = false;
      continue;
    }

    if (flow) {
      var match = RegExp(r'(\w+)\{([^}]+)\}').firstMatch(row);

      if (match != null) {
        String name = match.group(1)!;
        List<String> rules = match.group(2)!.split(',');

        List<Map<String, dynamic>> ruleList = [];

        for (String rule in rules) {
          match = RegExp(r'((\w)([<>])(\d+)\:)?(\w+)').firstMatch(rule);

          if (match != null) {
            Map<String, dynamic> ruleMap = {
              'var': match.group(2),
              'op': match.group(3),
              'val': match.group(4) != null ? int.parse(match.group(4)!) : 0,
              'dest': match.group(5)
            };

            ruleList.add(ruleMap);
          }

          flows[name] = ruleList;
        }
      }
    } else {
      Map<String, int> part = Map.fromIterable(
        row.substring(1, row.length - 1).split(',').map((v) => v.split('=')),
        key: (e) => e[0],
        value: (e) => int.parse(e[1])
      );

      parts.add(part);
    }
  }

  part1(flows, parts);
  part2(flows);
}