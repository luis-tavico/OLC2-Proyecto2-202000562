from abstract.instruction import Instruction
from environment.type import ExpressionType
from errors.error import Error

class Pop(Instruction):
    def __init__(self, array, line, column):
        self.array = array
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        return None