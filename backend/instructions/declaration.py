from abstract.instruction import Instruction
from environment.symbol import Symbol
from errors.error import Error

class Declaration(Instruction):
    def __init__(self, symbol_type, id, data_type, expression, line, column):
        self.symbol_type = symbol_type
        self.id = id
        self.data_type = data_type
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        # Generar simbolo
        result = self.expression.execute(ast, env, gen)
        sym = Symbol(symbol_type=self.symbol_type, id=self.id, data_type=self.data_type, position=result.value, line=self.line, column=self.column)
        # Validar tipo
        if result.type != self.data_type:
            ast.setErrors(Error(type="Semantico", description="Los tipos de dato son incorrectos.", ambit="Global" , line=self.line, column=self.column))
            return
        # Agregar al entorno
        env.saveVariable(ast, self.id, sym)
        return None