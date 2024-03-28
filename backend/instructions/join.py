from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.symbol import Symbol
from errors.error import Error

class Join(Instruction):
    def __init__(self, array, line, column):
        self.array = array
        self.line = line
        self.column = column

    def execute(self, ast, env):
        sym = self.array.execute(ast, env)
        if sym.data_type != ExpressionType.ARRAY:
            ast.setErrors(Error("Semantico", "No se puede acceder a un elemento de un tipo diferente a un arreglo", "ArrayAccess", self.line, self.column))
            return None

        array_temp = []
        val = ""
        for arr in sym.value:
            array_temp.append(str(arr.value))
        val += ', '.join(map(str, array_temp))
        return Symbol(symbol_type=None, value=val, data_type=ExpressionType.STRING, environment=env, line=self.line, column=self.column)