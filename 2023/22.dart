#!/usr/bin/env dart

import 'dart:io';
import 'dart:math';

Map<int, Map<int, Map<int, int>>> buildSpace(List<List<List<int>>> bricks) {
  Map<int, Map<int, Map<int, int>>> space = {};

  for (var brick in bricks) {
    addBrick(brick, space);
  }

  return space;
}

bool isBlocked(var space, int x, int y, int z) {
  return (space.containsKey(x) && space[x]!.containsKey(y) && space[x]![y]!.containsKey(z)) || z <= 0;
}

int getBlockIndexAt(var space, int x, int y, int z) {
  if (z == 0 || !isBlocked(space, x, y, z)) {
    return -1;
  }

  return space[x]![y]![z]!;
}

void addBrick(var brick, var space) {
  for (int x = brick[0][0]; x <  brick[0][0] + brick[1][0]; x++) {
    space.putIfAbsent(x, () => <int, Map<int, int>>{});
    for (int y = brick[0][1]; y < brick[0][1] + brick[1][1]; y++) {
      space[x]!.putIfAbsent(y, () => <int, int>{});
      for (int z = brick[0][2]; z < brick[0][2] + brick[1][2]; z++) {
        space[x]![y]![z] = brick[2][0]; // index
      }
    }
  }
}

void removeBrick(var brick, var space) {
  for (int x = brick[0][0]; x <  brick[0][0] + brick[1][0]; x++) {
    for (int y = brick[0][1]; y < brick[0][1] + brick[1][1]; y++) {
      for (int z = brick[0][2]; z < brick[0][2] + brick[1][2]; z++) {
        space[x][y].remove(z);
      }
    }
  }
}

bool canFall(var brick, var space) {
  for (int x = brick[0][0]; x <  brick[0][0] + brick[1][0]; x++) {
    for (int y = brick[0][1]; y < brick[0][1] + brick[1][1]; y++) {
      for (int z = brick[0][2]; z < brick[0][2] + brick[1][2]; z++) {
        if (isBlocked(space, x, y, z - 1) && getBlockIndexAt(space, x, y, z - 1) != brick[2][0]) { // get index
          return false;
        }
      }
    }
  }

  return true;
}

void doFall(var brick, var space) {
  removeBrick(brick, space);

  // fall in z-axis
  brick[0][2] -= 1;

  addBrick(brick, space);
}

bool fall(var bricks, var space) {
  bool stable = true;

  for (var brick in bricks) {
    if (canFall(brick, space)) {
      doFall(brick, space);
      stable = false;
    }
  }

  return stable;
}

int brickCompare(List<List<int>> a, List<List<int>> b) {
  int az = min(a[0][2], a[0][2] + a[1][2]);
  int bz = min(b[0][2], b[0][2] + b[1][2]);
  return az.compareTo(bz);
}

bool canDisintegrate(var brick, var space) {
  for (int x = brick[0][0]; x <  brick[0][0] + brick[1][0]; x++) {
    for (int y = brick[0][1]; y < brick[0][1] + brick[1][1]; y++) {
      for (int z = brick[0][2]; z < brick[0][2] + brick[1][2]; z++) {
        if (isBlocked(space, x, y, z + 1) && getBlockIndexAt(space, x, y, z + 1) != brick[2][0]) { // get index
          return false;
        }
      }
    }
  }

  return true;
}

Set<int> getHeldBy(var brick, var space) {
  Set<int> heldBy = {};

  for (int x = brick[0][0]; x <  brick[0][0] + brick[1][0]; x++) {
    for (int y = brick[0][1]; y < brick[0][1] + brick[1][1]; y++) {
      for (int z = brick[0][2]; z < brick[0][2] + brick[1][2]; z++) {
        if (isBlocked(space, x, y, z - 1) && getBlockIndexAt(space, x, y, z - 1) != brick[2][0]) { // get index
         heldBy.add(getBlockIndexAt(space, x, y, z - 1));
        }
      }
    }
  }

  return heldBy;
}

Map<int, Set<int>> findHeldBy(var bricks, var space) {
  Map<int, Set<int>> heldMap = {};

  for (var brick in bricks) {
    heldMap[brick[2][0]] = getHeldBy(brick, space);
  }

  return heldMap;
}

Map<int, Set<int>> part1(var bricks, var space) {
  while (!fall(bricks, space));

  Map<int, Set<int>> heldBy = findHeldBy(bricks, space);

  int count = 0;

  for (var brick in bricks) {
    if (heldBy.values.every((element) => !element.contains(brick[2][0]) || element.length > 1)) {
      count++;
    }
  }

  print(count);

  return heldBy;
}

void part2(var bricks, Map<int, Set<int>> heldMap) {
  int sum = 0;

  for (var brick in bricks) {
    Set<int> destroyed = {brick[2][0]}; // index
    bool done = false;

    do {
      done = true;

      for (int bIndex in heldMap.keys) {
        if (destroyed.containsAll(heldMap[bIndex]!) && !destroyed.contains(bIndex)) {
          destroyed.add(bIndex);
          done = false;
        }
      }

    } while (!done);

    sum += (destroyed.length - 1);
  }

  print(sum);
}

void main() {
  List<List<List<int>>> bricks = File("22.input")
      .readAsLinesSync()
      .map((line) => line.split('~')
          .map((group) => group.split(',').map((s) => int.parse(s)).toList())
          .toList())
      .map((pair) => [
        pair[0],
        [
          pair[1][0] - pair[0][0] + 1,
          pair[1][1] - pair[0][1] + 1,
          pair[1][2] - pair[0][2] + 1,
        ],
      ])
      .toList();

  for (int i = 0; i < bricks.length; i++) {
    bricks[i].add([i]); // save index as single item list, ugly but...
  }

  bricks.sort((a, b) => brickCompare(a, b));

  var space = buildSpace(bricks);

  Map<int, Set<int>> heldMap = part1(bricks, space);

  part2(bricks, heldMap);
}