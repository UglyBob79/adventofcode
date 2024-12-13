#!/usr/bin/env python3
move_map = {
    '>': (1, 0),
    'v': (0, 1),
    '<': (-1, 0),
    '^': (0, -1)
}

def add(pos, delta):
    return (pos[0] + delta[0], pos[1] + delta[1])

def is_wall(map, pos):
    return map['walls'][pos[1]][pos[0]]

def is_box(map, pos):
    return map['boxes'][pos[1]][pos[0]] != 0

def print_map(map, player):
    for y in range(len(map['walls'])):
        for x in range(len(map['walls'][0])):
            if map['walls'][y][x] == 1:
                print('#', end='')
            elif map['boxes'][y][x] != 0:
                print(map['boxes'][y][x], end='')
            elif x == player[0] and y == player[1]:
                print('@', end='')
            else:
                print('.', end='')
        print('')

def count_gps(map):
    total = 0
    for y in range(len(map['boxes'])):
        for x in range(len(map['boxes'][0])):
            if map['boxes'][y][x] == 1 or map['boxes'][y][x] == '[':
                total += 100 * y + x
    return total

def convert_map(map):
    new_map = {'walls': [], 'boxes': []}

    for y in range(len(map['boxes'])):
        walls = []
        boxes = []
        for x in range(len(map['boxes'][0])):
            if map['walls'][y][x] == 1:
                walls.extend([1, 1])
                boxes.extend([0, 0])
            elif map['boxes'][y][x] == 1:
                walls.extend([0, 0])
                boxes.extend(['[', ']'])
            else:
                walls.extend([0, 0])
                boxes.extend([0, 0])
        new_map['walls'].append(walls)
        new_map['boxes'].append(boxes)

    return new_map

def move_box(map, pos, dir):
    if dir == (0, 1) or dir == (0, -1):
        box = get_box(map, pos)
        for p in box:
            new_pos = add(p, dir)
            map['boxes'][new_pos[1]][new_pos[0]] = map['boxes'][p[1]][p[0]]
            map['boxes'][p[1]][p[0]] = 0
    else:
        new_pos = add(pos, dir)
        map['boxes'][new_pos[1]][new_pos[0]] = map['boxes'][pos[1]][pos[0]]
        map['boxes'][pos[1]][pos[0]] = 0

def get_box(map, pos):
    if not is_box(map, pos):
        return None
    elif map['boxes'][pos[1]][pos[0]] == '[':
        return (pos, add(pos, (1, 0)))
    elif map['boxes'][pos[1]][pos[0]] == ']':
        return (add(pos, (-1, 0)), pos)
    else:
        return [pos]

def can_move(map, pos, dir):
    if is_wall(map, pos):
        return False
    elif is_box(map, pos):
        if dir == (0, 1) or dir == (0, -1):
            box = get_box(map, pos)
            return all(can_move(map, add(p, dir), dir) for p in box)
        else:
            return can_move(map, add(pos, dir), dir)
    else:
        return True

def push(map, pos, dir):
    if is_wall(map, pos):
        return
    elif is_box(map, pos):
        if dir == (0, 1) or dir == (0, -1):
            box = get_box(map, pos)
            any(push(map, add(p, dir), dir) for p in box)
        else:
            push(map, add(pos, dir), dir)
        move_box(map, pos, dir)

def move_char(map, dir, pos):
    if can_move(map, add(pos, dir), dir):
        push(map, add(pos, dir), dir)
        return add(pos, dir)
    else:
        return pos

def traverse(map, moves, pos, visualize=False):
    if visualize:
        print_map(map, pos)
    for move in moves:
        if visualize:
            print("Move: ", move)
            input()
        pos = move_char(map, move_map[move], pos)
        if visualize:
            print_map(map, pos)

    return count_gps(map)

with open("15.input") as file:
    map = {'walls': [], 'boxes': []}
    player = (None, None)

    for y, line in enumerate(file):
        line = line.strip()
        if not line:
            break
        row_walls = [1 if char == '#' else 0 for char in line]
        row_boxes = [1 if char == 'O' else 0 for char in line]

        if '@' in line:
            x = line.index('@')
            player = (x, y)

        map['walls'].append(row_walls)
        map['boxes'].append(row_boxes)

    moves = [char for line in file if line.strip() for char in line.strip()]
    map_wide = convert_map(map)

    print(traverse(map, moves, player))
    print(traverse(map_wide, moves, (player[0] * 2, player[1])))
