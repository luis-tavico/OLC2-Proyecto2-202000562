from abstract.expression import Expression
from environment.symbol import Symbol
from environment.type import ExpressionType
from errors.error import Error

class Return(Expression):
    def __init__(self, exp, line, column):
        self.line = line
        self.column = column
        self.exp = exp

    def execute(self, ast, env):
        if env.functionValidation():
            if self.exp == None:
                return Symbol(symbol_type=None, value=None, data_type=ExpressionType.RETURN, environment=env, line=self.line, column=self.column)
            sym = self.exp.execute(ast, env)
            return Symbol(symbol_type=None, value=sym, data_type=ExpressionType.RETURN, environment=env, line=self.line, column=self.column)
        ast.setErrors(Error("Semantico", "Return fuera de una funcion", self.line, self.column))
        return Symbol(symbol_type=None, value=None, data_type=ExpressionType.NULL, environment=env, line=self.line, column=self.column)