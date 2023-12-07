#!/usr/bin/env dart

import 'dart:io';

Map<String, int> cardMap = {
  'A': 14,
  'K': 13,
  'Q': 12,
  'J': 11,
  'T': 10,
  '9': 9,
  '8': 8,
  '7': 7,
  '6': 6,
  '5': 5,
  '4': 4,
  '3': 3,
  '2': 2
};

Map<int, String> reverseCardMap = Map.fromEntries(
    cardMap.entries.map((entry) => MapEntry(entry.value, entry.key)));

Map<String, int> handType = {
  '11111': 1,
  '2111': 2,
  '221': 3,
  '311': 4,
  '32': 5,
  '41': 6,
  '5': 7
};

List<int> handCount(String hand, List<int> handVals) {
  List<int> count = List<int>.filled(15, 0);

  hand.split('').map((c) => cardMap[c]).forEach((c) => count[c!]++);

  return count;
}

String handSignature(String hand, List<int> handVals) {
  List<int> count = handCount(hand, handVals).where((element) => element != 0).toList()..sort((a, b) => b.compareTo(a));
  return count.join('');
}

int calcHandType(String hand) {
  String handSig =
      (handCount(hand, hand.split('').map((c) => cardMap[c]!).toList())
              .where((element) => element != 0)
              .toList()
            ..sort((a, b) => b.compareTo(a)))
          .join();

  return handType[handSig]!;
}

int calcScore(int handType, String hand, { bool jokers = false }) {
  String newHand = hand;

  if (jokers) {
    List<int> handVals = newHand.split('').map((c) => cardMap[c]!).toList();
    List<int> count = handCount(newHand, handVals);

    int jokers = count[cardMap['J']!];

    if (jokers > 0) {
      count[cardMap['J']!] = 0;
      int highest = count.lastIndexOf(count.reduce((value, element) => value > element ? value : element));

      newHand = newHand.replaceAll('J', reverseCardMap[highest]!);
    }
  }

  int handScore = calcHandType(newHand);

  hand.split('').map((c) => cardMap[c]!).forEach((c) {
    handScore <<= 8;
    handScore |= c;
  });

  return handScore;
}

void part(int part, List<Map<String, Object>> hands) {
  if (part == 2)
    cardMap['J'] = 1;

  hands..forEach((hand) {
      hand['score'] = calcScore(
          calcHandType((hand['hand'] as String)), (hand['hand'] as String),
          jokers: part == 2);
    })..sort((a, b) => (a['score']! as int).compareTo((b['score']! as int)));

  int i = 1;

  var result = hands.fold(0, (val, hand) => val + (hand['bid'] as int) * i++);
  print(result);
}

void main() {
  List<Map<String, Object>> hands = new File("7.input")
      .readAsLinesSync()
      .map((row) => row.split(' '))
      .map((hand) => {'hand': hand[0], 'bid': int.parse(hand[1]), 'score': 0})
      .toList();

  part(1, hands);
  part(2, hands);
}
