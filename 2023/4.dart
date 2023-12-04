#!/usr/bin/env dart

import 'dart:io';

void part1(List<int> score) {
  var sum = score
      .map((element) => element == 0 ? 0 : 1 << (element - 1))
      .reduce((value, element) => value + element);

  print(sum);
}

void part2(List<int> score) {
  List<int> instances = List<int>.filled(score.length, 1);

  for (int i = 0; i < score.length; i++) {
    if (instances[i] > 0) {
      for (int j = i + 1; j <= i + score[i]; j++) {
        instances[j] += instances[i];
      }
    }
  }

  print(instances.reduce((value, element) => value + element));
}

void main() {
  List<String> data = new File("4.input").readAsLinesSync().toList();

  var score = data.map((card) => RegExp(r'\d+(?![:\d])').allMatches(card).map((match) => match.group(0)!).toSet()).map((set) => 35 - set.length).toList();

  part1(score);
  part2(score);
}
