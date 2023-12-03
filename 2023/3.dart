#!/usr/bin/env dart

import 'dart:io';

bool checkSymbol(List<List<int>> data, int x, int y) {
  if (x < 0 || y < 0 || x >= data[0].length || y >= data.length) {
    return false;
  } else {
    return data[y][x] != 46 && (data[y][x] < 48 || data[y][x] > 57);
  }
}

List<int>? checkStar(List<List<int>> data, int x, int y) {
  if (x < 0 || y < 0 || x >= data[0].length || y >= data.length) {
    return null;
  } else {
    return data[y][x] == 42 ? [x, y] : null;
  }
}

void scanScematic(List<List<int>> data) {
  int sum = 0;
  Map<String, List<int>> stars = {};

  for (int y = 0; y < data.length; y++) {
    int num = 0;
    bool symbol = false;
    String? star = null;

    for (int x = 0; x < data[y].length; x++) {
      int c = data[y][x];

      if (c >= 48 && c <= 57) {
        if (num > 0) num *= 10;

        num += c - 48;

        if (!symbol) {
          symbol = List.generate(3, (dx) => x - 1 + dx).any((newX) =>
              List.generate(3, (dy) => y - 1 + dy)
                  .any((newY) => checkSymbol(data, newX, newY)));
        }

        for (int newX = x - 1; newX <= x + 1 && star == null; newX++) {
          for (int newY = y - 1; newY <= y + 1 && star == null; newY++) {
            star = checkStar(data, newX, newY)?.toString();
          }
        }
      } else {
        if (num > 0) {
          if (symbol) sum += num;

          symbol = false;

          if (star != null) stars.putIfAbsent(star, () => []).add(num);

          num = 0;
          star = null;
        }
      }
    }

    if (num > 0) {
      if (symbol) sum += num;

      if (star != null) stars.putIfAbsent(star, () => []).add(num);
    }
  }

  int gears = 0;

  for (List<int> star in stars.values) {
    if (star.length == 2) {
      gears += star[0] * star[1];
    }
  }

  print(sum);
  print(gears);
}

void main() {
  List<List<int>> data = new File("3.input")
      .readAsLinesSync()
      .map((line) => line.codeUnits)
      .toList();

  scanScematic(data);
}
