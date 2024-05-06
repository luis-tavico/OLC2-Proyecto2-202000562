from abstract.expression import Expression
from environment.type import ExpressionType
from environment.value import Value

class Continue(Expression):
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        val = Value("", True, ExpressionType.CONTINUE, [], [], [])
        return val