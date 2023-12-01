#!/usr/bin/env dart

import 'dart:io';

Map<String, String> numMap = {
  'one': '1',
  'two': '2',
  'three': '3',
  'four': '4',
  'five': '5',
  'six': '6',
  'seven': '7',
  'eight': '8',
  'nine': '9'
};

int calcCalib(List<String> data) {
  return data.map((str) {
    var nums = str.replaceAll(new RegExp(r'[^0-9]'), '');
    return nums[0] + nums[nums.length - 1];
  }).fold(0, (prev, curr) => prev + int.parse(curr));
}

String convert(String data) {
  String out = '';

  for (int i = 0; i < data.length; i++) {
    if (data.codeUnitAt(i) >= 48 && data.codeUnitAt(i) <= 57) {
      out += data[i];
    } else {
      numMap.forEach((key, value) {
        bool match = true;
        for (int j = 0; j < key.length; j++) {
            if (i + j >= data.length || data[i + j] != key[j]) {
                match = false;
                break;
            }
        }

        if (match) {
            out += value;
        }
      });
    }
  }

  return out;
}

void main() {
  List<String> data = new File("1.input").readAsLinesSync();

  print(calcCalib(data));

  List<String> convData = data.map((str) => convert(str)).toList();

  print(calcCalib(convData));
}
