#!/usr/bin/python3

with open('./input.txt', 'r') as f:
    contents = f.read().splitlines()[0]

values = [int(x) for x in contents]

width = 25
height = 6
layers = len(values) // (width * height)
im_data = []
i = 0

for layer in range(layers):
    layer_data = []
    for row in range(height):
        row_data = []
        for col in range(width):
            row_data.append(values[i])
            i += 1
        layer_data.append(row_data)
    im_data.append(layer_data)

fewest_zeros = width * height
fewest_zero_layer = None

final_img = []

for y in range(height):
    row = []
    for x in range(width):
        for layer in im_data:
            val = layer[y][x]
            if val != 2:
                row.append(val)
                break
            else:
                continue
    final_img.append(row)

for row in final_img:
    line = ''
    for val in row:
        if val == 0:
            line += '.'
        elif val == 1:
            line += '#'
    print(line)

