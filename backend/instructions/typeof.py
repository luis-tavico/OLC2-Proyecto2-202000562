from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.symbol import Symbol
from errors.error import Error

class Typeof(Instruction):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env):
        val = self.expression.execute(ast, env)
        if val:
            return Symbol(symbol_type=None, value=val.data_type.name.lower(), data_type=ExpressionType.STRING, environment=env, line=self.line, column=self.column)
        return None