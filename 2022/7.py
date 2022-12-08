#!/usr/bin/env python3

def ls(curr, data):
    for d in data:
        for child in curr['children']:
            if d[1] == child['name']:
                continue

        if d[0] == 'dir':
            print("ls dir: " + d[1])
            dir = {'name': d[1], 'type': 'dir', 'children': [], 'parent': curr, 'size': 0}
            curr['children'].append(dir)
        else:
            file = {'name': d[1], 'type': 'file', 'children': None, 'parent': curr, 'size': int(d[0])}
            update_size(curr, file['size'])
            curr['children'].append(file)

def update_size(curr, size):
    curr['size'] += size
    if curr['parent']:
        update_size(curr['parent'], size)

def cd(fs, curr, path):
    if path == '/':
        return fs
    elif path == '..':
        if curr['parent']:
            return curr['parent']
        else:
            return curr
    else:
        for child in curr['children']:
            if child['name'] == path:
                return child

        dir = {'name': path, 'type': 'dir', 'children': [], 'parent': curr, 'size': 0}
        curr['children'].append(dir)
        return dir

def print_dir(curr, offset):
    print(offset + '- ' + curr['name'] + ' (dir, size=%d)' % curr['size'])

    for child in curr['children']:
        if child['type'] == 'dir':
            print_dir(child, offset + '  ')
        else:
            print(offset + '  - ' + child['name'] + ' (file, size=%d)' % child['size'])

tot_sum = 0

def find_sum(curr):
    global tot_sum

    if curr['size'] <= 100000:
        tot_sum += curr['size']

    for child in curr['children']:
        if child['type'] == 'dir':
            find_sum(child)

    return tot_sum

found = []
def find_del(curr, min_size):
    global found

    if curr['size'] >= min_size:
        found.append(curr)

    for child in curr['children']:
        if child['type'] == 'dir':
            find_del(child, min_size)

    return found

def traverse(data):
    fs = {'name': '/', 'type': 'dir', 'children': [], 'parent': None, 'size': 0}
    curr = fs
    ls_data = []

    for line in data:
        if line.startswith('$'):
            if ls_data:
                ls(curr, ls_data)
                ls_data = []
            if line.startswith('$ cd'):
                curr = cd(fs, curr, line.split(' ')[2])
            elif line.startswith('$ ls'):
                ls_data = []
        else:
            ls_data.append(line.split(' '))

    if ls_data:
        ls(curr, ls_data)

    return fs

with open("7.input") as file:
    data = file.read().splitlines()

    fs = traverse(data)

    print_dir(fs, '')
    print()

    print(find_sum(fs))

    found = find_del(fs, 30000000 - (70000000 - fs['size']))
    print(min([f['size'] for f in found]))
