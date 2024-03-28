from abstract.expression import Expression
from environment.symbol import Symbol
from environment.type import ExpressionType
from errors.error import Error

class Continue(Expression):
    def __init__(self, line, column):
        self.line = line
        self.column = column

    def execute(self, ast, env):
        if env.loopValidation():
            return Symbol(symbol_type=None, value=None, data_type=ExpressionType.CONTINUE, environment=env, line=self.line, column=self.column)
        ast.setErrors(Error("La declaracion Continue no esta dentro de un ciclo.", self.line, self.column))
        return Symbol(symbol_type=None, value=None, data_type=ExpressionType.NULL, environment=env, line=self.line, column=self.column)