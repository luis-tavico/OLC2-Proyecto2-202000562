from abstract.instruction import Instruction
from environment.environment import Environment
from environment.type import ExpressionType
from environment.execute import statementExecuter
from expression.access import Access
from instructions.declaration import Declaration
from errors.error import Error

class For(Instruction):
    def __init__(self, declaration, exp1, exp2, block, line, column):
        self.declaration = declaration
        self.exp1 = exp1
        self.exp2 = exp2
        self.block = block
        self.line = line
        self.column = column
   
    def execute(self, ast, env, gen):
        return None