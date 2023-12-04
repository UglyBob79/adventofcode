#!/usr/bin/env dart

import 'dart:io';

void scanScematic(List<String> data) {
  Map<String, int> parts = {};
  Map<String, List<int>> gears = {};

  data.asMap().forEach((y, row) {
    for (RegExpMatch match in RegExp(r'\d+').allMatches(row)) {
      for (int sy = y - 1; sy <= y + 1; sy++) {
        for (int sx = match.start - 1; sx <= match.end; sx ++) {
          if (sx < 0 || sy < 0 || sx >= row.length || sy >= data.length) continue;

          if (data[sy].codeUnitAt(sx) != 46 && (data[sy].codeUnitAt(sx) < 48 || data[sy].codeUnitAt(sx) > 57)) {
            parts[[match.start, y].toString()] = int.parse(match.group(0)!);

            if (data[sy][sx] == '*')
              gears.putIfAbsent([sx, sy].toString(), () => []).add(int.parse(match.group(0)!));
          }
        }
      }
    }
  });

  print(parts.values.reduce((value, element) => value + element));
  print(gears.values.where((element) => element.length > 1).map((gear) => gear.reduce((a, b) => a * b)).reduce((a, b) => a +b));
}

void main() {
  List<String> data = new File("3.input")
      .readAsLinesSync()
      .toList();
  scanScematic(data);
}