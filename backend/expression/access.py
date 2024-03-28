from abstract.expression import Expression

class Access(Expression):
    def __init__(self, id, line, column):
        self.id = id
        self.line = line
        self.column = column

    def execute(self, ast, env):
        sym = env.getSymbol(ast, self.id)
        return sym