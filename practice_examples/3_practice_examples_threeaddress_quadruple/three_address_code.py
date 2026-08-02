"""
Three-address code (3AC) instruction classes -- fully implemented.

    BinOpTAC(dest, op, src1, src2)   dest = src1 op src2
    CopyTAC(dest, src)               dest = src

`op` is one of '+', '-', '*', '/'. `dest`/`src1`/`src2`/`src` are always
plain strings: 

"""


class BinOpTAC:
    def __init__(self, dest, op, src1, src2):
        self.dest = dest
        self.op = op
        self.src1 = src1
        self.src2 = src2

    def render(self):
        return f"{self.dest} = {self.src1} {self.op} {self.src2}"


class CopyTAC:
    def __init__(self, dest, src):
        self.dest = dest
        self.src = src

    def render(self):
        return f"{self.dest} = {self.src}"




def render_threeAddressCode(instructions):
    """
    Text form of a flat list of TAC instructions, one per line 
    """
    return "\n".join(instr.render() for instr in instructions)

