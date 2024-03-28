from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.symbol import Symbol
from errors.error import Error

class Tostring(Instruction):
    def __init__(self, expression, line, column):
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env):
        val = self.expression.execute(ast, env) 
        if val.data_type == ExpressionType.NUMBER or val.data_type == val.data_type == ExpressionType.FLOAT:
            return Symbol(symbol_type=None, value=str(val.value), data_type=ExpressionType.STRING, environment=env, line=self.line, column=self.column)
        elif val.data_type == ExpressionType.BOOLEAN:
            if val.value:
                return Symbol(symbol_type=None, value="true", data_type=ExpressionType.STRING, environment=env, line=self.line, column=self.column)
            return Symbol(symbol_type=None, value="false", data_type=ExpressionType.STRING, environment=env, line=self.line, column=self.column)
        else:
            ast.setErrors(Error("Semantico", "Se ha excedido el maximo de ciclos permitidos.", "For", self.line, self.column))
        return None
