#!/usr/bin/python3

with open('./input.txt', 'r') as f:
    contents = f.read().splitlines()[0]

opcodes = [int(x) for x in contents.split(',')]
opcodes[1] = 12
opcodes[2] = 2

current_index = 0

while True:
    opcode = opcodes[current_index]

    if opcode == 99:
        break

    input_1 = opcodes[current_index + 1]
    input_2 = opcodes[current_index + 2]
    output = opcodes[current_index + 3]

    if opcode == 1:
        opcodes[output] = opcodes[input_1] + opcodes[input_2]
    elif opcode == 2:
        opcodes[output] = opcodes[input_1] * opcodes[input_2]
    else:
        raise Exception()

    current_index += 4

print(opcodes[0])
