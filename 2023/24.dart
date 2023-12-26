#!/usr/bin/env dart

import 'dart:io';

int A = 0;
int B = 1;
int C = 2;

int X = 0;
int Y = 1;
int Z = 2;

int PT = 0;
int VEL = 1;

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
  print("Hailstone A: ${h1[PT]} @ ${h1[VEL]}");
  print("Hailstone B: ${h2[PT]} @ ${h2[VEL]}");
  int crossProduct = h1[VEL][X] * h2[VEL][Y] - h1[VEL][Y] * h2[VEL][X];

  if (crossProduct == 0) {
    print("Hailstones' paths are parallel; they never intersect.");
    return false;
  }

  double t1 = (h2[VEL][Y] * (h2[PT][X] - h1[PT][X]) - h2[VEL][X] * (h2[PT][Y] - h1[PT][Y])) / crossProduct;
  double t2 = (h1[VEL][X] * (h2[PT][Y] - h1[PT][Y]) - h1[VEL][Y] * (h2[PT][X] - h1[PT][X])) / (h1[VEL][Y] * h2[VEL][X] - h1[VEL][X] * h2[VEL][Y]);

  if (t1 < 0 && t2 < 0) {
    print("Hailstones' paths crossed in the past for both hailstones.");
    return false;
  } else if (t1 < 0) {
    print("Hailstones' paths crossed in the past for hailstone A.");
    return false;
  } else if (t2 < 0) {
    print("Hailstones' paths crossed in the past for hailstone B.");
    return false;
  } else {
    double x = h1[PT][X] + h1[VEL][X] * t1;
    double y = h1[PT][Y] + h1[VEL][Y] * t1;

    if (inside(x, y, min, max)) {
      print("Hailstones' paths will cross inside the test area (at x=$x, y=$y).");
      return true;
    } else {
      print("Hailstones' paths will cross outside the test area (at x=$x, y=$y).");
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
}