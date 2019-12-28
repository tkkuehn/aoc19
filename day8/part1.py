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

for layer, layer_idx in zip(im_data, range(layers)):
    zero_count = 0
    for row in layer:
        for value in row:
            if value == 0:
                zero_count += 1
    if zero_count < fewest_zeros:
        fewest_zeros = zero_count
        fewest_zero_layer = layer_idx

one_count = 0
two_count = 0

for row in im_data[fewest_zero_layer]:
    for value in row:
        if value == 1:
            one_count += 1
        elif value == 2:
            two_count += 1

print(one_count * two_count)

