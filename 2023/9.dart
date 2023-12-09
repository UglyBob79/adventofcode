#!/usr/bin/env dart

import 'dart:io';

int calcNext(List<int> history) {
  List<List<int>> gen = [history];
  int level = 0;

  while (!gen[level].every((element) => element == 0)) {
    gen.add(List.generate(
      gen[level].length - 1,
      (index) => gen[level][index + 1] - gen[level][index],
    ));
    level++;
  }

  gen[level].add(0);

  while (level > 0) {
    gen[level - 1].add(gen[level - 1].last + gen[level].last);
    level--;
  }

  return gen[0].last;
}

void main() {
  List<String> data = new File("9.input")
      .readAsLinesSync()
      .toList();

  var historys = data.map((line) => line.split(' ').map((e) => int.parse(e)).toList()).toList();

  var nexts = historys.map((history) => calcNext(history)).toList();
  print(nexts.reduce((value, element) => value + element));

  nexts = historys.map((history) => calcNext(history.reversed.toList())).toList();
  print(nexts.reduce((value, element) => value + element));
}