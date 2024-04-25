from abstract.instruction import Instruction
from environment.symbol import Symbol
from expression.operation import Operation
from expression.access import Access

class Assignment(Instruction):
    def __init__(self, id, type_assignment, expression, line, column):
        self.id = id
        self.type_assignment = type_assignment
        self.expression = expression
        self.line = line
        self.column = column
   
    def execute(self, ast, env, gen):
        if self.type_assignment == '=':
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
        elif self.type_assignment == '+=':
            gen.comment('Incremento de variable')
            # Obtener valor
            sym = Access(self.id, self.line, self.column)
            # Efectuar operacion
            result = Operation(sym, '+', self.expression, self.line, self.column)
            result = result.execute(ast, env, gen)
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
        elif self.type_assignment == '-=':
            gen.comment('Incremento de variable')
            # Obtener valor
            sym = Access(self.id, self.line, self.column)
            # Efectuar operacion
            result = Operation(sym, '-', self.expression, self.line, self.column)
            result = result.execute(ast, env, gen)
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