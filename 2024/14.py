#!/usr/bin/env python3
import re
from pprint import pprint
from functools import reduce
import copy
import numpy as np
import math
regex = re.compile(r"p=(-?\d+),(-?\d+)\s+v=(-?\d+),(-?\d+)")

quad_map = {
    (0, 0): 0,
    (1, 0): 1,
    (0, 1): 2,
    (1, 1): 3
}

def safety(robots, dim):
    mid = tuple(d // 2 for d in dim)
    quads = [0, 0, 0, 0]

    for robot in robots:
        if robot['p'][0] != mid[0] and robot['p'][1] != mid[1]:
          quads[sum((0 if coord < mid[i] else [1, 2][i]) for i, coord in enumerate(robot['p']))] += 1

    return reduce(lambda x, y: x * y, quads)

biggest = 0
biggest_time = None
smallest = None
smallest_time = None

def weight(distance, k=1.0):
    return math.exp(-k * distance)

def line_score(robots):
    x_list = [robot['p'][0] for robot in robots]
    median_x = x_list[len(x_list) // 2]
    #print("median_x: " + str(median_x))

    score = sum([weight(abs(robot['p'][0] - median_x)) for robot in robots])

    return score


def is_tree_bak(robots, dim, time):
    global biggest, biggest_time

    points = [robot['p'] for robot in robots]

    # Sort points by y-coordinate first, then by x-coordinate
    points.sort(key=lambda p: (p[1], p[0]))

    # Create a list where each sublist contains x-values for each unique y
    y_max = max(p[1] for p in points)  # Get the maximum y-value
    sorted_y_list = [[] for _ in range(y_max + 1)]  # Create a list of empty lists

    for point in points:
        x, y = point
        sorted_y_list[y].append(x)

    longest_sequences = []

    for y, x_values in enumerate(sorted_y_list):
        if not x_values:
            longest_sequences.append(0)  # If no x-values for y, append 0
            continue  # Skip empty lists

        # Sort x-values for each y to ensure they're in order (if not already sorted)
        x_values.sort()

        longest_seq_len = 1  # The minimum length of a sequence is 1
        current_seq_len = 1  # Start with the first x-value in the list

        # Iterate through the x-values to find consecutive sequences
        for i in range(1, len(x_values)):
            if x_values[i] == x_values[i - 1] + 1:
                current_seq_len += 1  # If consecutive, increase current sequence length
            else:
                # Update the longest sequence if needed
                longest_seq_len = max(longest_seq_len, current_seq_len)
                current_seq_len = 1  # Reset for new sequence

        # Final check after loop to ensure we capture the longest sequence
        longest_seq_len = max(longest_seq_len, current_seq_len)

        # Append the length of the longest sequence for this y
        longest_sequences.append(longest_seq_len)

    #print(longest_sequences)
    if sum(longest_sequences) > biggest:
        biggest = sum(longest_sequences)
        biggest_time = time
        print("biggest " + str(biggest) + " at " + str(biggest_time))

def is_tree_bak2(robots, dim, time):
    global smallest, smallest_time
    dist = 0
    for i in range(len(robots)):
        for j in range(i + 1, len(robots)):
            dist += abs(robots[i]['p'][0] - robots[j]['p'][0])

    if not smallest:
        smallest = dist
    elif dist < smallest:
        smallest = dist
        smallest_time = time
        print("Smallest " + str(smallest) + " at " + str(smallest_time))

initial = None
def is_tree(robots, dim, time):
    global initial
    score = line_score(robots)

    if time == 0:
        initial = score

    print("time " + str(time) + " score " + str(score) + " initial " + str(initial))


with open("14.input") as file:
    robots = [{'p': [int(match.group(1)), int(match.group(2))], 'v': [int(match.group(3)), int(match.group(4))]} for line in file if (match := re.match(regex, line))]
    # nrs = list(map(int, re.findall(r"-?\d+", line)))

    dim = (11, 7) if file.name.endswith('.example') else (101, 103)

    #print(robots)

    robots_bak = copy.deepcopy(robots)

    for robot in robots:
      for i in range(2):
          robot['p'][i] = (robot['p'][i] + 100 * robot['v'][i]) % dim[i]

    print(safety(robots, dim))

    robots = robots_bak

    best_score = None
    best_time = None

    for time in range(1, 8200):
        #print(time)
        for robot in robots:
            for i in range(2):
                robot['p'][i] = (robot['p'][i] + robot['v'][i]) % dim[i]
        score = line_score(robots)

        if not best_score or score >= best_score:
            print("time " + str(time) + " score " + str(score))
            best_score = score
            best_time = time

    print(best_time)
    print(best_score)