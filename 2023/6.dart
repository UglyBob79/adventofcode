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

  var result = races.map((race) => calcWins(race[0], race[1]));

  print(result.reduce((value, element) => value * element));

  var time2 = int.parse(RegExp(r'\d+').allMatches(data[0]).map((match) => match.group(0)!).reduce((value, element) => value + element));
  var dist2 = int.parse(RegExp(r'\d+').allMatches(data[1]).map((match) => match.group(0)!).reduce((value, element) => value + element));

  print(calcWins(time2, dist2));
}