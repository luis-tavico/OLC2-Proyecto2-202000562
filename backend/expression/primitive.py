from abstract.expression import Expression
from environment.symbol import Symbol

class Primitive(Expression):
    def __init__(self, value, type, line, column):
        self.value = value
        self.type = type
        self.line = line
        self.column = column

    def execute(self, ast, env):
        return Symbol(symbol_type=None, value=self.value, data_type=self.type, environment=env, line=self.line, column=self.column)