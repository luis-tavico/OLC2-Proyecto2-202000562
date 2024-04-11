from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.symbol import Symbol
from errors.error import Error

class Touppercase(Instruction):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        return None