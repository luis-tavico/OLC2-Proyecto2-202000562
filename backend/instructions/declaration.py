from abstract.instruction import Instruction
from expression.primitive import Primitive
from environment.symbol import Symbol
from environment.type import ExpressionType
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
        if self.expression == None:
            if self.data_type == ExpressionType.NUMBER:
                self.expression = Primitive(0, ExpressionType.NUMBER, self.line, self.column)
            elif self.data_type == ExpressionType.STRING:
                self.expression = Primitive("", ExpressionType.STRING, self.line, self.column)
        # Ejecutar expresion
        result = self.expression.execute(ast, env, gen)
        # Asignar tipo si no tiene
        if self.data_type == None:
            self.data_type = result.type
        # Generar simbolo
        if (isinstance(self.expression, Primitive)):
            sym = Symbol(symbol_type=self.symbol_type, id=self.id, data_type=self.data_type, position=result.value, value=self.expression.value, line=self.line, column=self.column)
        else:
            sym = Symbol(symbol_type=self.symbol_type, id=self.id, data_type=self.data_type, position=result.value, value=None, line=self.line, column=self.column)
        # Validar tipo
        if result.type != self.data_type:
            ast.setErrors(Error(type="Semantico", description="Los tipos de dato son incorrectos.", ambit="Global" , line=self.line, column=self.column))
            return
        # Agregar al entorno
        env.saveVariable(ast, self.id, sym)

        return None