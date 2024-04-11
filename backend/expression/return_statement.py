from abstract.expression import Expression
from environment.symbol import Symbol
from environment.type import ExpressionType
from errors.error import Error

class Return(Expression):
    def __init__(self, exp, line, column):
        self.line = line
        self.column = column
        self.exp = exp

    def execute(self, ast, env, gen):
        return None