from abstract.instruction import Instruction
from environment.type import ExpressionType
from errors.error import Error

class Push(Instruction):
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
        exp = self.expression.execute(ast, env)
        sym.value.append(exp)
        return None