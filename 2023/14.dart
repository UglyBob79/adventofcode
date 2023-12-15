#!/usr/bin/env dart

import 'dart:io';

bool roll(List<List<String>> map, String dir) {
  int xOffset = 0;
  int yOffset = 0;
  bool stable = true;

  switch (dir) {
    case 'N':
      yOffset = -1;
      break;

    case 'S':
      yOffset = 1;
      break;

    case 'W':
      xOffset = -1;
      break;

    case 'E':
      xOffset = 1;
      break;
  }

  for (int i = 1; i < map.length; i++) {
    for (int j = 0; j < map[i].length; j++) {
      int x = 0;
      int y = 0;

      if (dir == 'N' || dir == 'S') {
        x = j;
        y = dir == 'N' ? i : map.length - i - 1;
      } else {
        x = dir == 'W' ? i : map.length - i - 1;
        y = j;
      }

      if (map[y][x] == 'O' && map[y + yOffset][x + xOffset] == '.') {
        map[y + yOffset][x + xOffset] = 'O';
        map[y][x] = '.';
        stable = false;
      }
    }
  }

  return stable;
}

bool compare(List<List<String>> map1, List<List<String>> map2) {
  for (int y = 0; y < map1.length; y++) {
    for (int x = 0; x < map1[y].length; x++) {
      if (map1[y][x] != map2[y][x])
        return false;
    }
  }
  return true;
}

int weight(List<List<String>> map) {
  int sum = 0;

  for (int i = 0; i < map.length; i++) {
    sum += map[i].fold(0, (val, element) => val += (element == 'O') ? (map.length - i) : 0);
  }

  return sum;
}

void part1(List<List<String>> map) {
  while (!roll(map, 'N'));

  print(weight(map));
}

void part2(List<List<String>> map) {
  List<List<List<String>>> cycles = [];

  cycles.add(map.map((row) => List<String>.from(row)).toList());

  for (int i = 1; i < 1000000000; i++) {
    for (String dir in ['N', 'W', 'S', 'E']) {
      while (!roll(map, dir));
    }

    cycles.add(map.map((row) => List<String>.from(row)).toList());

    for (int j = cycles.length - 2; j >= 0; j--) {
      if (compare(cycles[cycles.length - 1], cycles[j])) {
        print(weight(cycles[j + (1000000000 - i) % (i - j)]));
        return;
      }
    }
  }
}

void printMap(List<List<String>> map) {
  for (var row in map) {
    print("${row.join('')}");
  }
  print("");
}

void main() {
  List<List<String>> data = new File("14.input")
      .readAsLinesSync().map((line) => line.split(''))
      .toList();

  part1(data.map((row) => List<String>.from(row)).toList());
  part2(data);
}