from environment.type import ExpressionType

def rootExecuter(instructions, ast, env, gen):
    for instruction in instructions:
        instruction.execute(ast, env, gen)

def statementExecuter(instructions, ast, env, gen):
    for instruction in instructions:
        res = instruction.execute(ast, env, gen)
        
        '''
        if res != None and res != True:      
            if res.data_type == ExpressionType.RETURN:
                return res.value
            return res
        '''

    return None