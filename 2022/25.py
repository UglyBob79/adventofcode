#!/usr/bin/env python3

import math

SNAFU_DIGITS = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

def dec2snafu(dec):
    dig = None
    val = 1
    max_val = 0
    pos = 0

    while True:
        diff = dec
        for d in SNAFU_DIGITS:
            if abs(dec - val * SNAFU_DIGITS[d]) < abs(diff):
                diff = dec - val * SNAFU_DIGITS[d]
                dig = d
        if abs(diff) < max_val:
            break

        pos += 1
        max_val += 2 * val
        val *= 5

    snafu = [dig] + [' '] * pos
    rest = diff

    val = math.pow(5, pos - 1)

    for i in range(1, pos + 1):
        dig = None
        diff = rest

        for d in SNAFU_DIGITS:
            if abs(rest - val * SNAFU_DIGITS[d]) <= abs(diff):
                diff = rest - val * SNAFU_DIGITS[d]
                dig = d

        rest = diff
        snafu[i] = dig
        val //= 5

    return ''.join(snafu)

def snafu2dec(snafu):
    v = 1
    dec = 0

    for s in reversed(snafu):
        dec += v * SNAFU_DIGITS[s]
        v *= 5

    return dec

with open('25.input') as file:
    snafus = file.read().splitlines()

    print(dec2snafu(sum([snafu2dec(snafu) for snafu in snafus])))