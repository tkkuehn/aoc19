#!/usr/bin/python3

with open('./input.txt', 'r') as f:
    contents = f.read().splitlines()[0]

program = [int(x) for x in contents.split(',')]

class Computer:
    def __init__(self):
        self.memory = []
        self.inst_ptr = 0
        self.output_buffer = []
        pass

    def run_program(self, program):
        self.memory = program.copy()
        self.inst_ptr = 0

        while True:
            print('Instruction pointer: {}'.format(self.inst_ptr))
            opcode_val = str(self.memory[self.inst_ptr])
            print(opcode_val)

            digits = len(opcode_val)

            if digits == 1:
                opcode_val = '0' + opcode_val
                digits += 1

            print(opcode_val)

            opcode = int(opcode_val[-2:])

            if opcode == 99:
                return self.output_buffer
            elif opcode in [1, 2]:
                params = 3
            elif opcode in [3, 4]:
                params = 1
            else:
                raise Exception('Invalid opcode')

            for i in range(params + 2 - digits):
                opcode_val = '0' + opcode_val

            print(opcode_val)

            if opcode == 1:
                if int(opcode_val[-3]) == 0:
                    augend_addr = self.memory[self.inst_ptr + 1]
                    augend = self.memory[augend_addr]
                else:
                    augend = self.memory[self.inst_ptr + 1]

                if int(opcode_val[-4]) == 0:
                    addend_addr = self.memory[self.inst_ptr + 2]
                    addend = self.memory[addend_addr]
                else:
                    addend = self.memory[self.inst_ptr + 2]

                if int(opcode_val[-5]) == 0:
                    result = self.memory[self.inst_ptr + 3]
                else:
                    raise Exception('Invalid parameter mode')

                print('{} + {} -> {}'.format(augend, addend, result))

                self.memory[result] = augend + addend
            elif opcode == 2:
                if int(opcode_val[-3]) == 0:
                    multiplicand_addr = self.memory[self.inst_ptr + 1]
                    multiplicand = self.memory[multiplicand_addr]
                else:
                    multiplicand = self.memory[self.inst_ptr + 1]

                if int(opcode_val[-4]) == 0:
                    multiplier_addr = self.memory[self.inst_ptr + 2]
                    multiplier = self.memory[multiplier_addr]
                else:
                    multiplier = self.memory[self.inst_ptr + 2]

                if int(opcode_val[-5]) == 0:
                    result = self.memory[self.inst_ptr + 3]
                else:
                    raise Exception('Invalid parameter mode')

                print('{} * {} -> {}'.format(multiplicand, multiplier, result))

                self.memory[result] = multiplicand * multiplier 
            elif opcode == 3:
                if int(opcode_val[-3]) == 0:
                    input_ = self.memory[self.inst_ptr + 1]
                else:
                    raise Exception('Invalid parameter mode')

                val = int(input('Input: '))

                print('{} -> {}'.format(val, input_))

                self.memory[input_] = val
            elif opcode == 4:
                if int(opcode_val[-3]) == 0:
                    output_addr = self.memory[self.inst_ptr + 1]
                    output_ = self.memory[output_addr]
                else:
                    output_ = self.memory[self.inst_ptr + 1]

                self.output_buffer.append(output_)
            else:
                raise Exception('Invalid opcode')

            self.inst_ptr += params + 1

comp = Computer()

try:
    print(comp.run_program(program))
except Exception as e:
    print('Exception: {}, Output: {}'.format(e, comp.output_buffer))
