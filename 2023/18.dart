#!/usr/bin/env dart

import 'dart:io';

Map<String, List<int>> move = {
  'R': [1, 0],
  'D': [0, 1],
  'L': [-1, 0],
  'U': [0, -1]
};

List<int> add(List<int> l1, List<int> l2) {
  return List.generate(l1.length, (index) => (l1[index] + l2[index]).toInt());
}

List<int> moveSteps(List<int> pos, String dir, int steps) {
  return add(pos,  move[dir]!.map((e) => e * steps).toList());
}

int shoelaceFormula(List<List<int>> points) {
  if (points.length < 3) {
    throw ArgumentError('A polygon must have at least three vertices.');
  }

  int sum1 = 0;
  int sum2 = 0;
  int n = points.length;

  for (int i = 0; i < n; i++) {
    int xi = points[i][0];
    int yi = points[i][1];

    int xj = points[(i + 1) % n][0];
    int yj = points[(i + 1) % n][1];

    sum1 += (xi * yj);
    sum2 += (yi * xj);
  }

  int area = ((sum1 - sum2).abs() ~/ 2);
  return area;
}

List<dynamic> getPointsAndCircum(List<List<String>> plan, bool useHex) {
  List<List<int>> points = [];
  List<int> pos = [0, 0];
  int circum = 0;

  for (var instr in plan) {
    points.add(pos);

    int steps = 0;
    String dir = '';

    if (!useHex) {
      steps = int.parse(instr[1]);
      dir = instr[0];
    } else {
      int val = int.parse(instr[2].replaceAll(RegExp(r'[#()]'), ''), radix: 16);
      dir = move.keys.elementAt(val & 0xF);
      steps = val >> 4;
    }

    circum += steps;
    pos = moveSteps(pos, dir, steps);
  }

  return [points, circum];
}

int getArea(List<List<String>> plan, bool useHex) {
  var[points, circum] = getPointsAndCircum(plan, useHex);

  int area = shoelaceFormula(points);

  return area + (circum as int) ~/ 2 + 1;
}

void part1(List<List<String>> plan) {
  print(getArea(plan, false));
}

void part2(List<List<String>> plan) {
  print(getArea(plan, true));
}

void main() {
List<List<String>> data = File("18.input")
    .readAsLinesSync()
    .map((row) => row.split(' '))
    .toList();

  part1(data);
  part2(data);
}