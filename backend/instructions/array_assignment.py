from abstract.instruction import Instruction
from environment.type import ExpressionType
from errors.error import Error


class Arrayassignment(Instruction):
    def __init__ (self, id, indexes, expression, line, column):
        self.id = id
        self.indexes = indexes
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        return None