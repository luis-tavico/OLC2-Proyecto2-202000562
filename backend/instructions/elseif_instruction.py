from abstract.instruction import Instruction
from environment.execute import statementExecuter
from environment.environment import Environment

class Elseif(Instruction):
    def __init__(self, exp, block, line, column):
        self.exp = exp
        self.block = block
        self.line = line
        self.column = column

    def execute(self, ast, env):
        validate = self.exp.execute(ast, env)
        if validate.value:
            else_if_env = Environment(env, "ELSE_IF")
            result = statementExecuter(self.block, ast, else_if_env)
            if result == None:
                return True
            else:
                return result
        return None