"""
AST to Three-Address Code generator.

  - Var(name)  -> return the name directly. No instruction emitted --
                  reading a variable doesn't require computing anything.

  - Num(value) -> return str(value) directly. No instruction emitted --
                  a literal is already a value.

  - BinOp(op, left, right) -> recursively get the left and right
                  operands (each may or may not have emitted
                  instructions as a side effect), allocate ONE new
                  temporary, emit ONE BinOpTAC combining the two
                  operands into it, and return the new temporary's name.
 
  - Assign(var, expr) -> get the expr's result operand, emit ONE CopyTAC
                  assigning it into var.name.
 """
from ast_nodes import Num, Var, Assign, BinOp
from three_address_code import TripleProgram, BinOpTriple, AssignTriple


class TACGenerator:
    def __init__(self):
        self.program = TripleProgram()

    
    def gen_stmt(self, stmt):
        if isinstance(stmt, Assign):
            operand = self.gen_expr(stmt.expr)
            self.program.append(AssignTriple(stmt.var.name, operand))
        return self.program


    def gen_expr(self, node):
        """
        TODO(week-4): dispatch on the expression node's type. Returns an
        OPERAND -- a plain variable-name string, a literal's text, or a
        TripleRef (index) -- never an AST node and never a triple itself.        
        """
        if isinstance(node, Num):
            return str(node.value)        #nothing appended to the program
        if isinstance(node, Var):
            return node.name              #nothing appended to the program
        if isinstance(node, BinOp):
            left  = self.gen_expr(node.left)
            right = self.gen_expr(node.right)
            return self.program.append(BinOpTriple(node.op, left, right))


def generate_for_statement(stmt):
    """Wrapper: generate() a fresh TACGenerator for one function."""
    return TACGenerator().gen_stmt(stmt)
