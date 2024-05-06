from abstract.instruction import Instruction
from environment.type import ExpressionType
from errors.error import Error

class Push(Instruction):
    def __init__(self, array, expression, line, column):
        self.array = array
        self.expression = expression
        self.line = line
        self.column = column

    def execute(self, ast, env, gen):
        # Obtner arreglo
        sym = env.getVariable(ast, self.array.id, {'line': self.line, 'column': self.column})
        if(sym.data_type == ExpressionType.NULL):
            ast.setErrors(Error(type="Semantico", description=f"El arreglo {self.array} no ha sido encontrado", ambit=env.id , line=self.line, column=self.column))
            return None
        # Obtener tamaño de arreglo
        size = env.getVariable(ast, sym.position+"_length", {'line': self.line, 'column': self.column})
        gen.add_br()
        gen.comment('Push a un arreglo')
        # Traer el arreglo
        gen.add_la('t4', str(sym.position))
        # Cargar longitud
        gen.add_br()
        gen.add_li('t3', str(size.position))
        gen.add_lw('t1', '0(t3)')
        gen.add_li('t2', str(4))
        # Multiplicar el indice por el tamaño de cada elemento (4 bytes)
        gen.add_br()
        gen.add_operation('mul', 't1', 't1', 't2')
        # Sumar el desplazamiento a la dirección base
        gen.add_operation('add', 't4', 't4', 't1')
        # Acceder al valor en la direccion calculada
        gen.add_lw('t3', '0(t4)')
        # Ejecutar expresion
        self.expression.execute(ast, env, gen)
        gen.add_br()
        # Guardar nuevo valor
        gen.add_sw('t3', '0(t4)')
        # Incrementar la longitud
        gen.add_br()
        gen.add_li('t3', str(size.position))
        gen.add_lw('t1', '0(t3)')
        gen.add_operation('addi', 't1', 't1', '1')
        gen.add_sw('t1', '0(t3)')

        return None