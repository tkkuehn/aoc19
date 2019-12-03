#!/usr/bin/python3

with open('./input.txt', 'r') as f:
    paths = f.read().splitlines()

position_sets = [set(), set()]

for path, position_set in zip(paths, position_sets):
    steps = path.split(',')
    cur_x = 0
    cur_y = 0

    for step in steps:
        dir = step[0]
        dist = int(step[1:])

        if dir == 'U':
            new_positions = {(cur_x, y) for y in
                    range(cur_y + 1, cur_y + dist + 1)}
            cur_y += dist
        elif dir == 'D':
            new_positions = {(cur_x, y) for y in 
                    range(cur_y - 1, cur_y - dist - 1, -1)}
            cur_y -= dist
        elif dir == 'R':
            new_positions = {(x, cur_y) for x in
                    range(cur_x + 1, cur_x + dist + 1)}
            cur_x += dist
        elif dir == 'L':
            new_positions = {(x, cur_y) for x in 
                    range(cur_x - 1, cur_x - dist - 1, -1)}
            cur_x -= dist
        else:
            raise Exception('Invalid direction')

        position_set |= new_positions

    position_set.discard((0, 0))

intersections = position_sets[0] & position_sets[1]
closest = min(intersections, key=lambda pos: abs(pos[0]) + abs(pos[1]))

print(abs(closest[0]) + abs(closest[1]))

