#!/usr/bin/env dart

import 'dart:io';

Map<String, int> cache = {};

int cachedFindArrangements(String line, List<int> groups) {
  String key = line + groups.join(',');

  if (!cache.containsKey(key))
    cache[key] = findArrangements(line, groups);

  return cache[key]!;
}

int findArrangements(String line, List<int> groups) {
  if (line.length == 0) {
    return groups.isEmpty ? 1 : 0;
  }

  if (line[0] == '.') {
    return cachedFindArrangements(line.substring(1), groups);
  } else if (line[0] == '?' ) {
    String subLine = line.substring(1);
    return cachedFindArrangements('#' + subLine, groups) + findArrangements('.' + subLine, groups);
  } else if (!groups.isEmpty && groups[0] <= line.length) {
    bool possible = true;
    for (int i = 0; i < groups[0]; i++) {
      if (line[i] == '.') {
        possible = false;
      }
    }

    int offset = groups[0];

    if (possible) {
      if (groups[0] < line.length) {
        if (line[groups[0]] == '#') {
          possible = false;
        } else {
          offset++;
        }
      }
    }

    if (possible) {
      return cachedFindArrangements(line.substring(offset), groups.sublist(1));
    }
  }

  return 0;
}

void part1(List<Map<String, Object>> data) {
  print(data.map((input) => cachedFindArrangements(input['pattern']! as String, input['groups']! as List<int>)).reduce((value, element) => value + element));
}

void part2(List<Map<String, Object>> data) {
  int sum = 0;

  for (var row in data.sublist(0, data.length)) {
    var line = List.filled(5, row['pattern']).join('?');
    var groups = List.generate(5, (_) => row['groups'] as List<int>).expand((element) => element).toList();

    int v = cachedFindArrangements(line, groups);
    sum += v;
  }

  print(sum);
}

void main() {
  List<Map<String, Object>> data = File("12.input").readAsLinesSync().map((line) {
    var parts = line.split(' ');
    return {
      'pattern': parts[0],
      'groups': parts[1].split(',').map((str) => int.parse(str)).toList(),
    };
  }).toList();


  part1(data);
  part2(data);
}