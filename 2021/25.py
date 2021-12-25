#!/usr/bin/env python3
import copy

if __name__ == '__main__':
    with open("25.input") as file:
        ocean = [bytearray(row.strip(), 'utf-8') for row in file.readlines()]

        step = 0
        while True:
            moved = False
            next = copy.deepcopy(ocean)
            for y in range(len(ocean)):
                for x in range(len(ocean[0])):
                    if chr(ocean[y][x]) == '>':
                        if chr(ocean[y][(x + 1) % len(ocean[0])]) == '.':
                            next[y][x] = ord('.')
                            next[y][(x + 1) % len(ocean[0])] = ord('>')
                            moved = True

            ocean = copy.deepcopy(next)
            
            for x in range(len(ocean[0])):
                for y in range(len(ocean)):
                    if chr(ocean[y][x]) == 'v':
                        if chr(ocean[(y + 1) % len(ocean)][x]) == '.':
                            next[y][x] = ord('.')
                            next[(y + 1) % len(ocean)][x] = ord('v')
                            moved = True

            ocean = next
            step += 1

            if not moved:
                print(step)
                break
