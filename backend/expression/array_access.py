from abstract.expression import Expression
from environment.type import ExpressionType
from errors.error import Error

class ArrayAccess(Expression):
    def __init__(self, array, indexes, line, column):
        self.array = array
        self.indexes = indexes
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        return None

