#!/usr/bin/env dart

import 'dart:io';

void part1(List<String> data) {
  int sum = data
      .map((d) => d.codeUnits
          .map((c) => c)
          .fold(0, (value, element) => ((value + element) * 17) % 256))
      .reduce((value, element) => value + element);

  print(sum);
}

void part2(List<String> data) {
  List<List<Map<String, int>>> boxes = List.generate(256, (_) => []);

  for (String cmd in data) {
    var match = RegExp(r'([a-z]+)([-=]{1})([0-9]?)').firstMatch(cmd);
    if (match != null) {
      String label = match.group(1)!;
      String oper = match.group(2)!;
      int focal = match.group(3) != "" ? int.parse(match.group(3)!) : -1;
      int boxIndex = label.codeUnits.fold(0, (int acc, int codeUnit) => ((acc + codeUnit) * 17) % 256);
      int lensIndex = boxes[boxIndex].indexWhere((lens) => lens.containsKey(label));

      if (oper == '=') {
        if (lensIndex != -1) {
          boxes[boxIndex][lensIndex][label] = focal;
        } else {
          boxes[boxIndex].add({label: focal});
        }
      } else {
        if (lensIndex != -1) {
          boxes[boxIndex].removeAt(lensIndex);
        }
      }
    }
  }

  int sum = 0;

  for (int i = 0; i < boxes.length; i++) {
    if (!boxes[i].isEmpty) {
      for (int j = 0; j < boxes[i].length; j++) {
        sum += (i + 1) * (j + 1) * boxes[i][j][boxes[i][j].keys.first]!;
      }
    }
  }
  print(sum);
}

void main() {
  List<String> data = new File("15.input")
      .readAsLinesSync()
      .toList()[0].split(',');

  part1(data);
  part2(data);
}