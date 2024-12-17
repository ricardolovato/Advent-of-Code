class Computer:
    def __init__(self, A, B, C, instr: list):
        self.A = A
        self.B = B
        self.C = C

        self.instr = instr

    def run(self):
        while self.instr:
            opcode = self.instr.pop()
            operand = self.instr.pop()




comp = Computer(0, 0, 9, [2, 6])
