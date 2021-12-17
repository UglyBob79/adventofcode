#!/usr/bin/env python3
import re

required = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

with open("4.input") as file:
    data = [row.strip() for row in file.readlines()]

    passports = []
    passport = {}
    for i, row in enumerate(data):
        if row:
            for k, v in [entry.split(':') for entry in row.split(' ')]:
                passport[k] = v
        if not row or i == len(data) - 1:
            passports.append(passport)
            passport = {}
            continue

    valids1 = 0
    valids2 = 0
    for passport in passports:
        valid = True
        for r in required:
            if not r in passport:
                valid = False
                break
        if valid:
            valids1 += 1
            if 1920 <= int(passport['byr']) <= 2002:
                if 2010 <= int(passport['iyr']) <= 2020:
                    if 2020 <= int(passport['eyr']) <= 2030:
                        unit = passport['hgt'][-2:]
                        if unit == 'cm' and 150 <= int(passport['hgt'][:-2]) <= 193 or unit == 'in' and 59 <= int(passport['hgt'][:-2]) <= 76:
                            if re.match('#[0-9a-f]{6}', passport['hcl']):
                                if passport['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
                                    if len(passport['pid']) == 9 and passport['pid'].isnumeric():
                                        valids2 += 1

    print(valids1)
    print(valids2)
