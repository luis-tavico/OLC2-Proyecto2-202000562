from abstract.expression import Expression

class Ternary(Expression):
    def __init__(self, exp1, exp2, exp3, line, column):
        self.exp1 = exp1
        self.exp2 = exp2
        self.exp3 = exp3
        self.line = line
        self.column = column

    def execute(self, ast, env):
        condition = self.exp1.execute(ast, env)
        if condition.value:
            return self.exp2.execute(ast, env)
        return self.exp3.execute(ast, env)