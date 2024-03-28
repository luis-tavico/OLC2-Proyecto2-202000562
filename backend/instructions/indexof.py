from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.symbol import Symbol
from errors.error import Error

class Indexof(Instruction):
    def __init__(self, array, expression, line, column):
        self.array = array
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env):
        sym = self.array.execute(ast, env)
        if sym.data_type != ExpressionType.ARRAY:
            ast.setErrors(Error("Semantico", "No se puede acceder a un elemento de un tipo diferente a un arreglo", "ArrayAccess", self.line, self.column))
            return None
        val = self.expression.execute(ast, env)
        for i, val_arr in enumerate(sym.value):
            if val_arr.value == val.value:
                return Symbol(symbol_type=None, value=i, data_type=ExpressionType.NUMBER, environment=env, line=self.line, column=self.column)
        return Symbol(symbol_type=None, value=-1, data_type=ExpressionType.NUMBER, environment=env, line=self.line, column=self.column)
