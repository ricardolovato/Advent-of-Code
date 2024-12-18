class Computer:
    def __init__(self, A, B, C, instr: list):
        self.A = i2b(A)
        self.B = i2b(B)
        self.C = i2b(C)

        self.instr = instr

        self.run()

    def run(self):
        op_counter = 0

        output = []
        while op_counter < len(self.instr):
            opcode = self.instr[op_counter]
            operand = self.instr[op_counter + 1]
            # self.show_registers()
            # print(f'Opcode: {opcode}, operand: {operand}')

            if opcode == 0:
                print('\tadv')
                self.adv(operand)
            elif opcode == 1:
                print('\tbxl')
                self.bxl(operand)
            elif opcode == 2:
                print('\tbst')
                self.bst(operand)
            elif opcode == 3:
                print('\tjnz')
                jnz = self.jnz(operand)
                if jnz is not None:
                    op_counter = jnz
                    continue
            elif opcode == 4:
                print('\tbxc')
                self.bxc(operand)
            elif opcode == 5:
                print('\tout')
                output.append(self.out(operand))
            elif opcode == 6:
                print('\tbdv')
                self.bdv(operand)
            elif opcode == 7:
                print('\tcdv')
                self.cdv(operand)
            op_counter += 2

        self.show_registers()
        print(','.join([str(v) for v in output]))

    def adv(self, operand):
        operand = self.combo_operand(operand)
        i_operand = b2i(operand)
        self.A = i2b(b2i(self.A) // 2**i_operand)#[0:3]


    def bxl(self, operand):
        self.B = xor(self.B, i2b(operand))


    def bst(self, operand):
        operand = self.combo_operand(operand)
        self.B = operand[0:3]


    def jnz(self, operand):
        if all(a == 0 for a in self.A):
            return None
        return operand

    def bxc(self, operand):
        self.B = xor(self.B, self.C)


    def out(self, operand):
        operand = self.combo_operand(operand)
        return b2i(operand[0:3])
        # print(b2i(operand[0:3]))


    def bdv(self, operand):
        operand = self.combo_operand(operand)
        i_operand = b2i(operand)
        self.B = i2b(b2i(self.A) // 2**i_operand)[0:3]


    def cdv(self, operand):
        operand = self.combo_operand(operand)
        i_operand = b2i(operand)
        self.C = i2b(b2i(self.A) // 2**i_operand)[0:3]

    def combo_operand(self, operand):
        if operand in [0, 1, 2, 3]:
            return i2b(operand)
        elif operand == 4:
            return self.A
        elif operand == 5:
            return self.B
        elif operand == 6:
            return self.C
        elif operand == 7:
            print('invalid operand')
            return None
        else:
            print('invalid operand')
            return None

    def show_registers(self,):
        print(f'Register A:\t{b2i(self.A)}')
        print(f'Register B:\t{b2i(self.B)}')
        print(f'Register C:\t{b2i(self.C)}')


def i2b(n):
    if n == 1:
        return [1]
    if n == 0:
        return [0]

    current = n
    remainders = []
    result = current//2
    while result != 0:
        result = current // 2
        remainders.append(current % 2)

        current = result
    return remainders


def b2i(n):
    s = 0
    for iV, v in enumerate(n):
        s += v * 2 ** iV
    return s


def xor(a, b):
    a, b = zero_pad(a, b)
    result = []
    for _a, _b in zip(a, b):
        if _a == 0 and _b == 1 or _a == 1 and _b == 0:
            result.append(1)
        else:
            result.append(0)
    return result

def zero_pad(a, b):
    # Make the lengths the same
    if len(a) != len(b):
        pad = abs(len(a) - len(b))
        if len(a) > len(b):
            while len(b) != len(a):
                b.append(0)
        else:
            while len(b) != len(a):
                a.append(0)
    return a, b

def mul(a, b):
    # Make the lengths the same
    a, b = zero_pad(a, b)

    # Multiplication
    results = []
    for idx in range(len(a)):
        if b[idx] == 1:
            results.append([0] * idx + a)

    # Equalize lengths
    max_len = max([len(r) for r in results])
    for idx in range(len(results)):
        while len(results[idx]) != max_len:
            results[idx].append(0)

    # Binary addition
    return add(results)

def add(n):
    # for _n in n:
    #     print(_n)

    num = []
    carry = 0
    for col_idx in range(len(n[0])):
        # print(f'col {col_idx}: {[_n[col_idx] for _n in n]}; carry {carry}')
        row = i2b(sum([_n[col_idx] for _n in n] + [carry]))

        result = row[0]
        if len(row) == 1:
            carry = 0
        else:
            carry = row[-1]
        num.append(result)

        # print(f'\tresult:{result}\n\tcarry:{carry}\n\tnums:{num}')
    num.append(carry)
    # print(num)

    return num

# comp = Computer(0, 0, 9, [2, 6])
# comp = Computer(10, 0, 0, [5,0,5,1,5,4])
# Computer(2024, 0, 0, [0,1,5,4,3,0])
# Computer(0, 29, 0, [1,7])
# Computer(0, 2024, 43690, [4,0])
# comp = Computer(729, 0, 0, [0,1,5,4,3,0])
Computer(61156655, 0, 0, [2,4,1,5,7,5,4,3,1,6,0,3,5,5,3,0])