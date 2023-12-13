#!/usr/bin/env dart

import 'dart:io';
import 'dart:math';
import 'package:matrices/matrices.dart';

int? findHorizontalMirror(Matrix map, int errorAccept) {
  for (int i = 0; i < map.rowCount - 1; i++) {
    int errors = 0;
    for (int j = 0; j < min(i + 1, map.rowCount - i - 1); j++) {
      for (int n = 0; n < map[i].length; n++) {
        if (map[i - j][n] != map[i + j + 1][n]) {
          errors++;
        }
      }
    }

    if (errors == errorAccept) {
      return i + 1;
    }
  }

  return null;
}

int mirror(Matrix map, int errorAccept) {
  int? horiz = findHorizontalMirror(map, errorAccept);

  return horiz != null ? 100 * horiz : findHorizontalMirror(map.transpose, errorAccept)!;
}

void main() {
  List<List<List<double>>> data = [[]];
  int i = 0;

  for (String line in new File("13.input").readAsLinesSync()) {
    if (line.isEmpty) {
      data.add([]);
      i++;
      continue;
    }

    data[i].add(line.split('').map((e) => e == '#' ? 1.0 : 0.0).toList());
  }

  List<Matrix> maps = data.map((m) => Matrix.fromList(m)).toList();

  print(maps.map((map) => mirror(map, 0)).reduce((value, element) => value + element));
  print(maps.map((map) => mirror(map, 1)).reduce((value, element) => value + element));
}