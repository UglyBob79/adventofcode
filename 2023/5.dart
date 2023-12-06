#!/usr/bin/env dart

import 'dart:io';

class PlantMap {
  final String name;
  PlantMap? next;
  List<List<int>> convs = [];

  PlantMap(this.name);

  void addConv(int destStart, int sourceStart, int len) {
    convs.add([sourceStart, sourceStart + len - 1, destStart - sourceStart]);
  }

  List<int> mapVals(List<int> vals) {
    return vals.map((v) => v + convs.firstWhere((conv) => (v >= conv[0] && v <= conv[1]), orElse: () => [0, 0, 0])[2]).toList();
  }

  bool isOverlap(List<int> range1, List<int> range2) {
    return (range1[0] <= range2[1] && range1[1] >= range2[0]) || range2[0] <= range1[1] && range2[1] >= range1[0];
  }

  List<List<int>> mapRanges(List<List<int>> ranges) {
    List<List<int>> out = [];

    while (ranges.isNotEmpty) {
      List<int> curr = ranges.removeAt(0);
      bool match = false;

      for (var conv in convs) {
        if (isOverlap(curr, conv)) {
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
            out.add(newRange);
            break;
          }
        }
      }

      if (!match) {
        out.add(curr);
      }
    }

    return out;
  }

  @override
  String toString() {
    StringBuffer buffer = new StringBuffer();
    buffer.writeln("\nPlantMap ${name} {");
      convs.forEach((c) => buffer.writeln("  (${c[0]}-${c[1]}: ${c[2]})"));
    buffer.writeln("}");
    return buffer.toString();
  }
}

void main() {
  List<String> data = new File("5.input")
      .readAsLinesSync()
      .toList();

  List<int> seeds = RegExp(r'(\d+)').allMatches(data[0]).map((match) => int.parse(match.group(0)!)).toList();

  List<PlantMap> maps = [];

  for (int i = 2; i < data.length; i++) {
    RegExpMatch? match = RegExp(r'(\d+) (\d+) (\d+)').firstMatch(data[i]);

    if (match != null) {
      List<int> conv = match.groups([1, 2, 3]).map((g) => int.parse(g!)).toList();
      maps.last.addConv(conv[0], conv[1], conv[2]);
    } else if (!data[i].isEmpty) {
      maps.add(PlantMap(data[i].split(' ')[0]));
    }
  }

  var locations = maps.fold(seeds, (curr, plantMap) => plantMap.mapVals(curr)).toList();
  print(locations.reduce((value, element) => value < element ? value : element));

  List<List<int>> ranges = List.generate((seeds.length / 2).ceil(), (index) => [seeds[index * 2], seeds[index * 2] + seeds[index * 2 + 1] - 1]).toList();

  var out = maps.fold(ranges, (curr, plantMap) => plantMap.mapRanges(curr)).toList();
  print(out.map((e) => e[0]).reduce((value, element) => value < element ? value : element));
}