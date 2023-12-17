#!/usr/bin/env dart

import 'dart:io';
import 'package:puzmat/puzmat.dart';
import 'dart:collection';

Map<Dir, List<int>> dMove = {
  Dir.north: [0, -1],
  Dir.south: [0, 1],
  Dir.west: [-1, 0],
  Dir.east: [1, 0]
};

Map<Dir, List<Dir>> turn = {
  Dir.north: [Dir.east, Dir.west],
  Dir.south: [Dir.east, Dir.west],
  Dir.west: [Dir.north, Dir.south],
  Dir.east: [Dir.north, Dir.south]
};

List<int> add(List<int> l1, List<int> l2) {
  return List.generate(l1.length, (index) => (l1[index] + l2[index]).toInt());
}

Queue<List<dynamic>> queue = Queue<List<dynamic>>();

void traverse(PuzMat mat, int minStraight, int maxStraight) {
  for (int i = 0; i < (3 << 2) + maxStraight; i++) {
    mat.addLayerFromMatrix(List<List<int>>.generate(
        mat.rows, (index) => List<int>.filled(mat.cols, 999999, growable: false),
        growable: false));
  }

  while (queue.isNotEmpty) {
    var task = queue.removeFirst();
    List<int> pos = task[0];
    Dir dir = task[1];
    int straight = task[2];
    int heat = task[3];

    if (!mat.inBounds(pos[1], pos[0])) {
      continue;
    }

    // why this as int bs?!?
    heat += mat[0][pos[1]][pos[0]] as int;

    int heatLayer = (Dir.values.indexOf(dir) << 2) + straight;

    if (heat >= mat[heatLayer][pos[1]][pos[0]]) {
      continue;
    } else {
      mat[heatLayer][pos[1]][pos[0]] = heat;
    }

    if (straight < maxStraight) {
      queue.add([add(pos, dMove[dir]!), dir, straight + 1, heat]);
    }

    if (straight >= minStraight) {
      for (Dir turnDir in turn[dir]!) {
        queue.add([add(pos, dMove[turnDir]!), turnDir, 1, heat]);
      }
    }
  }
}

void part1(List<List<int>> data) {
  var mat = PuzMat.fromMatrix(data);

  queue.add([[1, 0], Dir.east, 1, 0]);
  queue.add([[0, 1], Dir.south, 1, 0]);

  traverse(mat, 0, 3);

  int low = 999999;

  for (int i = 1; i < mat.layers; i++) {
    if (mat[i][mat.rows - 1][mat.cols - 1]! < low)
      low = mat[i][mat.rows - 1][mat.cols - 1]!;
  }

  print(low);
}

void part2(List<List<int>> data) {
  var mat = PuzMat.fromMatrix(data);

  queue.add([[1, 0], Dir.east, 2, 0]);
  queue.add([[0, 1], Dir.south, 2, 0]);

  traverse(mat, 4, 10);

  int low = 999999;

  for (int i = 1; i < mat.layers; i++) {
    if (mat[i][mat.rows - 1][mat.cols - 1]! < low)
      low = mat[i][mat.rows - 1][mat.cols - 1]!;
  }

  print(low);
}

void main() {
List<List<int>> data = File("17.input")
    .readAsLinesSync()
    .map((row) => row.split('').map((value) => int.parse(value)).toList())
    .toList();

  part1(data);
  part2(data);
}