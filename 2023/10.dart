#!/usr/bin/env dart

import 'dart:io';
import 'dart:math';

var pipeDirs = {
  '|': [[0, -1], [0, 1]],
  '-': [[-1, 0], [1, 0]],
  'L': [[0, -1], [1, 0]],
  'J': [[0, -1], [-1, 0]],
  '7': [[-1, 0], [0, 1]],
  'F': [[0, 1], [1, 0]]
};

var rotations = {
  '|': [[1, 0], [0, 1]],
  '-': [[1, 0], [0, 1]],
  'L': [[0, 1], [1, 0]],
  'J': [[0, -1], [-1, 0]],
  '7': [[0, 1], [1, 0]],
  'F': [[0, -1], [-1, 0]]
};

List<int> add(List<int> a, List<int> b) {
  assert(a.length == b.length);
  return List.generate(a.length, (index) => a[index] + b[index]);
}

List<int> inv(List<int> a) {
  return a.map((e) => -e).toList();
}

bool equal(List<int> a, List<int> b) {
  return a.length == b.length &&
      a.asMap().entries.every((entry) => entry.value == b[entry.key]);
}

List<int>? findStart(List<List<String>> data) {
  for (int y = 0; y < data.length; y++) {
    for (int x = 0; x < data[y].length; x++) {
      if (data[y][x] == 'S') {
        return [x, y];
      }
    }
  }

  return null;
}

String? matchPipe(List<List<int>> dirs) {
  return pipeDirs.keys.firstWhere(
    (key) => pipeDirs[key]!.every((list) => exists(list, dirs)),
    orElse: () => '',
  );
}

bool exists(List<int> p, List<List<int>> list) {
  return list.any((element) => p[0] == element[0] && p[1] == element[1]);
}

List<List<int>> findStartDirs(List<List<String>> data, List<int> start) {
  List<List<int>> startDirs = [];

  for (var dir in [[1, 0], [0, 1], [-1, 0], [0, -1]]) {
    var p = add(start, dir);

    if (p[1] >= 0 && p[1] < data.length && p[0] >= 0 && p[0] < data[p[1]].length && pipeDirs[data[p[1]][p[0]]] != null) {
      pipeDirs[data[p[1]][p[0]]]!.forEach((pipeDir) {
        if (equal(add(p, pipeDir), start)) {
          startDirs.add(dir);
        }
      });
    }
  }

  return startDirs;
}

List<int> matrixMult(List<List<int>> matrix, List<int> vector) {
  return [
    matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
    matrix[1][0] * vector[0] + matrix[1][1] * vector[1]
  ];
}

void printMap(List<List<String>> data) {
  for (var line in data) {
    print(line.join(''));
  }
}

List<List<int>> part1(List<List<String>> data) {
  var start = findStart(data)!;
  var startDirs = findStartDirs(data, start);

  data[start[1]][start[0]] = matchPipe(startDirs)!;

  List<int> curr = start;
  List<int> dir = startDirs[0];
  List<List<int>> loop = [];

  int step = 0;

  while (true) {
    loop.add(curr);

    curr = add(curr, dir);
    step++;

    if (equal(curr, start))
      break;

    dir = matrixMult(rotations[data[curr[1]][curr[0]]]!, dir);
  }

  print(step ~/ 2);

  return loop;
}

void part2(List<List<String>> data, List<List<int>> loop) {
  int area = 0;

  for (int y = 0; y < data.length; y++) {
    int inIntersect = 0;
    int outIntersect = 0;

    for (int x = 0; x < data[y].length; x++) {
      if (exists([x, y], loop)) {
        pipeDirs[data[y][x]]!.forEach((pipeDir) {
          if (pipeDir[1] == -1) {
            inIntersect++;
          }
          if (pipeDir[1] == 1) {
            outIntersect++;
          }
        });
      } else {
        if (min(inIntersect, outIntersect) % 2 == 1) {
          area++;
          data[y][x] = 'I';
        } else {
          data[y][x] = 'O';
        }
      }
    }
  }

  print(area);
}

void main() {
  var data = new File("10.input")
      .readAsLinesSync()
      .map((line) => line.split('')).toList()
      .toList();

  List<List<int>> loop = part1(data);
  part2(data, loop);
}
