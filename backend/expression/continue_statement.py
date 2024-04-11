from abstract.expression import Expression
from environment.symbol import Symbol
from environment.type import ExpressionType
from errors.error import Error

class Continue(Expression):
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        return None