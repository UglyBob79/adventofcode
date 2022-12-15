#!/usr/bin/env python3

import os

ROOT = '/tmp/aoc'

def make_fs(data):
    try:
        os.rmdir(ROOT)
    except OSError:
        pass

    try:
        os.mkdir(ROOT)
    except FileExistsError:
        pass

    os.chroot(ROOT)

    for line in data:
        if line.startswith('$ cd'):
            path = line.split(' ')[2]
            try:
                os.chdir(path)
            except FileNotFoundError:
                os.makedirs(path)
                os.chdir(path)
        elif line.startswith('$ ls'):
            pass
        elif line.startswith('dir'):
            path = line.split(' ')[1]
            try:
                os.mkdir(path)
            except FileExistsError:
                pass
        else:
            (size, filename) = line.split(' ')
            f = open(filename, 'wb')
            f.seek(int(size) - 1)
            f.write(b'\0')
            f.close()

def find_dirs(path, dirs):
    total = 0

    for entry in os.scandir(path):
        if entry.is_file():
            total += entry.stat().st_size
        elif entry.is_dir():
            total += find_dirs(entry.path, dirs)

    dirs.append((path, total))
    return total

with open("7.input") as file:
    data = file.read().splitlines()

    make_fs(data)

    dirs = []
    find_dirs('/', dirs)

    print(sum([dir[1] for dir in dirs if dir[1] <= 100000]))