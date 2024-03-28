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
   
    def execute(self, ast, env):
        if self.declaration == None:
            self.exp2 = Access(self.exp2, self.line, self.column)
            array = self.exp2.execute(ast, env)
            if array.data_type != ExpressionType.ARRAY:
                ast.setErrors(Error("Semantico", "Se esperaba un array", "For", self.line, self.column))
                return
            else:
                for index, val in enumerate(array.value):
                    if index == 0:
                        for_env = Environment(env, "FOR")
                        declaration = Declaration(None, self.exp1, val.data_type, None, self.line, self.column)
                        declaration.execute(ast, for_env)
                    for_env.setSymbol(ast, self.exp1, "=" , val)
                    flag = statementExecuter(self.block, ast, for_env)
                    if flag != None:
                        if flag.data_type == ExpressionType.BREAK:
                            break
                        if flag.data_type == ExpressionType.CONTINUE:
                            continue
                        if flag.data_type == ExpressionType.RETURN:
                            return flag
        else:
            for_env = Environment(env, "FOR")
            self.declaration.execute(ast, for_env)
            safe_cont = 0
            flag = None
            result = None
            while True:
                safe_cont += 1
                result = self.exp1.execute(ast, for_env)
                if result.value:
                    for_env = Environment(for_env, "for_env")
                    flag = statementExecuter(self.block, ast, for_env)
                    self.exp2.execute(ast, for_env)
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
                    ast.setErrors(Error("Semantico", "Se ha excedido el maximo de ciclos permitidos.", "For", self.line, self.column))
                    break
        return None