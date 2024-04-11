from abstract.instruction import Instruction
from environment.type import ExpressionType
from expression.primitive import Primitive
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
        return None