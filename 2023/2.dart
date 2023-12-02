#!/usr/bin/env dart

import 'dart:io';
import 'dart:math';

Map<String, int> limits = {'red': 12, 'green': 13, 'blue': 14};

void part1(List<List<Map<String, int>>> games) {
  int sum = games
      .asMap()
      .map((index, game) => MapEntry(
          index + 1,
          game
              .map((pull) => pull
                  .map((color, value) =>
                      MapEntry(color, (value > limits[color]!) ? false : true))
                  .values
                  .reduce((value, element) => value && element))
              .reduce((value, element) => value && element)))
      .entries
      .where((entry) => entry.value)
      .fold(0, (prev, entry) => prev + entry.key);

  print(sum);
}

void part2(List<List<Map<String, int>>> games) {
  int sum = games
      .map((game) => limits.keys
          .map((color) =>
              game.map((pull) => pull[color] ?? 0).toList().reduce(max))
          .toList()
          .reduce((value, element) => value * element))
      .reduce((value, element) => value + element);

  print(sum);
}

void main() {
  List<String> data = new File("2.input").readAsLinesSync();

  List<List<Map<String, int>>> games = data
      .map((line) => new RegExp(r'Game ([0-9]+): (.*)')
          .firstMatch(line)!
          .group(2)!
          .split(';')
          .map((s) => Map.fromIterable(s.trim().split(', ').map((s) => s.split(' ')),
              key: (item) => item[1].toString(),
              value: (item) => int.parse(item[0])))
          .toList())
      .toList();

  part1(games);

  part2(games);
}
