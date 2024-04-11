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

    def execute(self, ast, env, gen):
        return None