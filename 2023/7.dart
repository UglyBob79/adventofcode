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
  List<int> count = handCount(hand, handVals).where((element) => element != 0).toList();
  count.sort((a, b) => b.compareTo(a));

  return count.join('');
}

int calcScore(int handType, String hand) {
  int handScore = handType;

  hand.split('').map((c) => cardMap[c]!).forEach((c) {
    handScore <<= 8;
    handScore |= c;
  });

  return handScore;
}

int calcHandType(String hand) {
  List<int> handVals = hand.split('').map((c) => cardMap[c]!).toList();
  return handType[handSignature(hand, handVals)]!;
}

String replaceJokers(String hand, String card) {
  return hand.replaceAll('J', card);
}

int maxHandScore(int handType, String hand) {
  String newHand = hand;
  List<int> handVals = newHand.split('').map((c) => cardMap[c]!).toList();
  List<int> count = handCount(newHand, handVals);

  if (count[cardMap['J']!] > 0) {
    String handSig = handSignature(newHand, handVals);

    if (handSig == '5') {
      newHand = 'AAAAA';
    } else if (handSig == '41' || handSig == '32' || handSig == '11111') {
      newHand = replaceJokers(newHand, reverseCardMap[count.lastIndexWhere((element) => element != 0)]!);
    } else if (handSig == '311') {
      if (count.indexOf(3) == cardMap['J']) {
        newHand = replaceJokers(newHand, reverseCardMap[count.lastIndexWhere((element) => element != 0)]!);
      } else {
        newHand = replaceJokers(newHand, reverseCardMap[count.indexWhere((element) => element == 3)]!);
      }
    } else if (handSig == '221') {
      if (count.indexOf(1) == cardMap['J']) {
        newHand = replaceJokers(newHand, reverseCardMap[count.lastIndexWhere((element) => element != 0)]!);
      } else {
        newHand = replaceJokers(newHand, reverseCardMap[count.lastIndexWhere((element) => element == 2)]!);
      }
    } else if (handSig == '2111') {
      if (count.indexOf(1) == cardMap['J']) {
        newHand = replaceJokers(newHand, reverseCardMap[count.lastIndexWhere((element) => element == 2)]!);
      } else {
        newHand = replaceJokers(newHand, reverseCardMap[count.lastIndexWhere((element) => element != 0)]!);
      }
    }
  }

  return calcScore(calcHandType(newHand), hand);
}

void part(int part, List<Map<String, Object>> hands) {
  if (part == 2)
    cardMap['J'] = 1;

  hands.forEach((hand) {
    hand['score'] = (part == 1)
        ? calcScore(
            calcHandType((hand['hand'] as String)), (hand['hand'] as String))
        : maxHandScore(
            calcHandType((hand['hand'] as String)), (hand['hand'] as String));
  });
  hands.sort((a, b) => (a['score']! as int).compareTo((b['score']! as int)));

  int i = 1;

  var result = hands.fold(0, (val, hand) => val + (hand['bid'] as int) * i++);
  print(result);
}

void main() {
  List<String> data = new File("7.input")
      .readAsLinesSync()
      .toList();

  List<Map<String, Object>> hands = data
      .map((row) => row.split(' '))
      .map((hand) => {
            'hand': hand[0],
            'bid': int.parse(hand[1]),
            'score': 0
          })
      .toList();

  part(1, hands);
  part(2, hands);
}
