#!/usr/bin/env dart

import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';

class Connector {
  bool? signal = null;
  Connector? conn;
  Circuit owner;

  Connector(Circuit owner): this.owner = owner;

  void setSignal(bool signal) {
    if (signal) {
      highCount++;
    } else {
      lowCount++;
    }

    this.signal = signal;

    //print("setSignal: $signal ($owner)");
  }

  bool? getSignal() {
    bool? retVal = signal;
    signal = null;
    return retVal;
  }

  void connect(Connector conn) {
    this.conn = conn;
  }

  void reset() {
    signal = null;
  }

  @override
  String toString() {
    String dest = conn != null ? conn!.owner.name : '-';
    return 'Connector { conn: $dest, signal: $signal }';
  }
}

abstract class Circuit {
  final String name;
  List<Connector> inputs = [];
  List<Connector> outputs = [];

  Circuit(String name)
      : name = name;

  Connector newOutput() {
    Connector output = new Connector(this);
    outputs.add(output);
    return output;
  }

  Connector newInput() {
    Connector input = new Connector(this);
    inputs.add(input);
    return input;
  }

  void connect(Circuit inCircuit) {
    Connector input = newInput();
    Connector output = inCircuit.newOutput();

    input.connect(output);
    output.connect(input);
  }

  void setAllOutputs(bool signal) {
    for (var output in outputs) {
      output.setSignal(signal);
    }
  }

  bool propagate() {
    bool stable = true;

    for (var output in outputs) {
      bool? signal = output.getSignal();

      if (signal != null) {
        // don't use setSignal, we don't want it counted
        output.conn!.signal = signal;
        stable = false;
      }
    }

    return stable;
  }

  void reset() {
    inputs.forEach((input) { input.reset(); });
    outputs.forEach((output) { output.reset(); });
  }

  String getType();

  void process();


  @override
  String toString() {
    return '\n${getType()} {\n  name: $name,\n  in: $inputs,\n  out: $outputs }\n';
  }
}

class Broadcaster extends Circuit {

  Broadcaster(String name) : super(name);

  @override
  String getType() {
    return 'Broadcast';
  }

  void process() {
      bool? s = inputs[0].getSignal();

      if (s != null) {
        setAllOutputs(s);
      }
  }
}

class FlipFlop extends Circuit {

  bool on = false;

  FlipFlop(String name) : super(name);

  @override
  String getType() {
    return 'FlipFlop';
  }

  void process() {
    for (var input in inputs) {
      bool? s = input.getSignal();

      if (s != null) {
        if (!s) {
          on = !on;
          setAllOutputs(on);
        }
      }
    }
  }

  @override
  void reset() {
    super.reset();
    on = false;
  }
}

class Conjunction extends Circuit {

  List<bool> states = [];

  Conjunction(String name) : super(name);

  @override
  String getType() {
    return 'Conjunction';
  }

  @override
  void connect(Circuit inCircuit) {
    super.connect(inCircuit);
    states.add(false);
  }

  void process() {
    for (int i = 0; i < inputs.length; i++) {
      bool? s = inputs[i].getSignal();

      if (s != null) {
        states[i] = s;
        setAllOutputs(!states.every((element) => element == true));
      }
    }
  }

  @override
  void reset() {
    states.forEach((s) { s = false; });
  }
}

class Button extends Circuit {

  Button(String name) : super(name);

  @override
  String getType() {
    return 'Button';
  }

  void push() {
    outputs[0].setSignal(false);
  }

  void process() {
    // nothing to do
  }
}

class Output extends Circuit {

  Output(String name) : super(name);

  @override
  String getType() {
    return 'Output';
  }

  void process() {
    // nothing to do
  }
}

String getName(String cfgName) {
  if (cfgName == 'broadcaster') {
    return cfgName;
  } else {
    return cfgName.substring(1);
  }
}

int gcd(int a, int b) {
  while (b != 0) {
    var temp = b;
    b = a % b;
    a = temp;
  }
  return a;
}

int lcm(int a, int b) {
  return (a * b) ~/ gcd(a, b);
}

int lcmOfList(List<int> periods) {
  var result = periods.first;
  for (var period in periods.skip(1)) {
    result = lcm(result, period);
  }

  return result;
}

int lowCount = 0;
int highCount = 0;

List<bool>? lastNsStates;
List<int>? lastNsToggles;
int result = 0;

int simulate(Map<String, Circuit> circuits, int presses, bool solveCycles) {
  for (int i = 1; i <= presses; i++) {
    (circuits['button'] as Button).push();

    bool stable = false;

    while (!stable) {
      stable = true;

      for (var circuit in circuits.keys) {
        circuits[circuit]!.process();
      }

      for (var circuit in circuits.keys) {
        if (!circuits[circuit]!.propagate()) {
          stable = false;
        }
      }

      if (solveCycles) {
        Conjunction ns = (circuits['ns'] as Conjunction);
        List<bool> nsStates = ns.states;

        if (lastNsToggles == null) {
          lastNsToggles = List.filled(nsStates.length, 0);
        }

        for (int j = 0; j < nsStates.length; j++) {
          if (nsStates[j] == true && (lastNsStates == null || lastNsStates![j] == false)) {
            int diff = i - lastNsToggles![j];
            lastNsToggles![j] = diff;

            if (lastNsToggles!.every((element) => element > 0)) {
              return lcmOfList(lastNsToggles!);
            }
          }
        }
        lastNsStates = List.of(nsStates);
      }
    }
  }

  return lowCount * highCount;
}

void part1(Map<String, Circuit> circuits) {
  print(simulate(circuits, 1000, false));
}

void part2(Map<String, Circuit> circuits) {
  print(simulate(circuits, 1000000, true));
}

void writeToGraphviz(Map<String, Circuit> circuits) async {
  StringBuffer buffer = new StringBuffer();
  buffer.writeln('digraph {');

  for (var circuitName in circuits.keys) {
    var circuit = circuits[circuitName]!;

    for (var out in circuit.outputs) {
      buffer.writeln('  $circuitName -> ${out.conn!.owner.name};');
    }
  }

  buffer.writeln('}');

  // Write the DOT string to a file
  File dotFile = File('20.dot');
  dotFile.writeAsStringSync(buffer.toString());

  // Generate PNG image using Graphviz's dot command
  Process.runSync('dot', ['-Tpng', '-o20.png', dotFile.path]);
}

void main() {
  List<String> data = new File("20.input")
      .readAsLinesSync()
      .toList();

  Map<String, Circuit> circuits = {};

  Map<String, List<String>> config = {};

  for (var line in data) {
    var [input, outRaw] = line.split(' -> ');
    var outputs = outRaw.split(',').map((e) => e.trim()).toList();

    config[input] = outputs;
  }

  for (var cfg in config.keys) {
    if (cfg == 'broadcaster') {
      Broadcaster bc = new Broadcaster(cfg);
      circuits[cfg] = bc;
      Button b = new Button('button');
      circuits[b.name] = b;
      bc.connect(b);
    } else if (cfg.startsWith('%')) {
      circuits[getName(cfg)] = new FlipFlop(getName(cfg));
    } else if (cfg.startsWith('&')) {
      circuits[getName(cfg)] = Conjunction(getName(cfg));
    }
  }

  for (var input in config.keys) {
    var outputs = config[input]!;
    for (var output in outputs) {
      String name = getName(input);
      if (!circuits.containsKey(output)) {
        circuits[output] = Output(output);
      }
      circuits[output]!.connect(circuits[name]!);
    }
  }

  part1(circuits);
  circuits.values.forEach((circuit) { circuit.reset(); });
  writeToGraphviz(circuits);
  part2(circuits);
}