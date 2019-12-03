#!/usr/bin/python3

with open('./input.txt', 'r') as f:
    paths = f.read().splitlines()

positions = [set(), set()]

for path in paths:
    steps = path.split(',')
    cur_x = 0
    cur_y = 0

    for step in steps:
        dir = step[0]
        dist = int(step[1:])
        if dir == 'U':
            new_positions = (cur_x, range(cur_y + 1, dist + 1))


