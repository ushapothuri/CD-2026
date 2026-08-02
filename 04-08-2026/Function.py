"""
Function --  fully implemented.

Function has:
1. local SymbolTable -  contains information about all the local variables used in the function, 
which is mainly populated when declarations are parsed
2. AST list :  holds the statement AST list for one function, except declaration statement 
3. tripleTACstmts : holds the list of three address code statements in triples form
"""
from SymbolTable import SymbolTable
from three_address_code import TripleTAC

class Function:
    def __init__(self, returnType, name):
        self.returnType = returnType
        self.name = name
        self.statementsAstList = []
        self.localSymbolTable = SymbolTable()
        self.tripleTACstmts = TripleTAC()

    def setStatementsAstList(self, sastList):
        self.statementsAstList = sastList

    def getStatementsAstList(self):
        return self.statementsAstList

    def addStatement(self, stmt):
        self.statementsAstList.append(stmt)

    def setLocalSymbolTable(self, localList):
        self.localSymbolTable = localList

    def getLocalSymbolTable(self):
        return self.localSymbolTable

    def getReturnType(self):
        return self.returnType

    def getName(self):
        return self.name

    def generateTripleTAC(self):
        tacgen = TACGenerator()
        self.tripleTACstmts = tacgen.generate(self)

    def renderTripleTAC(self):
        return self.tripleTACstmts.render()

    def compile(self):
        pass


