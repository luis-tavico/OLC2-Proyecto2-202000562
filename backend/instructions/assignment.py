from abstract.instruction import Instruction

class Assignment(Instruction):
    def __init__(self, id, type_assignment, expression, line, column):
        self.id = id
        self.type_assignment = type_assignment
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env):
        result = self.expression.execute(ast, env)
        env.setSymbol(ast, self.id, self.type_assignment , result)