#!/usr/bin/env dart

import 'dart:io';

List<List<String>> transpose(List<List<String>> matrix) => matrix.isEmpty
    ? []
    : List.generate(matrix[0].length,
        (i) => List.generate(matrix.length, (j) => matrix[j][i]));

List<List<int>> findExpander(List<List<String>> data) {
  List<List<int>> expanders = [[], []];

  for (int y = 0; y < data.length; y++) {
    if (data[y].every((element) => element == '.')) {
      expanders[1].add(y);
    }
  }

  var trans = transpose(data);

  for (int x = 0; x < trans.length; x++) {
    if (trans[x].every((element) => element == '.')) {
      expanders[0].add(x);
    }
  }

  return expanders;
}

List<List<int>> findGalaxies(List<List<String>> data) => [
      for (int y = 0; y < data.length; y++)
        for (int x = 0; x < data[y].length; x++)
          if (data[y][x] == '#') [x, y]
    ];

bool inRange(int val, List<int>range) {
  range.sort();
  return range[0] <= val && val <= range[1];
}

int calcDistance(List<int> g1, List<int> g2, List<List<int>> expanders, int expansion) {
  int dist = (g2[0] - g1[0]).abs() + (g2[1] - g1[1]).abs();

  [0, 1].forEach((i) {
    dist += expansion * expanders[i].where((x) => inRange(x.toInt(), [g1[i], g2[i]])).length;
  });

  return dist;
}

int calcDistSum(List<List<int>> galaxies, List<List<int>> expanders, int expansion) =>
    [
      for (var i = 0; i < galaxies.length; i++)
        for (var j = i + 1; j < galaxies.length; j++)
          calcDistance(galaxies[i], galaxies[j], expanders, expansion)
    ].reduce((a, b) => a + b);

void main() {
  var data = new File("11.input")
      .readAsLinesSync()
      .map((line) => line.split('')).toList()
      .toList();

  var expanders = findExpander(data);
  var galaxies = findGalaxies(data);

  print(calcDistSum(galaxies, expanders, 1));
  print(calcDistSum(galaxies, expanders, 1000000 - 1));
}