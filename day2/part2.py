#!/usr/bin/python3

with open('./input.txt', 'r') as f:
    contents = f.read().splitlines()[0]

program = [int(x) for x in contents.split(',')]

def run_program(noun, verb):
    memory = program.copy()
    memory[1] = noun
    memory[2] = verb

    inst_ptr = 0

    while True:
        opcode = memory[inst_ptr]

        if opcode == 99:
            return memory[0]

        input_1_addr = memory[inst_ptr + 1]
        input_2_addr = memory[inst_ptr + 2]
        output_addr = memory[inst_ptr + 3]

        if opcode == 1:
            memory[output_addr] = memory[input_1_addr] + memory[input_2_addr]
        elif opcode == 2:
            memory[output_addr] = memory[input_1_addr] * memory[input_2_addr]
        else:
            raise Exception('Invalid opcode')

        inst_ptr += 4

for noun in range(100):
    for verb in range(100):
        if run_program(noun, verb) == 19690720:
            print('Noun: {}, Verb: {}'.format(noun, verb))
            print('100 * noun + verb = {}'.format((100 * noun) + verb))

