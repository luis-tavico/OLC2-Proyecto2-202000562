from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.environment import Environment
from errors.error import Error

class ArrayDeclaration(Instruction):
    def __init__(self, id, type, exp, line, column):
        self.id = id
        self.type = type
        self.exp = exp
        self.line = line
        self.column = column

    def execute(self, ast, env):
        result = self.exp.execute(ast, env)
        if result.data_type != ExpressionType.ARRAY:
            ast.setErrors(Error("Semantico", "La expresión no es un arreglo", "ArrayDeclaration", self.line, self.column))
            return
        for res in result.value:
            if isinstance(res, Environment):
                print(res.id)
            elif res.data_type != self.type and res.data_type != ExpressionType.ARRAY:
                ast.setErrors(Error("Semantico", "El arreglo contiene tipos incorrectos", "ArrayDeclaration", self.line, self.column))
                return
        env.saveSymbol(ast, self.id, result)