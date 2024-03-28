from abstract.instruction import Instruction
from environment.type import ExpressionType
from errors.error import Error

class Pop(Instruction):
    def __init__(self, array, line, column):
        self.array = array
        self.line = line
        self.column = column

    def execute(self, ast, env):
        sym = self.array.execute(ast, env)
        if sym.data_type != ExpressionType.ARRAY:
            ast.setErrors(Error("Semantico", "No se puede acceder a un elemento de un tipo diferente a un arreglo", "ArrayAccess", self.line, self.column))
            return None
        val = sym.value.pop()
        return val