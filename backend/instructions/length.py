from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.symbol import Symbol
from errors.error import Error

class Length(Instruction):
    def __init__(self, array, line, column):
        self.array = array
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        return None