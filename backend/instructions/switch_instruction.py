from abstract.instruction import Instruction

class Switch(Instruction):
    def __init__(self, exp, cases, line, column):
        self.exp = exp
        self.cases = cases
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        return None