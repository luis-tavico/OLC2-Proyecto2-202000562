from abstract.instruction import Instruction
from environment.execute import statementExecuter
from environment.environment import Environment

class If(Instruction):
    def __init__(self, exp, if_block, elseifs, else_block, line, column):
        self.exp = exp
        self.if_block = if_block
        self.elseifs = elseifs
        self.else_block = else_block
        self.line = line
        self.column = column  
    
    def execute(self, ast, env, gen):
        return None