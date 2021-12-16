#!/usr/bin/env python3
import binascii
from bitstring import BitStream
from functools import reduce
from operator import mul

verTot = 0

def decodeLiteral(header, s):
    more = 1
    v = 0
    while more:
        (more, d) = (s.read('uint:1'), s.read('uint:4'))
        v = (v << 4) | d
    return { 'header' : header, 'value' : v }

def decodeOperator(header, s):
    lenType = s.read('uint:1')
    length = s.read('uint:15') if lenType == 0 else s.read('uint:11')
    subPackets = []

    if lenType == 1:
        n = 0
        while n < length:
             subPackets.append(decodePacket(s))
             n += 1
    else:
        pos = s.pos
        while s.pos < pos + length:
            subPackets.append(decodePacket(s))

    return { 'header': header, 'lenType' : lenType, 'length' : length, 'sub' : subPackets}

def decodeHeader(s):
    return { 'version': s.read('uint:3'), 'type': s.read('uint:3') }

def decodePacket(s):
    global verTot
    header = decodeHeader(s)
    verTot += header['version']

    if header['type'] == 4:
        p = decodeLiteral(header, s)
    else:
        p = decodeOperator(header, s)

    return p

def evalPacket(packet):
    type = packet['header']['type']
    if type == 0:
        return sum([evalPacket(p) for p in packet['sub']])
    elif type == 1:
        return reduce(mul, [evalPacket(p) for p in packet['sub']])
    elif type == 2:
        return reduce(min, [evalPacket(p) for p in packet['sub']])
    elif type == 3:
        return reduce(max, [evalPacket(p) for p in packet['sub']])
    elif type == 4:
        return packet['value']
    elif type == 5:
        return 1 if evalPacket(packet['sub'][0]) > evalPacket(packet['sub'][1]) else 0
    elif type == 6:
        return 1 if evalPacket(packet['sub'][0]) < evalPacket(packet['sub'][1]) else 0
    elif type == 7:
        return 1 if evalPacket(packet['sub'][0]) == evalPacket(packet['sub'][1]) else 0

with open("16.input") as file:
    packet = decodePacket(BitStream(binascii.unhexlify(file.read().strip())))

    print(verTot)
    print(evalPacket(packet))
