#!/usr/bin/env python3

import os

EMPTY_ROW = [c for c in '.......']

# upside down shapes are easier...I think...
shapes = [
    ['####'],
    ['.#.',
     '###',
     '.#.'],
    ['###',
     '..#',
     '..#'],
    ['#',
     '#',
     '#',
     '#'],
    ['##',
     '##']
]

DEBUG_X_OFFSET = 20
DEBUG_Y_OFFSET = 10

debug_on = True
debug_list = []

def debug(str):
    debug_list.append(str)

def get_height(world):
    for i in range(len(world)):
        if world[i] == EMPTY_ROW:
            return i
    return len(world)

def get_free_height(world):
    return len(world) - get_height(world)

def extend_world(world, height):
    for _ in range(height):
        world.append(EMPTY_ROW.copy())

def raster_object(world, object):
    for y, row in enumerate(object['shape']):
        for x, c in enumerate(row):
            wx = object['x'] + x
            wy = object['y'] + y

            if c == '#':
                world[wy][wx] = c

def check_collision(world, object):
    #print("check_collision (x:", object['x'], "y:", object['y'], ")")
    # out of bounds?
    if object['x'] < 0 or object['x'] + len(object['shape'][0]) > len(world[0]) or object['y'] < 0:
        #print("out of bounds")
        return True

    for y, row in enumerate(object['shape']):
        for x, c in enumerate(row):
            wx = object['x'] + x
            wy = object['y'] + y
            #print(wx, wy, c)

            if object['shape'][y][x] == '#' and world[wy][wx] != '.':
                return True

    return False

def blow(world, object, wind):
    #print("blow", wind)
    delta = {'<': -1, '>': 1}[wind]
    object['x'] += delta

    if check_collision(world, object):
        debug("Blow collision at (%d, %d)" % (object['x'], object['y']))
        object['x'] -= delta

def fall(world, object):
    #print("fall")
    object['y'] -= 1

    if check_collision(world, object):
        debug("Fall collision at (%d, %d)" % (object['x'], object['y']))
        object['y'] += 1
        raster_object(world, object)
        return False

    return True

def update(world, object, wind):
    blow(world, object, wind)

    return fall(world, object)

def draw_world(world, object, wind, count, break_at=None):
    os.system('cls' if os.name == 'nt' else 'clear')

    size = os.get_terminal_size()
    y_len = size.lines - 2

    if object:
        o_xr = range(object['x'], object['x'] + len(object['shape'][0]))
        o_yr = range(object['y'], object['y'] + len(object['shape']))

    for sy in range(size.lines - 2): # space for input
        y = len(world) - 1 - sy
        if y >= 0:
            row = '|'
            for x in range(len(world[y])):
                if object and x in o_xr and y in o_yr and object['shape'][y - object['y']][x - object['x']] == '#':
                    row += '@'
                else:
                    row += world[y][x]
            row += '|'

            if sy == 0 and wind is not None:
                row += ' Wind: ' + wind

            if debug_on:
                dbg_pos = len(debug_list) - y_len - DEBUG_Y_OFFSET + sy
                if sy >= DEBUG_Y_OFFSET and dbg_pos in range(len(debug_list)):
                    row += DEBUG_X_OFFSET * ' ' + debug_list[dbg_pos]

            print(row)
    if len(world) < size.lines - 2:
        print('+-------+')

    print('Count: ' + str(count) + ' Height: ' + str(get_height(world)), end='')
    if break_at is not None and count >= break_at:
        input()
    else:
        print('\n')

def find_repeat(world):
    match = True
    for i in range(len(world) // 2):
        debug("compare %s == %s" % (world[i], world[i + (len(world) // 2)]))
        if world[i] != world[i + (len(world) // 2)]:
            match = False
            break
    if match:
        input("REPEAT")
        debug("Found repeat of count %d height %d" % (len(world) // 2, get_height(world) // 2))

def simulate(wind, count, visualize=False, break_at=None):
    world = []
    w = 0
    shape_idx = 0

    for shape_idx in range(count):
        object = {
            'shape': shapes[shape_idx % len(shapes)],
            'x': 2,
            'y': get_height(world) + 3
        }

        extend_world(world, (object['y'] + len(object['shape'])) - len(world))

        curr_wind = None
        while True:
            if visualize:
                draw_world(world, object, curr_wind, shape_idx + 1, break_at)
            curr_wind = wind[w % len(wind)]
            w += 1
            if not update(world, object, curr_wind):
                #find_repeat(world)
                break
        if visualize:
            draw_world(world, None, curr_wind, shape_idx + 1, break_at)

    return get_height(world)

with open('17.example') as file:
    wind = file.read().strip()


    skip_a = False
    skip_b = True

    if not skip_a:
        print(simulate(wind, 2022, True))

    if not skip_b:
            # len shapes is 5
            # common denominator is 5 * 10091 = 50445
            # repeat height 79739
            # repeat count 50445
            # goal count 1000000000000
            # repeated count 19823570
            # repeated height 1580711648230
            # rest count 13345
            # rest height 21080
            # total height

        # goal_count = 1000000000000
        # wind_len = len(wind)
        # shapes_len = len(shapes)
        # repeat_len = wind_len * shapes_len
        # repeat_multi = goal_count // repeat_len
        # repeat_count = repeat_multi * repeat_len
        # repeat_rest = goal_count - repeat_count
        # repeat_height = 79739
        # repeated_height = repeat_height * repeat_multi
        # rest_height = 21080
        # total_height = repeated_height + rest_height

        # print("wind len:", wind_len)
        # print("shapes len:", shapes_len)
        # print("repeat len: ", repeat_len)
        # print("repeat_multi:", repeat_multi)
        # print("repeat_count:", repeat_count)
        # print("repeat_rest:", repeat_rest)
        # print("repeat_height:", repeat_height)
        # print("repeated_height:", repeated_height)
        # print("total_height:", total_height)
        # input("ENTER")

        simulate(wind, 300, True, 40)

        goal_count = 1000000000000
        wind_len = len(wind)
        shapes_len = len(shapes)
        repeat_len = shapes_len * wind_len
        repeat_multi = goal_count // repeat_len
        repeat_count = repeat_multi * repeat_len
        repeat_rest = goal_count - repeat_count

        print("goal count: ", goal_count)
        print("wind len:", wind_len)
        print("shapes len:", shapes_len)
        print("repeat len: ", repeat_len)
        print("repeat_multi:", repeat_multi)
        print("repeat_count:", repeat_count)
        print("repeat_rest:", repeat_rest)

        skip_repeat = False

        if not skip_repeat:
            repeat_height = simulate(wind, repeat_len, True, 30)
            print("repeat height:" + str(repeat_height))


        rest_height = simulate(wind, repeat_rest, True)
        print("rest height:" + str(rest_height))


        #repeat_height = 79739
        repeated_height = repeat_height * repeat_multi
        #rest_height = 21080
        total_height = repeated_height + rest_height


        print("repeat_height:", repeat_height)
        print("repeated_height:", repeated_height)
        print("total_height:", total_height)
