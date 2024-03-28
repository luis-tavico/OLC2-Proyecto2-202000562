from environment.type import ExpressionType

def RootExecuter(instructionList, ast, env):
    for inst in instructionList:
        inst.execute(ast, env)

def statementExecuter(instructionList, ast, env):
    for inst in instructionList:
        res = inst.execute(ast, env)
        if res != None and res != True:
            if res.data_type == ExpressionType.RETURN:
                return res.value
            return res
    return None