from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.symbol import Symbol
from errors.error import Error

class Tolowercase(Instruction):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env):
        val = self.expression.execute(ast, env)
        if val.data_type == ExpressionType.STRING:
            return Symbol(symbol_type=None, value=val.value.lower(), data_type=ExpressionType.STRING, environment=env, line=self.line, column=self.column)
        else:
            ast.setErrors(Error("Semantico", "Se esperaba un tipo STRING.", "ToLowerCase", self.line, self.column))
        return None