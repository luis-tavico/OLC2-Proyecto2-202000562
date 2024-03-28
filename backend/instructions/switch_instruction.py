from abstract.instruction import Instruction

class Switch(Instruction):
    def __init__(self, exp, cases, line, column):
        self.exp = exp
        self.cases = cases
        self.line = line
        self.column = column

    def execute(self, ast, env):
        exp = self.exp.execute(ast, env).value
        for case in self.cases:
            if case.exp != None:
                exp_case = case.exp.execute(ast, env).value
                if exp == exp_case:
                    returnValue = case.execute(ast, env)
                    if returnValue != None:
                        return returnValue
            else:
                default = case.execute(ast, env)
        return None

