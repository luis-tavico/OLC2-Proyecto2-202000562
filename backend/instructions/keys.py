from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.symbol import Symbol
from errors.error import Error

class Keys(Instruction):
    def __init__ (self, instance, line, column):
        self.instance = instance
        self.line = line
        self.column = column

    def execute(self, ast, env):
        env_interface = self.instance.execute(ast, env)
        struct = env_interface.symbols_table
        keys = []
        for key in list(struct.keys()):
            keys.append(Symbol(symbol_type=None, value=key, data_type=ExpressionType.STRING, environment=env, line=self.line, column=self.column))
        return Symbol(symbol_type=None, value=keys, data_type=ExpressionType.ARRAY, environment=env, line=self.line, column=self.column)