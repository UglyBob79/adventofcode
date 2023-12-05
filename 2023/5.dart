#!/usr/bin/env dart

import 'dart:io';

class PlantMap {
  final String name;
  PlantMap? next;
  List<List<int>?> convs = [];

  PlantMap(this.name);

  void addConv(int destStart, int sourceStart, int len) {
    convs.add([sourceStart, sourceStart + len - 1, destStart - sourceStart]);
  }

  int mapVal(int val) {
    var conv = convs.firstWhere((conv) => (val >= conv![0] && val <= conv[1]), orElse: () => null);

    if (conv != null)
      val = val + conv[2];

    return next != null ? next!.mapVal(val) : val;
  }

  bool overlap(List<int> range1, List<int> range2) {
    return (range1[0] <= range2[1] && range1[1] >= range2[0]) || range2[0] <= range1[1] && range2[1] >= range1[0];
  }

  int mapRange(List<int> range) {
    List<List<int>> ranges = [range];
    List<int> minVals = [];

    while (ranges.length > 0) {
      List<int> curr = ranges.removeAt(0);
      bool match = false;

      for (var conv in convs) {
        if (overlap(curr, conv!)) {
          match = true;

          if (curr[0] < conv[0]) {
            ranges.add([curr[0], conv[0] - 1]);
            ranges.add([conv[0], curr[1]]);
            break;
          } else if (curr[1] > conv[1]) {
            ranges.add([curr[0], conv[1]]);
            ranges.add([conv[1] + 1, curr[1]]);
            break;
          } else {
            List<int> newRange = curr.map((e) => e + conv[2]).toList();
            minVals.add( next != null ? next!.mapRange(newRange) : newRange[0]);
            break;
          }
        }
      }

      if (!match) {
        minVals.add((next != null) ? next!.mapRange(curr) : curr[0]);
      }
    }

   return minVals.reduce((value, element) => value < element ? value : element);
  }

  @override
  String toString() {
    StringBuffer buffer = new StringBuffer();
    buffer.writeln("PlantMap ${name} {");
      convs.forEach((c) => buffer.writeln("  (${c![0]}-${c[1]}: ${c[2]})"));
    buffer.writeln("}");
    return buffer.toString();
  }
}

void main() {
  List<String> data = new File("5.input")
      .readAsLinesSync()
      .toList();

  List<int> seeds = RegExp(r'(\d+)').allMatches(data[0]).map((match) => int.parse(match.group(0)!)).toList();

  PlantMap? start = null;
  PlantMap? curr = null;

  for (int i = 2; i < data.length; i++) {
    RegExpMatch? match = RegExp(r'(\d+) (\d+) (\d+)').firstMatch(data[i]);

    if (match != null) {
      List<int> conv = match.groups([1, 2, 3]).map((g) => int.parse(g!)).toList();
      curr!.addConv(conv[0], conv[1], conv[2]);
    } else if (!data[i].isEmpty) {
      PlantMap plantMap = PlantMap(data[i].split(' ')[0]);

      if (start == null)
        start = plantMap;

      if (curr != null)
        curr.next = plantMap;

      curr = plantMap;
    }
  }

  int lowest = seeds.map((seed) => start!.mapVal(seed)).reduce((value, element) => value < element ? value : element);
  print(lowest);

  List<List<int>> ranges = List.generate((seeds.length / 2).ceil(), (index) => seeds.sublist(index * 2, (index + 1) * 2),).toList();
  lowest = ranges.map((range) => start!.mapRange([range[0], range[0] + range[1] - 1])).reduce((value, element) => value < element ? value : element);
  print(lowest);
}