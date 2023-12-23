#!/usr/bin/env dart

import 'dart:io';
import 'package:puzmat/puzmat.dart';
import '10.dart';
import 'package:collection/collection.dart';
import 'dart:collection';

int maxSteps = 0;

Map<Dir, List<int>> dMove = {
  Dir.north: [0, -1],
  Dir.south: [0, 1],
  Dir.west: [-1, 0],
  Dir.east: [1, 0]
};

Map<Dir, Dir> opDir = {
  Dir.north: Dir.south,
  Dir.south: Dir.north,
  Dir.west: Dir.east,
  Dir.east: Dir.west
};

void traverse(PuzMat map, var pos, int steps, var end) {
  if (!map.inBounds(pos[1], pos[0])) {
    return;
  }

  if (equal(pos, end)) {
    if (steps > maxSteps) {
      maxSteps = steps;
    }
    return;
  }

  map[3][pos[1]][pos[0]] = '0';

  for (var newPos in map.empty4Positions([1, 3], pos)) {
    if (map.isEmpty(2, newPos[1], newPos[0]) ||
        ((map[2][newPos[1]][newPos[0]] == '>' &&
                newPos[1] == pos[1] &&
                newPos[0] == pos[0] + 1) ||
            (map[2][newPos[1]][newPos[0]] == 'v' &&
                newPos[1] == pos[1] + 1 &&
                newPos[0] == pos[0]))) {
      traverse(map, newPos, steps + 1, end);
    }
  }

  map[3][pos[1]][pos[0]] = ' ';
}

class Node<T> {
  T data;
  Map<Node<T>, dynamic> edges;
  bool visited = false;

  Node(this.data) : edges = {};

  void addEdge(Node<T> destination, dynamic weight) {
    edges[destination] = weight;
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;

    if (other is Node<T>) {
      if (data is List && other.data is List) {
        // Compare lists element-wise
        List<dynamic> thisList = data as List<dynamic>;
        List<dynamic> otherList = other.data as List<dynamic>;

        if (thisList.length != otherList.length) {
          return false;
        }

        for (int i = 0; i < thisList.length; i++) {
          if (thisList[i] != otherList[i]) {
            return false;
          }
        }

        return true;
      } else {
        // Use default equality comparison for non-list data
        return data == other.data;
      }
    }

    return false;
  }

  bool isVisited() {
    return visited;
  }

  void setVisited(bool visited) {
    this.visited = visited;
  }

  @override
  String toString() {
    StringBuffer buffer = StringBuffer();
    buffer.writeln('  Node($data) {');

    edges.forEach((dest, weight) {
      buffer.writeln('    dest: ${dest.data}, steps: $weight');
    });

    buffer.writeln('  }');

    return buffer.toString();
  }
}

class Graph<T> {
  List<Node<T>> nodes;

  Graph() : nodes = [];

  Node addNode(T data) {
    Node<T> n = new Node(data);
    nodes.add(n);
    return n;
  }

  void addEdge(Node<T> source, Node<T> destination, dynamic weight) {
    if (nodes.contains(source) && nodes.contains(destination)) {
      source.addEdge(destination, weight);
      destination.addEdge(source, weight);
    }
  }

  Node<T>? findNode(T data) {
    return nodes.firstWhereOrNull((node) => _dataEquals(node.data, data));
  }

  bool _dataEquals(dynamic a, dynamic b) {
    if (a is List && b is List) {
      return ListEquality().equals(a, b);
    }
    return a == b;
  }

  @override
  String toString() {
    StringBuffer buffer = StringBuffer();
    buffer.writeln('Graph {');
    buffer.writeln('  nodes[${nodes.length}]:');

    for (Node n in nodes) {
      buffer.write(n.toString());
    }

    buffer.writeln('}');
    return buffer.toString();
  }
}

List<int> add(List<int> l1, List<int> l2) {
  return List.generate(l1.length, (index) => (l1[index] + l2[index]).toInt());
}

bool isCrossing(PuzMat map, List<int>pos) {
  return map.empty4Dirs([1], pos).length > 2;
}

Queue<List<dynamic>> queue = Queue<List<dynamic>>();

void findCrossings(PuzMat map, Graph graph, Node from, List<int> pos, Dir dir, int steps) {
  queue.add([from, pos, dir, steps]);

  while (queue.isNotEmpty) {
    var task = queue.removeFirst();
    Node from = task[0];
    List<int> pos = task[1];
    Dir dir = task[2];
    int steps = task[3];

    if (!map.inBounds(pos[1], pos[0])) {
      continue;
    }

    // already have been here?
    Node? n = graph.findNode(pos);
    if (n != null && n != from) {
      graph.addEdge(from, n, steps);
      continue;
    } else {
      if (isCrossing(map, pos)) {
        Node newNode = graph.addNode(pos);
        graph.addEdge(from, newNode, steps);
        steps = 0;
        from = newNode;
      }

      for (Dir nextDir in map.empty4Dirs([1], pos)) {
        if (nextDir != opDir[dir]) {
          var nextPos = add(pos, dMove[nextDir]!);
          queue.add([from, nextPos, nextDir, steps + 1]);
        }
      }
    }
  }
}

Graph<List<int>> generateGraph(PuzMat map, List<int> start, List<int> end) {
  Graph<List<int>> graph = new Graph();

  Node from = graph.addNode(start);
  graph.addNode(end);

  findCrossings(map, graph, from, start, Dir.south, 0);

  return graph;
}

void traverseGraph(Graph<List<int>> graph, Node curr, int steps, Node end) {
  if (curr == end) {
    if (steps > maxSteps) {
      maxSteps = steps;
    }
  }

  curr.setVisited(true);

  curr.edges.forEach((dest, dSteps) {
    if (!dest.visited) {
      traverseGraph(graph, dest, (steps + dSteps) as int, end);
    }
  });

  curr.setVisited(false);
}

void part1(PuzMat map) {
  List<int> start = [1, 0];
  List<int> end = [map.cols - 2, map.rows - 1];

  traverse(map, start, 0, end);

  print(maxSteps);
}

void part2(PuzMat map) {
  List<int> start = [1, 0];
  List<int> end = [map.cols - 2, map.rows - 1];

  map.clearLayer(3);

  var graph = generateGraph(map, start, end);

  maxSteps = 0;

  var startNode = graph.findNode(start)!;
  var endNode = graph.findNode(end)!;

  traverseGraph(graph, startNode, 0, endNode);

  print(maxSteps);
}

void main() {
  var map = PuzMat.mapLayersFromLayer(PuzMat<String>.fromFile(File('23.input'), ''), 0, [['.'], ['#'], ['>', 'v']], empty: ['.', ' ', ' ']);
  map.newLayer(' ', empty: ' ');
  map.setToStringMode(ToStringMode.overlay);

  part1(map);
  part2(map);
}