from abstract.expression import Expression
from environment.type import ExpressionType
from errors.error import Error

class ArrayAccess(Expression):
    def __init__(self, array, indexes, line, column):
        self.array = array
        self.indexes = indexes
        self.line = line
        self.column = column

    def execute(self, ast, env):
        sym = self.array.execute(ast, env)
        if sym.data_type != ExpressionType.ARRAY:
            ast.setErrors(Error("Semantico", "No se puede acceder a un elemento de un tipo diferente a un arreglo", "ArrayAccess", self.line, self.column))
            return
        return self.index_array(sym.value, self.indexes)

    def index_array(self, array, indexes):
        if len(indexes) == 1:
            return array[indexes[0].value]
        else:
            return self.index_array(array[indexes[0].value].value, indexes[1:])

