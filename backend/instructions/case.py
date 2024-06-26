from abstract.instruction import Instruction
from environment.environment import Environment
from environment.execute import statementExecuter

class Case(Instruction):
    def __init__(self, exp, block, line, column):
        self.exp = exp
        self.block = block
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        return None