#!/usr/bin/env dart

import 'dart:io';
import 'dart:collection';

import 'package:collection/collection.dart';

class Edge {
  final List<Node> nodes = [];
  bool _active = true;
  double _weight = 0;

  Edge(Node n1, Node n2) {
    nodes.add(n1);
    nodes.add(n2);
    n1.addEdge(this);
    n2.addEdge(this);
  }

  bool get isActive => _active;

  void set active(bool active) => _active = active;

  double get weight => _weight;

  void set weight(double weight) => _weight = weight;

  @override
  String toString() {
    return '${nodes[0].name}-${nodes[1].name}: ${weight}';
  }
}

class Node {
  final String name;
  final List<Edge> edges = [];

  Node(String name): this.name = name;

  void addEdge(Edge edge) {
    edges.add(edge);
  }

  void removeEdge(Edge edge) {
    edges.remove(edge);
  }

  Set<Node> get neighbors {
    return edges.expand((edge) => edge.nodes.where((node) => node != edge)).toSet();
  }

  @override
  String toString() {
    StringBuffer buffer = StringBuffer();
    buffer.writeln('  Node($name) {');
    buffer.writeln('  edges:');
    edges.forEach((edge) { '    $edge'; });
    buffer.writeln('  }');

    return buffer.toString();
  }
}

class Graph {
  final Map<String, Node> nodes = {};
  final List<Edge> edges = [];

  Node newOrOldNode(String name) => nodes.putIfAbsent(name, () => new Node(name));

  void addEdge(Edge edge) => edges.add(edge);

  bool nodeExist(String name) {
    return nodes[name]  != null;
  }

  void connect(String name1, String name2) {
    Node n1 = newOrOldNode(name1);
    Node n2 = newOrOldNode(name2);

    addEdge(Edge(n1, n2));
  }

  Edge? findEdge(String name1, String name2) {
    return edges.firstWhereOrNull((edge) =>
        (edge.nodes[0].name == name1 && edge.nodes[1].name == name2) ||
        (edge.nodes[0].name == name2 && edge.nodes[1].name == name1));
  }

  /// calc betweeness (importance of edges) using Brandes's algorithm
  void calcBetweenness() {
    for (var edge in edges) {
      edge.weight = 0.0;
    }

    for (var node in nodes.values) {
      var stack = <Node>[];
      var predecessors = <Node, List<Node>>{};
      var sigma = <Node, double>{};
      var delta = <Node, double>{};

      var queue = <Node>[];
      var dist = <Node, int>{};

      for (var vertex in nodes.values) {
        predecessors[vertex] = [];
        sigma[vertex] = 0.0;
        delta[vertex] = 0.0;
        dist[vertex] = -1;
      }

      sigma[node] = 1.0;
      dist[node] = 0;

      queue.add(node);

      while (queue.isNotEmpty) {
        var current = queue.removeAt(0);
        stack.add(current);

        for (var neighbor in current.neighbors) {
          if (dist[neighbor]! < 0) {
            queue.add(neighbor);
            dist[neighbor] = dist[current]! + 1;
          }

          if (dist[neighbor] == dist[current]! + 1) {
            sigma[neighbor] = sigma[neighbor]! + sigma[current]!;
            predecessors[neighbor]!.add(current);
          }
        }
      }

      while (stack.isNotEmpty) {
        var current = stack.removeLast();
        for (var predecessor in predecessors[current]!) {
          var ratio = sigma[predecessor]! / sigma[current]!;
          delta[predecessor] = delta[predecessor]! + ratio * (1 + delta[current]!);
        }

        if (current != node) {
          for (var incidentEdge in current.edges) {
            incidentEdge.weight += delta[current]! / 2;
          }
        }
      }
    }
  }

  @override
  String toString() {
    StringBuffer buffer = StringBuffer();
    buffer.writeln('Graph {');
    nodes.values.forEach((node) { buffer.write(node.toString()); });
    buffer.writeln('}');

    return buffer.toString();
  }
}

void writeToGraphviz(Graph graph, String filename) async {
  StringBuffer buffer = new StringBuffer();
  buffer.writeln('digraph {');

  for (var node in graph.nodes.values) {
    for (var edge in node.edges) {
      if (!edge.isActive)
        continue;

      var dest = edge.nodes[0] != node ? edge.nodes[0] : edge.nodes[1];
      buffer.writeln('  ${node.name} -> ${dest.name};');
    }
  }

  buffer.writeln('}');

  // Write the DOT string to a file
  File dotFile = File('$filename.dot');
  dotFile.writeAsStringSync(buffer.toString());

  // Generate PNG image using Graphviz's neato command
  Process.runSync('neato', ['-Tpng', '-o$filename.png', dotFile.path]);
}

List<int> countSubComponents(Graph graph) {
  List<int> count = [];
  Set<Node> notVisited = graph.nodes.values.toSet();

  while (notVisited.isNotEmpty) {
    Set<Node> visited = {};
    count.add(countComponents(graph, visited, notVisited.first));
    notVisited.removeAll(visited);
  }

  return count;
}

int countComponents(Graph graph,  Set<Node> visited, Node start) {
  Queue<Node> queue = Queue<Node>();
  int count = 0;

  queue.add(start);

  while (queue.isNotEmpty) {
    Node curr = queue.removeFirst();

    if (visited.contains(curr)) {
      continue;
    } else {
      visited.add(curr);
      count++;
    }

    for (var edge in curr.edges) {
      if (edge.isActive) {
        var dest = edge.nodes[0] != curr ? edge.nodes[0] : edge.nodes[1];
        queue.add(dest);
      }
    }
  }

  return count;
}

void part1(Graph graph) {
  graph.calcBetweenness();

  List<Edge> edgeList = graph.edges.toList()
    ..sort((a, b) => b.weight.compareTo(a.weight));

  for (var edge in edgeList.take(3)) {
    edge.active = false;
  }

  print(countSubComponents(graph).reduce((value, element) => value * element));
}

void main() {
  List<List<List<String>>> data = File("25.input")
      .readAsLinesSync()
      .map((line) => line.split(': ')
          .map((group) => group.split(' '))
          .toList())
      .toList();

  Graph compsGraph = new Graph();

  for (var row in data) {
    var from = row[0][0];
    for (var dest in row[1]) {
      compsGraph.connect(from, dest);
    }
  }

  part1(compsGraph);
}