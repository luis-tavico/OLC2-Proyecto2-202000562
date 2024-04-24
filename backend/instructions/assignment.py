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
        gen.comment('Asignacion de variable')
        # Obtener valor
        result = self.expression.execute(ast, env, gen)
        # Obteniendo la posicion
        sym = env.getVariable(ast, self.id, {'line': self.line, 'column': self.column})
        # Sustituyendo valor
        if 't' in str(result.value):
            gen.add_move('t0', str(result.value))
        else:
            gen.add_li('t0', str(result.value))
        gen.add_lw('t1', '0(t0)')
        gen.add_li('t3', str(sym.position))
        gen.add_sw('t1', '0(t3)')
        gen.comment('Fin asignacion')
        return None