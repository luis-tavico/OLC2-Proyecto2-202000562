from abstract.instruction import Instruction
from environment.execute import statementExecuter
from environment.environment import Environment

class Elseif(Instruction):
    def __init__(self, exp, block, line, column):
        self.exp = exp
        self.block = block
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        return None