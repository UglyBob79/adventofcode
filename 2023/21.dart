#!/usr/bin/env dart

import 'dart:io';
import 'package:puzmat/puzmat.dart';
import 'dart:collection';

void part1(List<int> start, PuzMat<String> map) {
  map.clearLayer(2);
  map.markMoveRange(start, 64, 'O', 2, [1, 2], exact: true);
  //print(map);

  print(map.layerCount(2, 'O'));
}

List<List<int>> possiblePoints(List<int> point, PuzMat<String> map) {
    // Return a list of all possible points that can be reached from the current point
    var points = List<List<int>>.empty(growable: true);
    var dirs = [[0, 1], [0, -1], [1, 0], [-1, 0]];

    for (var dir in dirs) {
      var newPoint = [point[0] + dir[0], point[1] + dir[1]];
      if (map[1][newPoint[1] % 131][newPoint[0] % 131] == ' ') {
        points.add(newPoint);
      }
    }

    return points;
}
Map<int, int> bfs(List<int> point, PuzMat<String> map,  int maxSteps) {
    // Use the Breadth first search to find the number of points hit each step, and return the dictionary with key of number of steps taken,
    // and value of number of points hit
    var tiles = Map<int, int>();
    var visited = Set<String>();
    Queue<List<dynamic>> queue = Queue<List<dynamic>>();

    queue.add([point, 0]);

    while (queue.isNotEmpty) {
      var task = queue.removeFirst();
      List<int> currPoint = task[0];
      int dist = task[1];

      if (dist == (maxSteps + 1) || visited.contains(currPoint.toString())) {
        continue;
      }

      tiles.putIfAbsent(dist, () => 0);
      tiles[dist] = tiles[dist]! + 1;

      visited.add(currPoint.toString());

      for (var nextPoint in possiblePoints(currPoint, map)) {
        queue.add([nextPoint, dist + 1]);
      }
    }

    return tiles;
}

int calculatePossibleSpots(List<int> start, PuzMat<String> map, int maxSteps) {
    // Get the output from bfs, and then return the sum of all potential stopping points in the tiles output based on even numbers
    var tiles = bfs(start, map, maxSteps);

    return tiles.entries
      .where((entry) => entry.key % 2 == maxSteps % 2)
      .map((entry) => entry.value)
      .fold(0, (sum, amount) => sum + amount);
}

int quad(List<int> y, int n) {
  // Use the quadratic formula to find the output at the large steps based on the first three data points
  int a = (y[2] - (2 * y[1]) + y[0]) ~/ 2;
  int b = y[1] - y[0] - a;
  int c = y[0];

  return (a * n * n) + (b * n) + c;
}

// Part 2 inspired by @CalSimmon (https://github.com/CalSimmon)
void part2(List<int> start, PuzMat<String> map) {
  int goal = 26501365;
  int size = map.rows;
  int edge = size ~/ 2;

  List<int> y = List.generate(3, (i) => calculatePossibleSpots(start, map, edge + i * size));

  print(quad(y, ((goal - edge) ~/ size)));
}

void main() {
  var map = PuzMat.mapLayersFromLayer(PuzMat<String>.fromFile(File('21.input'), ''), 0, [['.'], ['#'], ['S']], empty: ['.', ' ', ' ']);
  map.setToStringMode(ToStringMode.overlay);

  List<int> start = map.layerFindAll(2, 'S')[0];

  part1(start, map);
  part2(start, map);
}