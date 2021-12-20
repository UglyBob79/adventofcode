#!/usr/bin/env python3
from bitarray import bitarray

def printImg(img):
    for row in img:
        print(''.join([chr(9608) if b == 1 else ' ' for b in row]))

def enhance(data, steps):
    size = (len(data[0]), len(data))
    cSize = (size[0] + 2 * (2 * steps + 2), size[1] + 2 * (2 * steps + 2))
    offset = ((cSize[0] - size[0]) // 2, (cSize[1] - size[1]) // 2)

    img = []
    for y in range(cSize[1]):
        if y < offset[1]:
            img.append(bitarray('0' * cSize[0]))
        elif 0 <= y - offset[1] < size[1]:
            img.append(bitarray('0' * offset[0] + data[y - offset[1]] + '0' * (cSize[0] - offset[0] - size[0])))
        else:
            img.append(bitarray('0' * cSize[0]))

    for step in range(steps):
        imgNext = [bitarray('0' * len(img[0])) for i in range(len(img))]
        for y in range(step + 3, cSize[1] - step - 3):
            for x in range(step + 3, cSize[0] - step - 3):
                b = img[y - 1][x - 1:x + 2] + img[y][x - 1:x + 2] + img[y + 1][x - 1:x + 2]
                v = int(b.to01(), 2)
                imgNext[y][x] = algo[int(b.to01(), 2)]
        img = imgNext
    
    return img

with open("20.input") as file:
    algo = bitarray(''.join(['1' if b == '#' else '0' for b in file.readline().strip()]))
    file.readline()
    data = [''.join(['1' if b == '#' else '0' for b in row]) for row in file.read().splitlines()]

    img = enhance(data, 2)
    count = sum([sum(b) for b in img])
    print(count)

    img = enhance(data, 50)
    count = sum([sum(b) for b in img])
    print(count)
