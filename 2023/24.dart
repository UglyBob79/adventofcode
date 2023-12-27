#!/usr/bin/env dart

import 'dart:io';

import '18.dart';

int A = 0;
int B = 1;
int C = 2;

int X = 0;
int Y = 1;
int Z = 2;

int PT = 0;
int VEL = 1;

bool debugMode = false;

void debug(Object obj) {
  if (debugMode) {
    print(obj);
  }
}

bool inside(double x, double y, int min, int max) {
  return x >= min && x <= max && y >= min && y <= max;
}

List<int> getABC(List<List<int>> h) {
  int a = h[VEL][Y];
  int b = -h[VEL][X];
  int c = a * h[PT][X] + b * h[PT][Y];

  return [a, b, c];
}

bool isIntersecting(var h1, var h2, int min, int max) {
  debug("Hailstone A: ${h1[PT]} @ ${h1[VEL]}");
  debug("Hailstone B: ${h2[PT]} @ ${h2[VEL]}");
  int crossProduct = h1[VEL][X] * h2[VEL][Y] - h1[VEL][Y] * h2[VEL][X];

  if (crossProduct == 0) {
    debug("Hailstones' paths are parallel; they never intersect.");
    return false;
  }

  double t1 = (h2[VEL][Y] * (h2[PT][X] - h1[PT][X]) - h2[VEL][X] * (h2[PT][Y] - h1[PT][Y])) / crossProduct;
  double t2 = (h1[VEL][X] * (h2[PT][Y] - h1[PT][Y]) - h1[VEL][Y] * (h2[PT][X] - h1[PT][X])) / (h1[VEL][Y] * h2[VEL][X] - h1[VEL][X] * h2[VEL][Y]);

  if (t1 < 0 && t2 < 0) {
    debug("Hailstones' paths crossed in the past for both hailstones.");
    return false;
  } else if (t1 < 0) {
    debug("Hailstones' paths crossed in the past for hailstone A.");
    return false;
  } else if (t2 < 0) {
    debug("Hailstones' paths crossed in the past for hailstone B.");
    return false;
  } else {
    double x = h1[PT][X] + h1[VEL][X] * t1;
    double y = h1[PT][Y] + h1[VEL][Y] * t1;

    if (inside(x, y, min, max)) {
      debug("Hailstones' paths will cross inside the test area (at x=$x, y=$y).");
      return true;
    } else {
      debug("Hailstones' paths will cross outside the test area (at x=$x, y=$y).");
      return false;
    }
  }
}

void part1(List<List<List<int>>> hails, int min, int max) {
  int count = 0;
  for (int i = 0; i < hails.length; i++) {
    for (int j = i + 1; j < hails.length; j++) {
      List<List<int>> hail1 = hails[i];
      List<List<int>> hail2 = hails[j];

      if (isIntersecting(hail1, hail2, min, max)) {
        count++;
      }
    }
  }

  print(count);
}

Set<int> calcPossibleSpeeds(int distance, int hailSpeed) {
  Set<int> possible = {};
  for (int v = -1000; v <= 1000; v++) {
    int catchUpSpeed = v - hailSpeed;

    if (catchUpSpeed != 0 && distance % catchUpSpeed == 0) {
      possible.add(v);
    }
  }

  return possible;
}

/// this does not work on the example :(
List<int> calcAxisSpeeds(List<List<List<int>>> hails) {
  List<Set<int>> axisPossible = List.generate(3, (_) => {});

  for (int i = 0; i < hails.length - 1; i++) {
    for (int j = i + 1; j < hails.length; j++) {
      for (int axis = 0; axis < 3; axis++) {
        if (hails[i][VEL][axis] == hails[j][VEL][axis]) {
          Set<int> possible = calcPossibleSpeeds(hails[i][PT][axis] - hails[j][PT][axis], hails[i][VEL][axis]);
          if (axisPossible[axis].isEmpty) {
            axisPossible[axis].addAll(possible);
          } else {
            axisPossible[axis] = axisPossible[axis].intersection(possible);
          }
        }
      }
    }
  }

  return axisPossible.map((e) => e.first).toList();
}

List<int> calcPos(List<List<List<int>>> hails, List<int> stoneSpeed) {
  var ha = hails[0];
  var hb = hails[1];
  var ma = (ha[VEL][Y] - stoneSpeed[Y]) / (ha[VEL][X] - stoneSpeed[X]);
  var mb = (hb[VEL][Y] - stoneSpeed[Y]) / (hb[VEL][X] - stoneSpeed[X]);
  var ca = ha[PT][Y] - (ma * ha[PT][X]);
  var cb = hb[PT][Y] - (mb * hb[PT][X]);

  int x = ((cb - ca) / (ma - mb)).round();
  int y = (ma * x + ca).round();
  int t = (x - ha[PT][X]) ~/ (ha[VEL][X] - stoneSpeed[X]);
  int z = ha[PT][Z] + (ha[VEL][Z] - stoneSpeed[Z]) * t;

  return [x, y, z];
}

void part2(List<List<List<int>>> hails) {
  List<int> stoneSpeed = calcAxisSpeeds(hails);
  var pos = calcPos(hails, stoneSpeed);

  print(pos.reduce((value, element) => value + element));
}

void main() {
  String file = "24.input";
  List<List<List<int>>> data = File(file)
      .readAsLinesSync()
      .map((line) => line.split('@')
          .map((group) => group.split(',').map((s) => int.parse(s)).toList())
          .toList())
      .toList();

  int min = file == "24.example" ? 7 : 200000000000000;
  int max = file == "24.example" ? 27 : 400000000000000;

  part1(data, min, max);
  part2(data);
}