#!/usr/bin/python3

with open('./input.txt', 'r') as f:
    contents = f.read().splitlines()[0]

program = [int(x) for x in contents.split(',')]

class Computer:
    def __init__(self):
        self.memory = []
        self.inst_ptr = 0
        self.input_queue = []
        self.output_buffer = []
        pass

    def run_program(self, program):
        self.memory = program.copy()
        self.inst_ptr = 0
        self.continue_program()

    def continue_program(self):
        while True:
            opcode_val = str(self.memory[self.inst_ptr])

            digits = len(opcode_val)

            if digits == 1:
                opcode_val = '0' + opcode_val
                digits += 1

            opcode = int(opcode_val[-2:])

            if opcode == 99:
                return 0
            elif opcode in [1, 2, 7, 8]:
                params = 3
            elif opcode in [3, 4]:
                params = 1
            elif opcode in [5, 6]:
                params = 2
            else:
                raise Exception('Invalid opcode')

            for i in range(params + 2 - digits):
                opcode_val = '0' + opcode_val

            increase_int_ptr = True
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

                self.memory[result] = multiplicand * multiplier 
            elif opcode == 3:
                if int(opcode_val[-3]) == 0:
                    input_ = self.memory[self.inst_ptr + 1]
                else:
                    raise Exception('Invalid parameter mode')

                val = int(self.input_queue.pop(0))

                self.memory[input_] = val
            elif opcode == 4:
                if int(opcode_val[-3]) == 0:
                    output_addr = self.memory[self.inst_ptr + 1]
                    output_ = self.memory[output_addr]
                else:
                    output_ = self.memory[self.inst_ptr + 1]

                self.output_buffer.append(output_)
                self.inst_ptr += params + 1
                return 1
            elif opcode in [5, 6]:
                if int(opcode_val[-3]) == 0:
                    check_addr = self.memory[self.inst_ptr + 1]
                    check = self.memory[check_addr]
                else:
                    check = self.memory[self.inst_ptr + 1]

                if int(opcode_val[-4]) == 0:
                    val_addr = self.memory[self.inst_ptr + 2]
                    val = self.memory[val_addr]
                else:
                    val = self.memory[self.inst_ptr + 2]

                if ((opcode == 5 and check != 0)
                        or (opcode == 6 and check == 0)):
                    self.inst_ptr = val
                    increase_int_ptr = False 
            elif opcode == 7:
                if int(opcode_val[-3]) == 0:
                    a_addr = self.memory[self.inst_ptr + 1]
                    a = self.memory[a_addr]
                else:
                    a = self.memory[self.inst_ptr + 1]

                if int(opcode_val[-4]) == 0:
                    b_addr = self.memory[self.inst_ptr + 2]
                    b = self.memory[b_addr]
                else:
                    b = self.memory[self.inst_ptr + 2]

                if int(opcode_val[-5]) == 0:
                    result = self.memory[self.inst_ptr + 3]
                else:
                    raise Exception('Invalid parameter mode')

                if a < b:
                    self.memory[result] = 1
                else:
                    self.memory[result] = 0
            elif opcode == 8:
                if int(opcode_val[-3]) == 0:
                    a_addr = self.memory[self.inst_ptr + 1]
                    a = self.memory[a_addr]
                else:
                    a = self.memory[self.inst_ptr + 1]

                if int(opcode_val[-4]) == 0:
                    b_addr = self.memory[self.inst_ptr + 2]
                    b = self.memory[b_addr]
                else:
                    b = self.memory[self.inst_ptr + 2]

                if int(opcode_val[-5]) == 0:
                    result = self.memory[self.inst_ptr + 3]
                else:
                    raise Exception('Invalid parameter mode')

                if a == b:
                    self.memory[result] = 1
                else:
                    self.memory[result] = 0
            else:
                raise Exception('Invalid opcode')

            if increase_int_ptr:
                self.inst_ptr += params + 1

def run_amps(phases):
    a = Computer()
    b = Computer()
    c = Computer()
    d = Computer()
    e = Computer()

    a.input_queue.append(phases[0])
    b.input_queue.append(phases[1])
    c.input_queue.append(phases[2])
    d.input_queue.append(phases[3])
    e.input_queue.append(phases[4])

    a.input_queue.append(0)

    a.run_program(program)
    b.input_queue.append(a.output_buffer[-1])
    b.run_program(program)
    c.input_queue.append(b.output_buffer[-1])
    c.run_program(program)
    d.input_queue.append(c.output_buffer[-1])
    d.run_program(program)
    e.input_queue.append(d.output_buffer[-1])
    e.run_program(program)
    a.input_queue.append(e.output_buffer[-1])

    while True:
        a.continue_program()
        b.input_queue.append(a.output_buffer[-1])
        b.continue_program()
        c.input_queue.append(b.output_buffer[-1])
        c.continue_program()
        d.input_queue.append(c.output_buffer[-1])
        d.continue_program()
        e.input_queue.append(d.output_buffer[-1])
        if e.continue_program() == 0:
            break
        else:
            a.input_queue.append(e.output_buffer[-1])

    return e.output_buffer[-1]

max_signal = 0
phases = frozenset(range(5, 10))

for a_phase in phases:
    for b_phase in phases - frozenset([a_phase]):
        for c_phase in phases - frozenset([a_phase, b_phase]):
            for d_phase in phases - frozenset([a_phase, b_phase, c_phase]):
                for e_phase in phases - frozenset(
                        [a_phase, b_phase, c_phase, d_phase]):
                    signal = run_amps(
                        [a_phase, b_phase, c_phase, d_phase, e_phase])
                    if signal > max_signal:
                        max_signal = signal

print(max_signal)
