from abstract.instruction import Instruction
from environment.environment import Environment
from environment.type import ExpressionType
from environment.execute import statementExecuter
from errors.error import Error

class While(Instruction):
    def __init__(self, exp, block, line, column):
        self.exp = exp
        self.block = block
        self.line = line
        self.column = column

    def execute(self, ast, env):
        safe_cont = 0
        flag = None
        result = None
        while True:
            safe_cont += 1
            result = self.exp.execute(ast, env)
            if result.value:
                while_env = Environment(env, "WHILE")
                flag = statementExecuter(self.block, ast, while_env)
                if flag != None:
                    if flag.data_type == ExpressionType.BREAK:
                        break
                    if flag.data_type == ExpressionType.CONTINUE:
                        continue
                    if flag.data_type == ExpressionType.RETURN:
                        return flag
            else:
                break
            if safe_cont >= 1000:
                ast.setErrors(Error("Semantico", "Se ha excedido el maximo de ciclos permitidos." , "While", self.line, self.column))
                break
        return None