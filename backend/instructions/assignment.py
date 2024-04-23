from abstract.instruction import Instruction
from environment.symbol import Symbol

class Assignment(Instruction):
    def __init__(self, id, type_assignment, expression, line, column):
        self.id = id
        self.type_assignment = type_assignment
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        # Obtener valor
        result = self.expression.execute(ast, env, gen)
        sym = Symbol(symbol_type='', id=self.id, data_type=result.type, position=result.value, line=self.line, column=self.column)
        # Editar simbolo
        env.setVariable(ast, self.id, sym)
        return None