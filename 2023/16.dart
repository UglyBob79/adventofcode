#!/usr/bin/env dart

import 'dart:io';

enum Dir { north, south, east, west, none }

Map<Dir, List<int>> dMove = {
  Dir.north: [0, -1],
  Dir.south: [0, 1],
  Dir.west: [-1 , 0],
  Dir.east: [1, 0]
};

Map<String, Map<Dir, List<Dir>>> mirrors = {
  '|': {
    Dir.north: [Dir.north],
    Dir.south: [Dir.south],
    Dir.east: [Dir.north, Dir.south],
    Dir.west: [Dir.north, Dir.south]
  },
  '-': {
    Dir.north: [Dir.west, Dir.east],
    Dir.south: [Dir.west, Dir.east],
    Dir.east: [Dir.east],
    Dir.west: [Dir.west]
  },
  '\\': {
    Dir.north: [Dir.west],
    Dir.south: [Dir.east],
    Dir.east: [Dir.south],
    Dir.west: [Dir.north],
  },
  '/': {
    Dir.north: [Dir.east],
    Dir.south: [Dir.west],
    Dir.east: [Dir.north],
    Dir.west: [Dir.south]
  }
};

void beam(List<int> pos, Dir dir, List<List<String>> map, List<List<List<Dir>>> visited) {
  while (true) {
    if (pos[1] < 0 || pos[1] >= map.length || pos[0] < 0 || pos[0] >= map[0].length) {
      return;
    }

    if (visited[pos[1]][pos[0]].contains(dir)) {
      return;
    } else {
      visited[pos[1]][pos[0]].add(dir);
    }

    if (mirrors.containsKey(map[pos[1]][pos[0]])) {
      List<Dir> dirs = mirrors[map[pos[1]][pos[0]]]![dir]!;

      if (dirs.length == 1 && dirs[0] == dir) {
        pos[0] += dMove[dir]![0];
        pos[1] += dMove[dir]![1];
      } else {
        for (var d in dirs) {
          beam([pos[0] + dMove[d]![0], pos[1] + dMove[d]![1]], d, map, visited);
        }
        return;
      }
    } else {
      pos[0] += dMove[dir]![0];
      pos[1] += dMove[dir]![1];
    }
  }
}

void printMap(List<List<String>> map) {
  for (var row in map) {
    print(row.join(''));
  }
  print("");
}

void printVisited(List<List<List<Dir>>> visited) {
  for (var row in visited) {
    print(row.map((e) => e.isEmpty ? '.' : '#').join(''));
  }
  print("");
}

int simulate(List<int> pos, Dir dir, map) {
  List<List<List<Dir>>> visited = List.generate(map.length, (row) {
    return List.generate(map[0].length, (col) => []);
  });

  beam(pos, dir, map, visited);

  return visited
      .map((row) => row.fold(
          0, (previousValue, e) => previousValue + (e.isEmpty ? 0 : 1)))
      .reduce((value, element) => value + element);
}

void part1(List<List<String>> map) {
  print(simulate([0, 0], Dir.east, map));
}

void part2(List<List<String>> map) {
  List<int> energy = [];

  for (int col = 0; col < map[0].length; col++) {
    energy.add(simulate([col, 0], Dir.south, map));
    energy.add(simulate([col, map.length - 1], Dir.north, map));
  }

  for (int row = 0; row < map.length; row++) {
    energy.add(simulate([0, row], Dir.east, map));
    energy.add(simulate([map[0].length - 1, row], Dir.west, map));
  }

  print(energy.reduce((value, element) => value > element ? value : element));
}

void main() {
  List<List<String>> data = new File("16.input")
      .readAsLinesSync().map((row) => row.split(''))
      .toList();

  part1(data);
  part2(data);
}