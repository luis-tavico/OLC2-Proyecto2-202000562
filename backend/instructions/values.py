from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.symbol import Symbol
from errors.error import Error

class Values():
    def __init__ (self, instance, line, column):
        self.instance = instance
        self.line = line
        self.column = column

    def execute(self, ast, env):
        env_interface = self.instance.execute(ast, env)
        struct = env_interface.symbols_table
        values = []
        for value in list(struct.values()):
            values.append(value)
        return Symbol(symbol_type=None, value=values, data_type=ExpressionType.ARRAY, environment=env, line=self.line, column=self.column)
