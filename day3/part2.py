#!/usr/bin/python3

with open('./input.txt', 'r') as f:
    paths = f.read().splitlines()

position_dicts = [{}, {}]

for path, position_dict in zip(paths, position_dicts):
    strides = path.split(',')
    cur_steps = 0
    cur_x = 0
    cur_y = 0

    for stride in strides:
        dir_ = stride[0]
        dist = int(stride[1:])

        if dir_ == 'U':
            new_positions = {(cur_x, y): cur_steps + s + 1 for y, s in
                    zip(range(cur_y + 1, cur_y + dist + 1), range(dist))}
            cur_y += dist
            cur_steps += dist
        elif dir_ == 'D':
            new_positions = {(cur_x, y): cur_steps + s + 1 for y, s in 
                    zip(range(cur_y - 1, cur_y - dist - 1, -1), range(dist))}
            cur_y -= dist
            cur_steps += dist
        elif dir_ == 'R':
            new_positions = {(x, cur_y): cur_steps + s + 1 for x, s in
                    zip(range(cur_x + 1, cur_x + dist + 1), range(dist))}
            cur_x += dist
            cur_steps += dist
        elif dir_ == 'L':
            new_positions = {(x, cur_y): cur_steps + s + 1 for x, s in 
                    zip(range(cur_x - 1, cur_x - dist - 1, -1), range(dist))}
            cur_x -= dist
            cur_steps += dist
        else:
            raise Exception('Invalid direction')

        for pos in new_positions.keys():
            if pos not in position_dict:
                position_dict[pos] = new_positions[pos]

    position_dict.pop((0, 0), 0)

intersections = set(position_dicts[0].keys()) & set(position_dicts[1].keys())
closest = min(intersections,
              key=lambda pos: position_dicts[0][pos] + position_dicts[1][pos])

print('Closest: {}'.format(closest))
print('Path zero steps: {}, path one steps: {}'.format(
    position_dicts[0][closest], position_dicts[1][closest]))
print(position_dicts[0][closest] + position_dicts[1][closest])

