#!/usr/bin/python3

with open('./input.txt', 'r') as f:
    contents = f.read().splitlines()[0]

program = [int(x) for x in contents.split(',')]

class Computer:
    def __init__(self):
        self.memory = {}
        self.inst_ptr = 0
        self.input_queue = []
        self.output_buffer = []
        self.relative_base = 0

    def run_program(self, program):
        self.memory = {idx: val for idx, val in zip(range(len(program)), program)}
        self.inst_ptr = 0
        return self.continue_program()

    def access_memory(self, idx):
        if idx < 0:
            raise KeyError('Attempted to access negative address')

        try:
            return self.memory[idx]
        except KeyError:
            self.memory[idx] = 0
            return 0

    def mutate_memory(self, idx, val):
        if idx < 0:
            raise KeyError('Attempted to mutate negative address')

        self.memory[idx] = val

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
            elif opcode in [3, 4, 9]:
                params = 1
            elif opcode in [5, 6]:
                params = 2
            else:
                raise Exception('Invalid opcode')

            for i in range(params + 2 - digits):
                opcode_val = '0' + opcode_val

            increase_int_ptr = True
            if opcode == 1:
                augend_mode = int(opcode_val[-3])
                if augend_mode == 0:
                    augend_addr = self.access_memory(self.inst_ptr + 1)
                    augend = self.access_memory(augend_addr)
                elif augend_mode == 1:
                    augend = self.access_memory(self.inst_ptr + 1)
                elif augend_mode == 2:
                    augend_addr = self.access_memory(self.inst_ptr + 1)
                    augend = self.access_memory(
                        self.relative_base + augend_addr)
                else:
                    raise RuntimeError(
                        'Invalid augend mode: {}'.format(augend_mode))

                addend_mode = int(opcode_val[-4])
                if addend_mode == 0:
                    addend_addr = self.access_memory(self.inst_ptr + 2)
                    addend = self.access_memory(addend_addr)
                elif addend_mode == 1:
                    addend = self.access_memory(self.inst_ptr + 2)
                elif addend_mode == 2:
                    addend_addr = self.access_memory(self.inst_ptr + 2)
                    addend = self.access_memory(
                        self.relative_base + addend_addr)
                else:
                    raise RuntimeError(
                        'Invalid addend mode: {}'.format(addend_mode))

                result_mode = int(opcode_val[-5])
                if result_mode == 0:
                    result = self.access_memory(self.inst_ptr + 3)
                elif result_mode == 2:
                    result = self.relative_base + self.access_memory(
                        self.inst_ptr + 3)
                else:
                    raise RuntimeError(
                        'Invalid result mode: {}'.format(result_mode))

                self.mutate_memory(result, augend + addend)
            elif opcode == 2:
                multiplicand_mode = int(opcode_val[-3])
                if multiplicand_mode == 0:
                    multiplicand_addr = self.access_memory(self.inst_ptr + 1)
                    multiplicand = self.access_memory(multiplicand_addr)
                elif multiplicand_mode == 1:
                    multiplicand = self.access_memory(self.inst_ptr + 1)
                elif multiplicand_mode == 2:
                    multiplicand_addr = self.access_memory(self.inst_ptr + 1)
                    multiplicand = self.access_memory(self.relative_base
                        + multiplicand_addr)
                else:
                    raise RuntimeError(
                        'Invalid multiplicand mode: {}'.format(
                             multiplicand_mode))

                multiplier_mode = int(opcode_val[-4])
                if multiplier_mode == 0:
                    multiplier_addr = self.access_memory(self.inst_ptr + 2)
                    multiplier = self.access_memory(multiplier_addr)
                elif multiplier_mode == 1:
                    multiplier = self.access_memory(self.inst_ptr + 2)
                elif multiplier_mode == 2:
                    multiplier_addr = self.access_memory(self.inst_ptr + 2)
                    multiplier = self.access_memory(self.relative_base
                        + multiplier_addr)
                else:
                    raise RuntimeError(
                        'Invalid multiplier mode: {}'.format(multiplier_mode))

                result_mode = int(opcode_val[-5])
                if result_mode == 0:
                    result = self.access_memory(self.inst_ptr + 3)
                elif result_mode == 2:
                    result = self.relative_base + self.access_memory(
                        self.inst_ptr + 3)
                else:
                    raise RuntimeError(
                        'Invalid result mode: {}'.format(result_mode))

                self.mutate_memory(result, multiplicand * multiplier)
            elif opcode == 3:
                input_mode = int(opcode_val[-3])
                if input_mode == 0:
                    input_ = self.access_memory(self.inst_ptr + 1)
                elif input_mode == 2:
                    input_ = self.relative_base + self.access_memory(
                        self.inst_ptr + 1)
                else:
                    raise RuntimeError(
                        'Invalid input mode: {}'.format(input_mode))

                val = int(self.input_queue.pop(0))

                self.mutate_memory(input_, val)
            elif opcode == 4:
                output_mode = int(opcode_val[-3])
                if output_mode == 0:
                    output_addr = self.access_memory(self.inst_ptr + 1)
                    output_ = self.access_memory(output_addr)
                elif output_mode == 1:
                    output_ = self.access_memory(self.inst_ptr + 1)
                elif output_mode == 2:
                    output_addr = self.relative_base + self.access_memory(
                        self.inst_ptr + 1)
                    output_ = self.access_memory(output_addr)
                else:
                    raise RuntimeError(
                        'Invalid output mode: {}'.format(output_mode))

                self.output_buffer.append(output_)
                self.inst_ptr += params + 1
                return 1
            elif opcode in [5, 6]:
                check_mode = int(opcode_val[-3])
                if check_mode == 0:
                    check_addr = self.access_memory(self.inst_ptr + 1)
                    check = self.access_memory(check_addr)
                elif check_mode == 1:
                    check = self.access_memory(self.inst_ptr + 1)
                elif check_mode == 2:
                    check_addr = self.relative_base + self.access_memory(
                        self.inst_ptr + 1)
                    check = self.access_memory(check_addr)
                else:
                    raise RuntimeError('Invalid check mode: {}'.format(
                        check_mode))

                val_mode = int(opcode_val[-4])
                if val_mode == 0:
                    val_addr = self.access_memory(self.inst_ptr + 2)
                    val = self.access_memory(val_addr)
                elif val_mode == 1:
                    val = self.access_memory(self.inst_ptr + 2)
                elif val_mode == 2:
                    val_addr = self.relative_base + self.access_memory(
                        self.inst_ptr + 2)
                    val = self.access_memory(val_addr)
                else:
                    raise RuntimeError('Invalid val mode: {}'.format(
                        val_mode))

                if ((opcode == 5 and check != 0)
                        or (opcode == 6 and check == 0)):
                    self.inst_ptr = val
                    increase_int_ptr = False 
            elif opcode == 7:
                a_mode = int(opcode_val[-3])
                if a_mode == 0:
                    a_addr = self.access_memory(self.inst_ptr + 1)
                    a = self.access_memory(a_addr)
                elif a_mode == 1:
                    a = self.access_memory(self.inst_ptr + 1)
                elif a_mode == 2:
                    a_addr = self.relative_base + self.access_memory(
                        self.inst_ptr + 1)
                    a = self.access_memory(a_addr)
                else:
                    raise RuntimeError('Invalid a mode: {}'.format(
                        a_mode))

                b_mode = int(opcode_val[-4])
                if b_mode == 0:
                    b_addr = self.access_memory(self.inst_ptr + 2)
                    b = self.access_memory(b_addr)
                elif b_mode == 1:
                    b = self.access_memory(self.inst_ptr + 2)
                elif b_mode == 2:
                    b_addr = self.relative_base + self.access_memory(
                        self.inst_ptr + 2)
                    b = self.access_memory(b_addr)
                else:
                    raise RuntimeError('Invalid b mode: {}'.format(
                        b_mode))

                result_mode = int(opcode_val[-5])
                if result_mode == 0:
                    result = self.access_memory(self.inst_ptr + 3)
                elif result_mode == 2:
                    result = self.relative_base + self.access_memory(
                        self.inst_ptr + 3)
                else:
                    raise RuntimeError(
                        'Invalid result mode: {}'.format(result_mode))

                if a < b:
                    self.mutate_memory(result, 1)
                else:
                    self.mutate_memory(result, 0)
            elif opcode == 8:
                a_mode = int(opcode_val[-3])
                if a_mode == 0:
                    a_addr = self.access_memory(self.inst_ptr + 1)
                    a = self.access_memory(a_addr)
                elif a_mode == 1:
                    a = self.access_memory(self.inst_ptr + 1)
                elif a_mode == 2:
                    a_addr = self.relative_base + self.access_memory(
                        self.inst_ptr + 1)
                    a = self.access_memory(a_addr)
                else:
                    raise RuntimeError('Invalid a mode: {}'.format(
                        a_mode))

                b_mode = int(opcode_val[-4])
                if b_mode == 0:
                    b_addr = self.access_memory(self.inst_ptr + 2)
                    b = self.access_memory(b_addr)
                elif b_mode == 1:
                    b = self.access_memory(self.inst_ptr + 2)
                elif b_mode == 2:
                    b_addr = self.relative_base + self.access_memory(
                        self.inst_ptr + 2)
                    b = self.access_memory(b_addr)
                else:
                    raise RuntimeError('Invalid b mode: {}'.format(
                        b_mode))

                result_mode = int(opcode_val[-5])
                if result_mode == 0:
                    result = self.access_memory(self.inst_ptr + 3)
                elif result_mode == 2:
                    result = self.relative_base + self.access_memory(
                        self.inst_ptr + 3)
                else:
                    raise RuntimeError(
                        'Invalid result mode: {}'.format(result_mode))

                if a == b:
                    self.mutate_memory(result, 1)
                else:
                    self.mutate_memory(result, 0)
            elif opcode == 9:
                adjust_mode = int(opcode_val[-3])
                if adjust_mode == 0:
                    adjust_addr = self.access_memory(self.inst_ptr + 1)
                    adjust = self.access_memory(adjust_addr)
                elif adjust_mode == 1:
                    adjust = self.access_memory(self.inst_ptr + 1)
                elif adjust_mode == 2:
                    adjust_addr = self.relative_base + self.access_memory(
                        self.inst_ptr + 1)
                    adjust = self.access_memory(adjust_addr)
                else:
                    raise RuntimeError('Invalid adjust mode: {}'.format(
                        adjust_mode))

                self.relative_base += adjust

            else:
                raise Exception('Invalid opcode: {}'.format(opcode))

            if increase_int_ptr:
                self.inst_ptr += params + 1

a = Computer()
a.input_queue.append(1)
if a.run_program(program) == 1:
    while True:
        if a.continue_program() == 0:
            break

print(a.output_buffer)
