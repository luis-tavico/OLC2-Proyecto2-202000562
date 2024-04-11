from abstract.instruction import Instruction
from environment.type import ExpressionType
from errors.error import Error

class Push(Instruction):
    def __init__(self, array, expression, line, column):
        self.array = array
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        return None