from abstract.instruction import Instruction
from environment.type import ExpressionType
from environment.value import Value

class Indexof(Instruction):
    def __init__(self, array, expression, line, column):
        self.array = array
        self.expression = expression
        self.line = line
        self.column = column
        
    def execute(self, ast, env, gen):
        # Obtner arreglo
        sym = self.array.execute(ast, env, gen)
        # Obtener valor a buscar
        val = self.expression.execute(ast, env, gen)
        # Creando indice
        indx = gen.new_temp()
        gen.add_br()
        gen.comment('Agregando un primitivo numerico')
        gen.add_li('t0', str(-1))
        gen.add_li('t3', str(indx))
        gen.add_sw('t0', '0(t3)')
        # Traer el arreglo
        gen.add_la('t0', str(sym.value))
        # Inicializando contador
        gen.add_li('t1', str(0))
        # Creando etiqueta de ciclo
        looplbl = gen.new_label()
        gen.add_br()
        # Cargando valores del arreglo
        gen.new_body_label(looplbl)
        gen.add_lw('t3', '0(t0)')
        gen.add_lw('t2', '0(t3)')
        # Ejecutar condicion
        trueLvl = gen.new_label()
        falseLvl = gen.new_label()
        # Cargar valor a buscar
        gen.add_li('t3', str(val.value))
        gen.add_lw('t4', '0(t3)')
        # Agregando condición
        gen.add_beq('t4', 't2', trueLvl)
        # Agregando salto
        gen.add_jump(falseLvl)
        gen.add_br()
        # Etiqueta de salida
        exit = gen.new_label()
        gen.new_body_label(trueLvl)
        gen.add_li('t3', str(indx))
        gen.add_sw('t1', '0(t3)')
        # Salir
        gen.add_jump(exit)
        gen.add_br()
        gen.new_body_label(falseLvl)
        # Incrementar el puntero del arreglo
        gen.add_operation('addi', 't0', 't0', '4') # El 4 son 4 bytes (tamaño de un entero)
        # Incrementar el contador
        gen.add_operation('addi', 't1', 't1', '1')
        # obteniendo longitud
        sym = env.getVariable(ast, sym.value+"_length", {'line': self.line, 'column': self.column})
        # Cargando longitud
        gen.add_br()
        gen.comment('Agregando un primitivo numerico')
        gen.add_li('t3', str(sym.position))
        gen.add_lw('t2', "0(t3)")
        # Condicion
        gen.add_br()
        gen.add_bne('t1', 't2', looplbl)
        # salir
        gen.new_body_label(exit)
        return Value(str(indx), True, ExpressionType.NUMBER, [], [], [])