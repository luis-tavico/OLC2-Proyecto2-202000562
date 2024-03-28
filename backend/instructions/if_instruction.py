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
    
    def execute(self, ast, env):
        validate = self.exp.execute(ast, env)
        if validate.value:
            if_env = Environment(env, "IF")
            returnValue = statementExecuter(self.if_block, ast, if_env)
            if returnValue != None:
                return returnValue
            return None
        if self.elseifs != None:
            for elseif in self.elseifs:
                validate = elseif.execute(ast, env)
                if validate != None:
                    return validate
        if self.else_block != None:
            else_env = Environment(env, "ELSE")
            returnValue = statementExecuter(self.else_block, ast, else_env)
            if returnValue != None:
                return returnValue
        return None