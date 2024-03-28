from abstract.instruction import Instruction
from environment.type import ExpressionType
from errors.error import Error


class Arrayassignment(Instruction):
    def __init__ (self, id, indexes, expression, line, column):
        self.id = id
        self.indexes = indexes
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env):
        sym = self.id.execute(ast, env)
        if sym.data_type != ExpressionType.ARRAY:
            ast.setErrors(Error("Semantico", "No se puede acceder a un elemento de un tipo diferente a un arreglo", "ArrayAccess", self.line, self.column))
            return
        exp = self.expression.execute(ast, env)
        return self.change_value(sym.value, self.indexes, exp)

    def change_value(self, array, indexes, new_value):
        if len(indexes) == 1:
            array[indexes[0].value] = new_value
        else:
            self.change_value(array[indexes[0].value].value, indexes[1:], new_value)