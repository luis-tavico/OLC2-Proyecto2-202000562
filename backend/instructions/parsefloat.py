from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.symbol import Symbol
from errors.error import Error

class Parsefloat(Instruction):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env):
        exp = self.expression.execute(ast, env)
        if exp.data_type != ExpressionType.STRING:
            ast.setErrors(Error("Semantico", "El tipo de dato no es STRING", "Parsefloat", self.line, self.column))
            return
        try:
            return Symbol(symbol_type=None, value=float(exp.value), data_type=ExpressionType.FLOAT, environment=env, line=self.line, column=self.column)
        except:
            ast.setErrors(Error("Semantico", "No se puede convertir a entero", "Parsefloat", self.line, self.column))
            return None