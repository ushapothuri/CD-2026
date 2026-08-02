"""
Three-Address Code to MIPS generator.

# Pending
"""
from three_address_code import BinOpTriple, AssignTriple, is_literal, TripleRef

MIPS_OP = {
    '+': 'add',
    '-': 'sub',
    '*': 'mul',   # SPIM pseudo-instruction: 3-operand mul $d,$s,$t
    '/': 'div',   # SPIM pseudo-instruction: 3-operand div $d,$s,$t
}


class MIPSGenerator:
    def __init__(self):     
        self.mips_lines = []
        # simple register allocation, when ever it is part of source operand make it available
        # $t0-$t9  all are available initially
        self.availabilitiy_registers = [True, True, True, True, True, True, True, True, True, True] 
        self.triple_index_to_reg = {}

    # allocate first available register
    def allocate_registers(self):
        """
        Call this to allocate register
        """
        try:
            freeregidx = self.availabilitiy_registers.index(True)
            self.availabilitiy_registers[freeregidx] = False
            reg = "$t" + str(freeregidx)
            return reg 
        except ValueError:
            print("Registers are not available")
    
    def deallocate_register(self, reg):
        extract_idx = int(reg[2])
        self.availabilitiy_registers[extract_idx]= True 


    def addMIPS(self, line):
        """Appends one line of MIPS assembly """
        self.mips_lines.append(line)

    def load(self, operand, reg):
        """
          - If is_literal(operand) is True: 
            `li reg, operand`
          - Otherwise:
            `lw reg, name`
        """
        if is_literal(operand):
            self.addMIPS(f"li {reg}, {operand}")
        else:
            self.addMIPS(f"lw {reg}, disp($fp)of{operand}")

    def store(self, reg, name):
        """
           `sw reg, name`
        """
        self.addMIPS(f"sw {reg},disp($fp)of{name}")
        self.deallocate_register(reg)
        
    def gen_instr(self, triple):
        """  
          isinstance(instr, CopyTAC):
              self.load(instr.src, '$t0')
              self.store('$t0', instr.dest)
        """
        if isinstance(triple, BinOpTriple):
            if isinstance(triple.arg1, TripleRef):
                src1 = self.triple_index_to_reg[triple.arg1.index]
            else:
                src1 = self.allocate_registers()
                self.load(triple.arg1, src1)
                
            if isinstance(triple.arg2, TripleRef):
                src2 = self.triple_index_to_reg[triple.arg2.index]
            else:
                src2 = self.allocate_registers()
                self.load(triple.arg2, src2)

            dest = self.allocate_registers()
            
            self.addMIPS(f"{MIPS_OP[triple.op]} {dest}, {src1}, {src2}")
            self.triple_index_to_reg[triple.index] = dest
            if not isinstance(triple.arg1, TripleRef):
                self.deallocate_register(src1)
            if not isinstance(triple.arg2, TripleRef):
                self.deallocate_register(src2)
        elif isinstance(triple,AssignTriple):
            if isinstance(triple.arg1, TripleRef):
                src = self.triple_index_to_reg[triple.arg1.index]
            else:
                src = self.allocate_registers()
                self.load(triple.arg1, src)
            self.store(src, triple.dest)


    def generate(self, instructions):
        """
        Runs gen_instr() over the whole 3AC list, then appends
        the program-exit syscall sequence, then renders the final .s
        text. You should not need to change this method.
        """
        for instr in instructions:
            self.gen_instr(instr)
        self.addMIPS("li $v0, 10")
        self.addMIPS("syscall")
        return self.render()

    def render(self):
        lines = []
        lines.extend(f"{line}" for line in self.mips_lines)
        return "\n".join(lines) + "\n"


def generate_mips(tripleprogram):
    """wrapper: generates MIPS assembly"""
    return MIPSGenerator().generate(tripleprogram.triples)
