from abstract.expression import Expression
from environment.type import ExpressionType
from environment.value import Value

class Return(Expression):
    def __init__(self, exp, line, column):
        self.line = line
        self.column = column
        self.exp = exp

    def execute(self, ast, env, gen):
        # Ejecutar expresion
        result = self.exp.execute(ast, env, gen)
        val = Value(result.value, True, ExpressionType.RETURN, [], [], [])
        return val