#!/usr/bin/env dart

import 'dart:io';

void part1(List<int> dirs, Map<String, List<String>> nodes) {
  var curr = 'AAA';
  int i = 0;

  while (curr != 'ZZZ') {
    curr = nodes[curr]![dirs[i++ % dirs.length]];
  }

  print(i);
}

int calculateLCM(int a, int b) {
  int gcd = calculateGCD(a, b);
  return (a * b) ~/ gcd;
}

int calculateGCD(int a, int b) {
  while (b != 0) {
    int remainder = a % b;
    a = b;
    b = remainder;
  }
  return a;
}

void part2(List<int> dirs, Map<String, List<String>> nodes) {
  List<String> currs = nodes.keys.where((k) => k.endsWith('A')).toList();
  List<int> loops = List<int>.filled(currs.length, 0);

  for (int j = 0; j < currs.length; j++) {
    String curr = currs[j];
    int i = 0;
    int steps = 0;

    while (loops[j] == 0) {
      curr = nodes[curr]![dirs[i++ % dirs.length]];

      if (curr.endsWith('Z')) {
        if (steps > 0 && (i - steps == steps)) {
          loops[j] = steps;
          break;
        }
        steps = i;
      }
    }
  }

  print(loops.reduce(calculateLCM));
}

void main() {
  List<String> data = new File("8.input")
      .readAsLinesSync()
      .toList();

  List<int> dirs = data[0].split('').map((e) => ['L', 'R'].indexOf(e)).toList();

  Map<String, List<String>> nodes = Map.fromEntries(data.skip(2).map((row) {
    var matches = RegExp(r'([A-Z0-9]+)').allMatches(row);
    return MapEntry(matches.elementAt(0).group(0)!, [matches.elementAt(1).group(0)!, matches.elementAt(2).group(0)!]);
  }));

  part1(dirs, nodes);
  part2(dirs, nodes);
}