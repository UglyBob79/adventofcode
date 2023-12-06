#!/usr/bin/env dart

import 'dart:io';
import 'dart:math';

int calcWins(int time, int dist) {
  double discr = sqrt(time * time - 4 * (dist + 1));
  List<int> x = [((time - discr) / 2).ceil(), ((time + discr) / 2).floor()];

  return x[1] - x[0] + 1;
}

void main() {
  List<String> data = new File("6.input")
      .readAsLinesSync()
      .toList();

  var time = RegExp(r'\d+').allMatches(data[0]).map((match) => int.parse(match.group(0)!)).toList();
  var dist = RegExp(r'\d+').allMatches(data[1]).map((match) => int.parse(match.group(0)!)).toList();
  var races = List.generate(time.length, (index) => [time[index], dist[index]]);

  print(races.map((race) => calcWins(race[0], race[1])).reduce((value, element) => value * element));
  print(calcWins(int.parse(time.map((t) => t.toString()).join()), int.parse(dist.map((d) => d.toString()).join())));
}