from environment.type import ExpressionType

def rootExecuter(instructions, ast, env, gen):
    for instruction in instructions:
        instruction.execute(ast, env, gen)

def statementExecuter(instructions, ast, env, gen):
    for instruction in instructions:
        res = instruction.execute(ast, env, gen)
        if res != None:
            if res.type == ExpressionType.BREAK or res.type == ExpressionType.CONTINUE:
                return res
    return None