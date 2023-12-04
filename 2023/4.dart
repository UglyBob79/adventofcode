#!/usr/bin/env dart

import 'dart:io';

void part1(List<List<List<int>>> cards) {
  var sum = cards
      .map((element) =>
          element[0].where((item) => element[1].contains(item)).toList().length)
      .map((element) => element == 0 ? 0 : 1 << (element - 1))
      .reduce((value, element) => value + element);

  print(sum);
}

void part2(List<List<List<int>>> cards) {
  List<int> instances = List<int>.filled(cards.length, 1);

  for (int i = 0; i < cards.length; i++) {
    if (instances[i] > 0) {
      int count = cards[i][0].where((item) => cards[i][1].contains(item)).length;
      for (int j = i + 1; j <= i + count; j++) {
        instances[j] += instances[i];
      }
    }
  }

  print(instances.reduce((value, element) => value + element));
}

void main() {
  List<String> data = new File("4.input").readAsLinesSync().toList();

  List<List<List<int>>> cards = data.map((card) {
    var match = RegExp(r'Card\s+([0-9]+):([^|]+)\|(.*)').firstMatch(card);
    var winning = match!.group(2)!.trim().split(RegExp(r'\s+')).map((e) => int.parse(e)).toList();
    var numbers = match.group(3)!.trim().split(RegExp(r'\s+')).map((e) => int.parse(e)).toList();

    return [winning, numbers];
  }).toList();

  part1(cards);
  part2(cards);
}
