from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.value import Value

class Typeof(Instruction):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        exp = self.expression.execute(ast, env, gen)
        if exp.type == ExpressionType.NUMBER:
            return Value("str_number", False, ExpressionType.STRING, [], [], [])
        elif exp.type == ExpressionType.STRING:
            return Value("str_string", False, ExpressionType.STRING, [], [], [])
        elif exp.type == ExpressionType.BOOLEAN:
            return Value("str_boolean", False, ExpressionType.STRING, [], [], [])
        return None