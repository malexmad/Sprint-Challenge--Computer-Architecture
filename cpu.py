"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 7

        self.e = 0
        self.l = 0
        self.g = 0

    def ram_read(self, add):
        """ Accept address to read and return valued stored """
        return self.ram[add]

    def ram_write(self, add, val):
        """ Accept address and value to write """
        self.ram[add] = val

    def load(self):
        address = 0

        try:

            filename = sys.argv[1]
            with open(filename) as f:
                for line in f:

                    comment_split = line.split("#")

                    num = comment_split[0].strip()

                    if num == '':
                        continue

                    val = int(num, 2)
                    self.ram[address] = val
                    address += 1

            # print("done loading")
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            print(self.reg[reg_a] * self.reg[reg_b])

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        MUL = 0b10100010
        ADD = 0b10100000
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001

        CMP = 0b10100111
        JEQ = 0b01010101
        JNE = 0b01010110
        JMP = 0b01010100

        while running:

            inst = self.ram_read(self.pc)

            if inst == LDI:
                # store value in register
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)

                # print(operand_a, operand_b)
                self.reg[operand_a] = operand_b
                # self.ram_write(operand_a,operand_b)
                self.pc += 3

            elif inst == CALL:
                return_addr = self.pc + 2

                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = return_addr

                reg_num = self.ram[self.pc + 1]
                dest_addr = self.reg[reg_num]
                self.pc = dest_addr

            elif inst == RET:
                return_addr = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1

                self.pc = return_addr

            elif inst == MUL:
                # print the product of 2 values
                self.alu("MUL", self.ram_read(self.pc+1), self.ram_read(self.pc+2))
                self.pc += 3

            elif inst == ADD:
                self.alu("ADD", self.ram_read(self.pc+1), self.ram_read(self.pc+2))
                self.pc +=3

            elif inst == PRN:
                # print value in register
                print(self.reg[self.ram_read(self.pc+1)])
                self.pc += 2

            elif inst == PUSH:
                reg = self.ram[self.pc + 1]
                val = self.reg[reg]
                self.reg[self.sp] -= 1
                self.ram[self.reg[self.sp]] = val
                self.pc += 2

            elif inst == POP:
                reg = self.ram[self.pc+1]
                val = self.ram[self.reg[self.sp]]
                self.reg[reg] = val
                self.reg[self.sp] += 1
                self.pc += 2

            elif inst == CMP:
                if self.reg[self.ram_read(self.pc + 1)] == self.reg[self.ram_read(self.pc + 2)]:
                    self.e = 1
                    self.l = 0
                    self.g = 0
                elif self.reg[self.ram_read(self.pc + 1)] < self.reg[self.ram_read(self.pc + 2)]:
                    self.l = 1
                    self.e = 0
                    self.g = 0
                elif self.reg[self.ram_read(self.pc + 1)] > self.reg[self.ram_read(self.pc + 2)]:
                    self.g = 1
                    self.l = 0
                    self.e = 0

                self.pc += 3

            elif inst == JEQ:
                if self.e == 1:
                    self.pc = self.reg[self.ram_read(self.pc + 1)]
                else:
                    self.pc += 2

            elif inst == JNE:
                if self.e == 0:
                    self.pc = self.reg[self.ram_read(self.pc + 1)]
                else:
                    self.pc += 2

            elif inst == JMP:
                self.pc = self.reg[self.ram_read(self.pc + 1)]

            elif inst == HLT:
                # halt CPU and exit
                running = False

            else:
                print("Unknown instruction")
                running = False


# cpu = CPU()
#
# cpu.load()
# cpu.run()
